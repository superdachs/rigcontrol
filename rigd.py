#!/usr/bin/env python3

# daemon for controling the rig

from time import sleep
from daemonize import Daemonize
import os
import sys
import logging
import datetime
import gphoto2 as gp

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

camera = None

def setup_camera():
    logger.debug("searching camera...")
    context = gp.Context()
    camera = gp.Camera()
    while True:
        try:
            camera.init(context)
        except gp.GPhoto2Error as e:
            if e.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                sleep(2)
                continue
            raise
        break
    abilities = gp.check_result(gp.gp_camera_get_abilities(camera))
    model = abilities.model
    logger.info("camera %s found." % model)
    

def main():
    setup_camera()
    while True:
        #TODO: check if camera is still present. if not reset and run setup again
        sleep(5)


daemon = Daemonize(app=app, pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
