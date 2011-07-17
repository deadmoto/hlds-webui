#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import httpthread
import os
import subprocess
import time
import var


def checkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def getparameters():
    return "-game cstrike -console +map {0} +maxplayers 11 +port {1}".format(var.HLDS_MAP, var.HLDS_PORT)


def getpathtologs():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H-%M-%S")
    checkdir(os.path.join("logs", today))
    return  os.path.join("logs", today, now + ".txt")


def hlds_run():
    var.HLDS_ISRUNNING = True

    if (os.name == "nt"):
        hlds_run_nt()
    if (os.name == "posix"):
        hlds_run_posix()

    var.HLDS_ISRUNNING = False


def hlds_run_nt():
    args = (var.HLDS_PATH_NT + "hlds.exe", getparameters())
    pipe = open(getpathtologs(), "w")
    process = subprocess.Popen(args, cwd=var.HLDS_PATH_NT, stderr=pipe, stdin=pipe, stdout=pipe)
    while (var.HLDS_TIMELEFT > 0):
        if (process.poll() == None):
            var.HLDS_TIMELEFT = var.HLDS_TIMELEFT - 1
            time.sleep(1)
        else:
            var.HLDS_TIMELEFT = 0
    os.system("TASKKILL /F /T /PID {0}".format(process.pid))


def hlds_run_posix():
    args = (var.HLDS_PATH_POSIX + "hlds_run " + getparameters())
    print args
    #pipe = open(getpathtologs(), "w")
    pipe = subprocess.PIPE
    process = subprocess.Popen(args, shell=True, stderr=pipe, stdin=pipe, stdout=pipe)
    while (var.HLDS_TIMELEFT > 0):
        if (process.poll() == None):
            var.HLDS_TIMELEFT = var.HLDS_TIMELEFT - 1
            print var.HLDS_TIMELEFT
            time.sleep(1)
        else:
            var.HLDS_TIMELEFT = 0
    os.system("kill -9 {0}".format(process.pid))
    #os.system("killall hlds_run")
    #os.system("killall hlds_i686")

if __name__ == "__main__":
    httpd = httpthread.HTTPThread().start()
    while (True):
        if (var.HLDS_WAIT == True):
            var.HLDS_WAIT = False
            hlds_run()
        else:
            time.sleep(1)