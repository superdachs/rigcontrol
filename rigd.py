#/usr/bin/env python3

# daemon for controling the rig

from time import import sleep
from daemonize import import Daemonize
import os
import sys
import logging
import datetime

app = "rigd"
pdir = os.path.join('tmp', app)
pid = os.path.join(pdir, "%s.pid" % app)
if not os.path.exists("var/log"):
    os.makedirs("var/log")
if not os.path.exists("tmp/%s" % app):
    os.makedirs("tmp/%s" % app)

logger = logging.getLogger(app)
logger.setLevel(logging.DEBUG)
logger.propagate = False
logfile = logging.FileHandler("var/log/%s.log" % app, "a")
logfile.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(message)s")
logfile.setFormatter(formatter)
logger.addHandler(logfile)

keep_fds = [logfile.stream.fileno()]

def setup_camera():
    pass

def main():
    while True:
        sleep(5)

daemon = Daemonize(app=app, pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
