import datetime

from flask import Flask, render_template

from model import TrackingContext


class RadarServer(Flask):

    def __init__(self, context: TrackingContext):
        super(RadarServer, self).__init__(__name__)
        self.context = context
        self.add_url_rule('/', 'index', self.index)
        self.add_template_filter(self.filter_torowclass, 'torowclass')
        self.add_template_filter(self.filter_toelapsed, 'toelapsed')
        self.add_template_filter(self.filter_tolen, 'tolen')

    def index(self):
        return render_template('tracking.html', aircrafts=self.context.aircrafts)

    def filter_torowclass(self, input: bool) -> str:
        return 'table-light' if input else 'table-warning'

    def filter_toelapsed(self, input: datetime.timedelta) -> str:
        return '%ds ago' % (input.total_seconds())

    def filter_tolen(self, o) -> int:
        return len(o)
