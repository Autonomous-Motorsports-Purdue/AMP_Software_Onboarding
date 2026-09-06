import cv2

class Image_Publisher():
    def __init__(self):
        # Initialize cv2 VideoCapture
        self.cap = cv2.VideoCapture(0)
        self.frame = None

    def run(self):
        print("running")
        # Read from video capture
        ret, self.frame = self.cap.read()
        # Check if frame was returned
        if self.frame is not None:
            # cv2.imshow("Image", self.frame)
            # cv2.waitKey(1)
            # return Frame
            return self.frame