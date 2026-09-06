import datetime
import csv
class Logger():
    def __init__(self):
        # Open and create a file object
        self.csvfile = open("logger.csv", 'w', newline='')
        # Create a csv writer object
        self.csvwriter = csv.writer(self.csvfile)

        # Create fields for CSV
        fields = ['timestamp', 'object_x', 'object_y', 'contour_area']
        # Write fields to CSV
        self.csvwriter.writerow(fields)

    def run(self, object_x, object_y, contour_area):
        # Check that input parameters are not None
        if object_x is not None and object_y is not None and contour_area is not None:
            # Get current timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')
            # Create a row containing the parameters as a list
            row = [timestamp, object_x, object_y, contour_area]
            # Write the row to the csv
            self.csvwriter.writerow(row)