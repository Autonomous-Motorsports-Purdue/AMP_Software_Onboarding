import time
import random

class Blocker():
    def __init__(self):
        # simulate a part doing something.
        pass

    def run(self):
        # block time is normal(0.25, 0.1) seconds
        t = max(random.normalvariate(0.25, 0.1), 0)
        print("Blocking for {:.2f} seconds...".format(t))
        time.sleep(t)
        print("Done blocking.")