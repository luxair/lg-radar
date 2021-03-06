import datetime
import subprocess
from threading import Thread

import pyModeS as pms

from model import TrackingContext, Aircraft

TC_IDENTIFICATION = [1, 2, 3, 4]
TC_POSITION = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
TC_VELOCITY = [19]


def compute_location(aircraft: Aircraft):
    last_o = None
    last_e = None

    for msgentry in aircraft.messages.entries:
        msg = msgentry.message
        tc = pms.adsb.typecode(msg)

        if tc in TC_POSITION:
            oe_flag = pms.adsb.oe_flag(msg)

            if oe_flag == 0:
                last_e = msgentry
            else:
                last_o = msgentry

    if last_o is not None and last_e is not None and \
            pms.adsb.df(last_e.message) == pms.adsb.df(last_o.message) and \
            pms.adsb.typecode(last_e.message) == pms.adsb.typecode(last_o.message) and \
            abs((last_e.timestamp - last_o.timestamp).total_seconds()) < 30:
        pos = pms.adsb.position(last_e.message, last_o.message, last_e.timestamp, last_o.timestamp)
        # print(pos, 'as of', last_o.timestamp, last_e.timestamp)
        return pos or (None, None)
    else:
        return None, None


class AdsbThread(Thread):
    def __init__(self, context: TrackingContext):
        super(AdsbThread, self).__init__()
        self.context = context
        self.messages = 0
        self.rejects = 0

    def run(self):
        with subprocess.Popen(['rtl_adsb', '-g', '48'], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as adsb_flow:
            while True:
                msg = adsb_flow.stdout.readline()

                if len(msg) == 0:
                    break

                self.process_adsb(msg.decode('ascii').strip('*;\r\n'))

    def process_adsb(self, msg: str) -> None:
        self.messages += 1

        msg = self.correct(msg)

        if pms.bin2int(pms.crc(msg)) != 0:
            self.rejects += 1
            return
        # print('Error rate:', 100 * self.rejects / self.messages)

        tc = pms.adsb.typecode(msg)
        icao = pms.adsb.icao(msg)

        if tc in TC_IDENTIFICATION:
            callsign = pms.adsb.callsign(msg).strip('_')
            print(msg, '%2d' % tc, pms.adsb.icao(msg), callsign)
            aircraft = self.context.registerAircraft(pms.adsb.icao(msg), callsign)
            aircraft.messages.add(msg)
            self.context.notify(aircraft)

        if tc in TC_POSITION:
            altitude = pms.adsb.altitude(msg)
            aircraft = self.context.getAircraft(icao)

            if aircraft is not None:
                aircraft.messages.add(msg)
                aircraft.lastmessage = datetime.datetime.now()
                aircraft.altitude = altitude
                lat, lon = compute_location(aircraft)
                if lat is not None and lon is not None:
                    aircraft.lat = lat
                    aircraft.lon = lon

                self.context.notify(aircraft)

            print(
                msg, '%2d' % tc, icao,
                altitude,
                aircraft
            )

        if tc in TC_VELOCITY:
            velocity = pms.adsb.velocity(msg)
            aircraft = self.context.getAircraft(icao)

            if aircraft is not None:
                aircraft.messages.add(msg)
                aircraft.lastmessage = datetime.datetime.now()
                aircraft.speed, aircraft.heading, \
                aircraft.vspeed, aircraft.sptype = velocity

                self.context.notify(aircraft)

            print(
                msg, '%2d' % tc, icao,
                velocity,
                aircraft
            )

    def correct(self, msg):
        crc = pms.bin2int(pms.crc(msg))
        result = msg

        if crc != 0:
            msg_bin = pms.hex2bin(msg)
            for i in range(len(msg_bin) - 24):
                if msg_bin[i] == '0':
                    msg_bin = self.replace(msg_bin, i, '1')
                else:
                    msg_bin = self.replace(msg_bin, i, '0')

                patched_msg = hex(int(msg_bin, 2))[2:]
                if pms.bin2int(pms.crc(patched_msg)) == 0:
                    result = patched_msg
                    break

                if msg_bin[i] == '0':
                    msg_bin = self.replace(msg_bin, i, '1')
                else:
                    msg_bin = self.replace(msg_bin, i, '0')

        return result

    def replace(self, msg_bin, i, s):
        return msg_bin[:i] + s + msg_bin[i + 1:]
