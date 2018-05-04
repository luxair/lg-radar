import subprocess
import pyModeS as pms
from threading import Thread

class Aircraft:
    def __init__(self, icao, callsign):
        self.icao = icao
        self.callsign = callsign

    def __str__(self):
        return 'Aircraft{icao=%s, callsign=%-8s}' % (self.icao, self.callsign)

class AircraftInformation:
    def __init__(self):
        self.altitude

class Context:
    def __init__(self):
        self.aircrafts = {}

    def registerAircraft(self, icao, callsign):
        result = self.getAircraft(icao)

        if result == None:
            result = Aircraft(icao, callsign)
            self.aircrafts[result] = None
            print('New registration: %s, Currently tracking %5d aircrafts'
                    % (result, len(self.aircrafts)))

        return result

    def getAircraft(self, icao):
        result = None

        for aircraft in self.aircrafts.keys():
            if aircraft.icao == icao:
                result = aircraft

        return result


class AdsbThread(Thread):
    def __init__(self):
        super(AdsbThread, self).__init__()
        self.context = Context()

    def run(self):
        with subprocess.Popen(['rtl_adsb'], stdout=subprocess.PIPE) as adsb_flow:
            while True:
                msg = adsb_flow.stdout.readline()

                if len(msg) == 0:
                    break

                self.process_adsb(msg.decode('ascii').strip('*;\r\n'))


    def process_adsb(self, msg):
        if pms.bin2int(pms.crc(msg)) != 0:
            return

        tc = pms.adsb.typecode(msg)

        if tc in [1,2,3,4]:
            print(msg, '%2d' % tc, pms.adsb.icao(msg), pms.adsb.callsign(msg))
            self.context.registerAircraft(pms.adsb.icao(msg), pms.adsb.callsign(msg))

        if tc in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
            icao = pms.adsb.icao(msg)
            aircraft = self.context.getAircraft(icao)
            print(
                msg, '%2d' % tc, icao,
                pms.adsb.altitude(msg),
                aircraft
            )


