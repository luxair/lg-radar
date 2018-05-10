import datetime
import subprocess
from threading import Thread

import pyModeS as pms

from model import TrackingContext


class AdsbThread(Thread):
    def __init__(self, context: TrackingContext):
        super(AdsbThread, self).__init__()
        self.context = context

    def run(self):
        with subprocess.Popen(['rtl_adsb'], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as adsb_flow:
            while True:
                msg = adsb_flow.stdout.readline()

                if len(msg) == 0:
                    break

                self.process_adsb(msg.decode('ascii').strip('*;\r\n'))

    def process_adsb(self, msg):
        if pms.bin2int(pms.crc(msg)) != 0:
            return

        tc = pms.adsb.typecode(msg)
        icao = pms.adsb.icao(msg)

        if tc in [1, 2, 3, 4]:
            callsign = pms.adsb.callsign(msg).strip('_')
            print(msg, '%2d' % tc, pms.adsb.icao(msg), callsign)
            self.context.registerAircraft(pms.adsb.icao(msg), callsign)

        if tc in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
            altitude = pms.adsb.altitude(msg)
            aircraft = self.context.getAircraft(icao)

            if aircraft is not None:
                aircraft.messages += 1
                aircraft.lastmessage = datetime.datetime.now()
                aircraft.altitude = altitude

            print(
                msg, '%2d' % tc, icao,
                altitude,
                aircraft
            )

        if tc in [19]:
            velocity = pms.adsb.velocity(msg)
            aircraft = self.context.getAircraft(icao)

            if aircraft is not None:
                aircraft.messages += 1
                aircraft.lastmessage = datetime.datetime.now()
                aircraft.speed, aircraft.heading, \
                aircraft.vspeed, aircraft.sptype = velocity

            print(
                msg, '%2d' % tc, icao,
                velocity,
                aircraft
            )
