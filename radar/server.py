import datetime

from flask import Flask, render_template, make_response

from model import TrackingContext, TrackingObserver, Aircraft

class RadarServer(Flask, TrackingObserver):

    def __init__(self, context: TrackingContext):
        super(RadarServer, self).__init__(__name__)
        self.context = context
        self.context.addObserver(self)
        self.aircraft_paths = {}
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

    def aircraft_updated(self, aircraft: Aircraft):
        if aircraft.lat is None or aircraft.lon is None:
            return

        cs = aircraft.callsign

        if not cs in self.aircraft_paths:
            self.aircraft_paths[cs] = []

        coord = (aircraft.lat, aircraft.lon)

        if coord not in self.aircraft_paths[cs]:
            self.aircraft_paths[cs].append(coord)
