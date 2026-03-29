
class Printer():
    def __init__(self):
        pass

    def run(self, lat, lon, alt, fix, corr_age):
        if lat is not None and lon is not None and alt is not None and fix is not None and corr_age is not None:
            print(f"lat: {lat}, lon: {lon}, alt: {alt}, fix: {fix}, corr_age: {corr_age}")
        else:
            print("No GPS data available")

