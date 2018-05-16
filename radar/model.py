import datetime


class MessageEntry:
    def __init__(self, msg: str):
        self.timestamp = datetime.datetime.now()
        self.message = msg


class MessageHistory:
    def __init__(self):
        self.entries = []

    def add(self, message: str):
        self.entries.append(MessageEntry(message))

    def __len__(self):
        return len(self.entries)


class Aircraft:
    def __init__(self, icao, callsign):
        now = datetime.datetime.now()
        self.icao = icao
        self.callsign = callsign
        self.messages = MessageHistory()
        self.firstmessage = now
        self.lastmessage = now
        self.altitude = None
        self.lat = None
        self.lon = None
        self.speed = None
        self.heading = None
        self.vspeed = None
        self.sptype = None

    def getLatency(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.lastmessage

    def getAverageInterval(self) -> datetime.timedelta:
        msglen = len(self.messages)
        return None if msglen < 2 else \
            (self.lastmessage - self.firstmessage) / (msglen - 1)

    def getTrackingStatus(self) -> bool:
        avg = self.getAverageInterval()
        lat = self.getLatency()

        if avg is None:
            return lat.total_seconds() < 120
        else:
            return lat < 10 * avg or lat.total_seconds() < 10

    def __str__(self):
        return 'Aircraft{icao=%s, callsign=%-8s}' % (self.icao, self.callsign)


class TrackingObserver:

    def aircraft_updated(self, aircraft: Aircraft):
        pass


class TrackingContext:
    def __init__(self):
        self.aircrafts = []
        self.observers = []

    def addObserver(self, obs: TrackingObserver):
        self.observers.append(obs)

    def registerAircraft(self, icao: str, callsign: str) -> Aircraft:
        result = self.getAircraft(icao)
        result.callsign = callsign
        return result

    def getAircraft(self, icao: str) -> Aircraft:
        result = None

        for aircraft in self.aircrafts:
            if aircraft.icao == icao:
                result = aircraft

        if result is None:
            result = Aircraft(icao, '???')
            self.aircrafts.insert(0, result)

        return result

    def notify(self, aircraft: Aircraft):
        for obs in self.observers:
            obs.aircraft_updated(aircraft)
