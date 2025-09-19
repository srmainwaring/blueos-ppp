import logging
import subprocess
import time
import threading

from pathlib import Path

logger = logging.getLogger("pppd.settings")

PPPD_EXECUTABLE = Path("/ppp_ws/ppp/pppd/pppd")
# PPPD_EXECUTABLE = Path("/shortcuts/userdata/code/ppp_ws/ppp/pppd/pppd"),


class PPPDaemon:
    def __init__(self):
        # arguments
        self.device = "/dev/ttyS0"
        self.baudrate = "921699"
        self.local = "192.168.1.205"
        self.remote = "192.168.1.200"

        # signal whether to enable / disable / shutdown the daemon
        self.lock = threading.Lock()
        self.is_enabled = False
        self.do_shutdown = False

        # run subprocess in a thread to not block
        self.thread = threading.Thread(target=self.child_task)
        self.thread.start()

    def __del__(self):
        self.shutdown()

    def child_task(self):
        "Run pppd as a subprocess"

        args = [
            PPPD_EXECUTABLE,
            f"{self.device}",
            f"{self.baudrate}",
            f"{self.local}:{self.remote}",
            "debug",
            "noauth",
            "nodetach",
            "crtscts",
            "local",
            "proxyarp",
            "ktune",
        ]

        is_running = False
        do_shutdown = False
        pppd_process = None
        while not do_shutdown:
            with self.lock:
                is_enabled = self.is_enabled
                do_shutdown = self.do_shutdown

            if is_enabled and not is_running and pppd_process is None:
                # start proces
                pppd_process = subprocess.Popen(args)
                is_running = True
                print("PPP started")

            if not is_enabled and is_running and pppd_process is not None:
                pppd_process.terminate()
                time.sleep(1)
                pppd_process.poll()
                if pppd_process.returncode is None:
                    pppd_process.kill()
                    time.sleep(1)
                pppd_process = None
                is_running = False
                print("PPP stopped")

            # check if still alive
            if pppd_process is not None:
                pppd_process.poll()

            time.sleep(0.5)

    def start(self):
        """stop the PPP daemon"""
        with self.lock:
            self.is_enabled = True

    def stop(self):
        """start the PPP daemon"""
        with self.lock:
            self.is_enabled = False

    def shutdown(self):
        """enable clean shutdown"""
        with self.lock:
            self.is_enabled = False
            self.do_shutdown = True
        self.thread.join()
