import time
from threading import Thread

import unicornhathd

from model import TrackingContext, Aircraft, TrackingObserver
from poi import center_coord, airport_coords


class HatThread(Thread, TrackingObserver):

    def __init__(self, context: TrackingContext):
        super(HatThread, self).__init__(daemon=False)
        self.blips = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.scanline = 0
        context.addObserver(self)

    def aircraft_updated(self, aircraft: Aircraft):
        if aircraft.lat is None or aircraft.lon is None:
            return
        coord = (aircraft.lat, aircraft.lon)

        scaled_coord = self.gps_to_matrix_coords(coord)

        if 0 <= scaled_coord[0] < 16 and 0 <= scaled_coord[1] < 16:
            self.blips[scaled_coord[1]][scaled_coord[0]] = 255

    def gps_to_matrix_coords(self, coord):
        zoom = 40
        rel_coord = (coord[0] - center_coord[0], coord[1] - center_coord[1])
        scaled_coord = (8 + int(zoom * rel_coord[0]), 8 + int(zoom * rel_coord[1]))
        return scaled_coord

    def run(self):
        while self.is_alive():
            unicornhathd.clear()

            for y in range(0, 16):
                for x in range(0, 16):
                    if y == self.scanline:
                        unicornhathd.set_pixel(x, y, 0, 0, 32)
                    if (y + 1) % 16 == self.scanline:
                        unicornhathd.set_pixel(x, y, 0, 0, 16)
                    if (y + 2) % 16 == self.scanline:
                        unicornhathd.set_pixel(x, y, 0, 0, 8)
                    if (y + 3) % 16 == self.scanline:
                        unicornhathd.set_pixel(x, y, 0, 0, 4)
                    if self.blips[x][y] > 0:
                        self.set_green(x, y, self.blips[x][y])
                        self.blips[x][y] -= 1

            for ac in airport_coords:
                c = self.gps_to_matrix_coords(ac)
                self.set_red(c[1], c[0], 128)

            ref = self.gps_to_matrix_coords(center_coord)
            self.set_red(ref[1], ref[0], 16)

            unicornhathd.show()

            self.scanline = (self.scanline + 1) % 16
            time.sleep(1.0)

    def set_green(self, x, y, g):
        p = unicornhathd.get_pixel(x, y)
        unicornhathd.set_pixel(x, y, p[0], g, p[2])

    def set_red(self, x, y, r):
        p = unicornhathd.get_pixel(x, y)
        unicornhathd.set_pixel(x, y, r, p[1], p[2])
