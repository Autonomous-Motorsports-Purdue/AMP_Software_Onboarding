#!/usr/bin/env python3
"""
GNSS Streamer Python Script
Equivalent to the gnssstreamer CLI command with NTRIP input and custom output handler.

This script:
1. Connects to a serial GNSS receiver on COM5
2. Sets up an NTRIP client to receive RTCM corrections
3. Filters for GNGGA messages
4. Outputs parsed position data with fix status and correction age
"""

from queue import Queue
from threading import Event, Thread, Lock
from time import sleep, perf_counter
from serial import Serial

from pygnssutils.gnssstreamer import GNSSStreamer
from pygnssutils.gnssntripclient import GNSSNTRIPClient
from pygnssutils.helpers import parse_url
from pygnssutils.globals import (
    CLIAPP,
    FORMAT_PARSED,
    ENCODE_NONE,
)

class GPS:
    def __init__(self):
        """
        Initialize GPS with threading support for donkeycar.
        """
        # Configuration parameters (matching the CLI command)
        self.serial_port = "COM7"
        self.baudrate = 9600
        self.timeout = 3

        # NTRIP configuration
        self.ntrip_url = "108.59.49.226:9000/MSM4_NEAR"
        self.ntrip_user = "automp1"
        self.ntrip_password = "automp1"
        self.gga_interval = 10  # Send GGA to NTRIP server every 10 seconds
        msg_filter = "GNGGA"

        # Message filtering - only process GNGGA messages
        self.msg_filter = "GNGGA"

        if not self.ntrip_url.startswith('http'):
            self.ntrip_url = f'http://{self.ntrip_url}'
    
        prot, hostname, port, mountpoint = parse_url(self.ntrip_url)
        https = 1 if prot == "https" else 0

        self.out_queue = Queue()
        self.stop_event = Event()

        streamer_kwargs = {
                'format': FORMAT_PARSED,  # Parse messages to objects
                'validate': 1,  # Validate checksums
                'msgmode': 0,  # GET mode
                'parsebitfield': 1,  # Parse UBX bitfields
                'encoding': ENCODE_NONE,  # No encoding
                'quitonerror': 1,  # Log errors and continue
                'protfilter': 7,  # NMEA + UBX + RTCM3 (1+2+4)
                'msgfilter': msg_filter,  # Filter for GNGGA messages
                'limit': 0,  # No message limit
                'outqueue': self.out_queue
            }
        
        self.ntrip_kwargs = {
            "server": hostname,
            "port": port,
            "https": https,
            "mountpoint": mountpoint,
            "ntrip_user": self.ntrip_user,
            "ntrip_password": self.ntrip_password,
            "version": "2.0",
            "ggamode": 0,
            "ggainterval": self.gga_interval,
            "datatype": "RTCM",
            "output": self.out_queue
        }
        
        self.ser = Serial(self.serial_port, self.baudrate, timeout=self.timeout)

        self.gnss = GNSSStreamer('DONKEY', 
                                 self.ser,
                                 **streamer_kwargs)
        self.ntrip = GNSSNTRIPClient("DONKEY", 
                                     **self.ntrip_kwargs)
        
        last_time = perf_counter()

    def update(self):
        self.gnss._read_loop(self.ser, 
                             stopevent=self.stop_event, 
                             outqueue=self.out_queue, 
                             inqueue=None, 
                             protfilter=7, 
                             kwargs=dict())
        self.ntrip._read_thread(settings=self.ntrip_kwargs, stopevent=self.stop_event, output=self.out_queue)
        self.gnss._outqueue.put("TEST")

    def run_threaded(self):
        if self.out_queue.empty():
            print("Queue empty")
            return None
        else:
            data = self.out_queue.get()
            dt = perf_counter() - last_time
            last_time = perf_counter()  
            print(f"dt = {last_time}")
            if data == "TEST":
                return None
            print(data)

            return data.lat, data.lon, data.alt, data.numSV, data.diffAge
