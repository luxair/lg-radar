import datetime


class Aircraft:
    def __init__(self, icao, callsign):
        now = datetime.datetime.now()
        self.icao = icao
        self.callsign = callsign
        self.messages = 1
        self.firstmessage = now
        self.lastmessage = now
        self.altitude = None
        self.speed = None
        self.heading = None
        self.vspeed = None
        self.sptype = None

    def getLatency(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.lastmessage

    def getAverageInterval(self) -> datetime.timedelta:
        return None if self.messages < 2 else \
            (self.lastmessage - self.firstmessage) / (self.messages - 1)

    def getTrackingStatus(self) -> bool:
        avg = self.getAverageInterval()
        lat = self.getLatency()

        if avg is None:
            return lat.total_seconds() < 120
        else:
            return lat < 10 * avg and lat.total_seconds() > 10

    def __str__(self):
        return 'Aircraft{icao=%s, callsign=%-8s}' % (self.icao, self.callsign)


class TrackingContext:
    def __init__(self):
        self.aircrafts = []

    def registerAircraft(self, icao: str, callsign: str) -> Aircraft:
        result = self.getAircraft(icao)

        if result == None:
            result = Aircraft(icao, callsign)
            self.aircrafts.insert(0, result)
            print('New registration: %s, Currently tracking %5d aircrafts'
                  % (result, len(self.aircrafts)))

        return result

    def getAircraft(self, icao: str) -> Aircraft:
        result = None

        for aircraft in self.aircrafts:
            if aircraft.icao == icao:
                result = aircraft

        return result
