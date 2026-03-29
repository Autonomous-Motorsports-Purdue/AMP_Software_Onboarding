import time
class Printer():
    def __init__(self):
        pass

    def run(self, lat, lon, alt, fix, corr_age, hdop, sat_count):
        if (
            lat is not None
            and lon is not None
            and alt is not None
            and fix is not None
            and corr_age is not None
            and hdop is not None
            and sat_count is not None
        ):
            print(
                "[Printer()]: "
                f"lat: {lat}, lon: {lon}, alt: {alt}, "
                f"fix: {fix}, corr_age: {corr_age}, hdop: {hdop}, sats: {sat_count}"
            )
        else:
            print("No GPS data available")
