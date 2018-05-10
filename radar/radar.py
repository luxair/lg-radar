from adsb import AdsbThread
from model import TrackingContext
from server import RadarServer

if __name__ == '__main__':
    tracking_context = TrackingContext()

    adsb_thread = AdsbThread(tracking_context)
    adsb_thread.start()

    server = RadarServer(tracking_context)
    server.run()
