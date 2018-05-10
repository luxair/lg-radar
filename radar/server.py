from flask import Flask, render_template

from model import TrackingContext


class RadarServer(Flask):

    def __init__(self, context: TrackingContext):
        super(RadarServer, self).__init__(__name__)
        self.context = context
        self.add_url_rule('/', 'index', self.index)

    def index(self):
        return render_template('tracking.html', aircrafts=self.context.aircrafts.keys())
