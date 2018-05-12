import datetime
from io import BytesIO

import matplotlib.pyplot as plt
from flask import Flask, render_template, make_response

from model import TrackingContext

reference_position = (49, 5.68333)


class RadarServer(Flask):

    def __init__(self, context: TrackingContext):
        super(RadarServer, self).__init__(__name__)
        self.context = context
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/map', 'map', self.map)
        self.add_template_filter(self.filter_torowclass, 'torowclass')
        self.add_template_filter(self.filter_toelapsed, 'toelapsed')
        self.add_template_filter(self.filter_tolen, 'tolen')

    def index(self):
        return render_template('tracking.html', aircrafts=self.context.aircrafts)

    def map(self):
        plt.style.use('bmh')
        plt.figure(figsize=(12, 8), dpi=80, facecolor='1.0')

        plt.scatter(x=[reference_position[0]],
                    y=[reference_position[1]],
                    label='Antenna')

        plt.scatter(x=[a.lon for a in self.context.aircrafts],
                    y=[a.lat for a in self.context.aircrafts],
                    label='Aircrafts')

        plt.legend()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        response = make_response(img.getvalue())
        response.headers['Content-Type'] = 'image/png'
        img.close()

        return response

    def filter_torowclass(self, input: bool) -> str:
        return 'table-light' if input else 'table-warning'

    def filter_toelapsed(self, input: datetime.timedelta) -> str:
        return '%ds ago' % (input.total_seconds())

    def filter_tolen(self, o) -> int:
        return len(o)
