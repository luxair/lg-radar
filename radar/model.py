class Aircraft:
    def __init__(self, icao, callsign):
        self.icao = icao
        self.callsign = callsign

    def __str__(self):
        return 'Aircraft{icao=%s, callsign=%-8s}' % (self.icao, self.callsign)


class TrackingContext:
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
