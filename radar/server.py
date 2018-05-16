import datetime
from io import BytesIO

import matplotlib.pyplot as plt
from flask import Flask, render_template, make_response

from model import TrackingContext, TrackingObserver, Aircraft
from poi import airport_coords, center_coord


class RadarServer(Flask, TrackingObserver):

    def __init__(self, context: TrackingContext):
        super(RadarServer, self).__init__(__name__)
        self.context = context
        self.context.addObserver(self)
        self.aircraft_paths = {}
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/map', 'map', self.map)
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

    def map(self):
        plt.style.use('bmh')
        plt.figure(figsize=(12, 8), dpi=80, facecolor='1.0')

        for cs, path in self.aircraft_paths.items():
            plt.scatter(x=[p[1] for p in path], y=[p[0] for p in path], label=cs)

        plt.plot([airport_coords[0][1], airport_coords[1][1]],
                 [airport_coords[0][0], airport_coords[1][0]], 'k-', lw=2)

        rad = 0.001
        plt.plot([center_coord[1] - rad, center_coord[1] + rad],
                 [center_coord[0] - rad, center_coord[0] + rad],
                 'k-', lw=2)
        plt.plot([center_coord[1] - rad, center_coord[1] + rad],
                 [center_coord[0] + rad, center_coord[0] - rad],
                 'k-', lw=2)

        plt.legend()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        response = make_response(img.getvalue())
        response.headers['Content-Type'] = 'image/png'
        img.close()

        return response

    def aircraft_updated(self, aircraft: Aircraft):
        if aircraft.lat is None or aircraft.lon is None:
            return

        cs = aircraft.callsign

        if not cs in self.aircraft_paths:
            self.aircraft_paths[cs] = []

        coord = (aircraft.lat, aircraft.lon)

        if coord not in self.aircraft_paths[cs]:
            self.aircraft_paths[cs].append(coord)
