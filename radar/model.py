import datetime


class Aircraft:
    def __init__(self, icao, callsign):
        self.icao = icao
        self.callsign = callsign
        self.messages = 1
        self.lastmessage = datetime.datetime.now()
        self.altitude = None
        self.speed = None
        self.heading = None
        self.vspeed = None
        self.sptype = None

    def getLatency(self):
        return datetime.datetime.now() - self.lastmessage

    def __str__(self):
        return 'Aircraft{icao=%s, callsign=%-8s}' % (self.icao, self.callsign)


class TrackingContext:
    def __init__(self):
        self.aircrafts = []

    def registerAircraft(self, icao: str, callsign: str) -> Aircraft:
        result = self.getAircraft(icao)

        if result == None:
            result = Aircraft(icao, callsign)
            self.aircrafts.append(result)
            print('New registration: %s, Currently tracking %5d aircrafts'
                  % (result, len(self.aircrafts)))

        return result

    def getAircraft(self, icao: str) -> Aircraft:
        result = None

        for aircraft in self.aircrafts:
            if aircraft.icao == icao:
                result = aircraft

        return result
