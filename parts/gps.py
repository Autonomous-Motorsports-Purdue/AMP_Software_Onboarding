#!/usr/bin/env python3
"""
GNSS receiver part for Donkeycar.

This part starts the pygnssutils GNSS reader and NTRIP client once, then
returns the latest parsed GGA fix without blocking the vehicle loop.
"""

from queue import Empty, Queue
from threading import Event, Lock
from time import sleep

from serial import Serial

from pygnssutils.globals import FORMAT_PARSED
from pygnssutils.gnssntripclient import GNSSNTRIPClient
from pygnssutils.gnssstreamer import GNSSStreamer
from pygnssutils.helpers import parse_url


class GPS:
    def __init__(self):
        # Receiver configuration.
        self.serial_port = "COM7"
        self.baudrate = 9600
        self.timeout = 3

        # NTRIP configuration.
        self.ntrip_url = "108.59.49.226:9000/MSM4_NEAR"
        self.ntrip_user = "automp1"
        self.ntrip_password = "automp1"
        self.gga_interval = 1 # number of seconds between sending messages back up to NTRIP.
        self.msg_filter = "GNGGA"

        if not self.ntrip_url.startswith("http"):
            self.ntrip_url = f"http://{self.ntrip_url}"

        protocol, hostname, port, mountpoint = parse_url(self.ntrip_url)
        self.ntrip_settings = {
            "server": hostname,
            "port": port,
            "https": 1 if protocol == "https" else 0,
            "mountpoint": mountpoint,
            "ntripuser": self.ntrip_user,
            "ntrippassword": self.ntrip_password,
            "version": "2.0",
            "ggamode": 0,
            "ggainterval": self.gga_interval,
            "datatype": "RTCM",
        }

        self.gnss_queue = Queue()
        self.stop_event = Event()
        self.lock = Lock()
        self.started = False
        self.ser = None
        self.gnss = None
        self.ntrip = None
        self.latest_output = (None, None, None, None, None, None, None)

    def _start_streams(self):
        with self.lock:
            if self.started:
                return

            self.ser = Serial(self.serial_port, self.baudrate, timeout=self.timeout)
            self.gnss = GNSSStreamer(
                self,
                self.ser,
                outformat=FORMAT_PARSED,
                validate=1,
                msgmode=0,
                parsebitfield=1,
                quitonerror=1,
                protfilter=7,
                msgfilter=self.msg_filter,
                limit=0,
                outqueue=self.gnss_queue,
                stopevent=self.stop_event,
            )
            self.ntrip = GNSSNTRIPClient(self)

            self.gnss.run()
            self.ntrip.run(
                **self.ntrip_settings,
                output=self.ser,
                stopevent=self.stop_event,
            )
            self.started = True

    def get_coordinates(self):
        if self.gnss is None:
            return {
                "lat": 0.0,
                "lon": 0.0,
                "alt": 0.0,
                "sep": 0.0,
                "sip": 0,
                "fix": "NO FIX",
                "hdop": 0.0,
                "diffage": 0,
                "diffstation": 0,
            }

        status = self.gnss.get_coordinates()
        return {
            "lat": status.get("lat", 0.0),
            "lon": status.get("lon", 0.0),
            "alt": status.get("alt", 0.0),
            "sep": status.get("sep", 0.0),
            "sip": status.get("sip", 0),
            "fix": status.get("fix", "NO FIX"),
            "hdop": status.get("hdop", status.get("HDOP", status.get("hDOP", 0.0))),
            "diffage": status.get("diffage", status.get("diffAge", 0)),
            "diffstation": status.get("diffstation", status.get("diffStation", 0)),
        }

    def _drain_gnss_queue(self):
        if self.gnss is None:
            return

        while True:
            try:
                data = self.gnss_queue.get_nowait()
            except Empty:
                break

            if not hasattr(data, "identity"):
                continue

            status = self.get_coordinates()
            with self.lock:
                self.latest_output = (
                    getattr(data, "lat", status.get("lat")),
                    getattr(data, "lon", status.get("lon")),
                    getattr(data, "alt", status.get("alt")),
                    status.get("fix"),
                    getattr(data, "diffAge", status.get("diffage")),
                    getattr(data, "HDOP", getattr(data, "hDOP", status.get("hdop"))),
                    getattr(data, "numSV", status.get("sip")),
                )

    def run(self):
        self._start_streams()
        self._drain_gnss_queue()
        with self.lock:
            return self.latest_output

    def update(self):
        self._start_streams()
        while not self.stop_event.is_set():
            self._drain_gnss_queue()
            sleep(0.05)

    def run_threaded(self):
        self._drain_gnss_queue()
        with self.lock:
            return self.latest_output

    def shutdown(self):
        self.stop_event.set()

        if self.ntrip is not None:
            self.ntrip.stop()

        if self.gnss is not None:
            self.gnss.stop()

        if self.ser is not None and self.ser.is_open:
            self.ser.close()

        with self.lock:
            self.started = False
