import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, make_response

from model import TrackingContext


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
        pm10 = np.array(['23', '45', '56', '12'])
        pm25 = np.array(['34', '56', '59', '34'])
        dates = np.array(['2017-12-20', '2017-12-21', '2017-12-22', '2017-12-23'])

        plt.figure(figsize=(12, 8), dpi=80, facecolor='1.0')
        plt.title("GangNam", fontsize=20)
        plt.plot_date(dates, pm10, 'rs--', label='pm10')
        plt.plot_date(dates, pm25, 'gs--', label='pm25')
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
