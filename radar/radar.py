from adsb import AdsbThread
from server import app

if __name__ == '__main__':
    adsb_thread = AdsbThread()
    adsb_thread.start()
    app.run()
