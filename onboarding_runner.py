import donkeycar.donkeycar as dk

from parts.image_publisher import Image_Publisher
from parts.image_cv import Object_Detection
from parts.log import Logger
from parts.gps import GPS
from parts.print import Printer

if __name__ == "__main__":
    V = dk.vehicle.Vehicle()
    print("starting")

    # V.add(Image_Publisher(), inputs=[], outputs=['image'])
    # V.add(Object_Detection(), inputs=['image'], outputs=['image_cv', 'object_x', 'object_y', 'contour_area'])
    # V.add(Logger(), inputs=['lat', 'lon', 'alt', 'fix', 'corr_age'], outputs=[])
    V.add(GPS(), inputs=[], outputs=['lat', 'lon', 'alt', 'fix', 'corr_age'], threaded=True)
    V.add(Printer(), inputs=['lat', 'lon', 'alt', 'fix', 'corr_age'], outputs=[])

    V.start(rate_hz=30)
    