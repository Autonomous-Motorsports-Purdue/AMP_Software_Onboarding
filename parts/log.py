import datetime
import csv
class Logger():
    def __init__(self):
        # start_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
        # Writing to a csv file``
        self.csvfile = open("logger.csv", 'w', newline='')
        # Creating a csv writer object
        self.csvwriter = csv.writer(self.csvfile)

        fields = ['timestamp', 'object_x', 'object_y', 'contour_area']
        # Write fields
        self.csvwriter.writerow(fields)
    
    '''
    def run(self, object_x, object_y, contour_area):
        if object_x is not None and object_y is not None and contour_area is not None:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')
            row = [timestamp, object_x, object_y, contour_area]
            self.csvwriter.writerow(row)
    '''

    def run(self, lat, lon, alt, fix, corr_age):
        if lat is not None and lon is not None and alt is not None and fix is not None and corr_age is not None:
            print(f"lat: {lat}, lon: {lon}, alt: {alt}, fix: {fix}, corr_age: {corr_age}")

