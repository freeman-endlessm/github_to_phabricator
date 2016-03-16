#!/usr/bin/python

import os
import subprocess
import time

from config import *

def fetch_cached_json(suffix):
    path = CACHE_DIR + suffix.replace("/", "_")
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()
    return None

def write_cached_json(suffix, data):
    path = CACHE_DIR + suffix.replace("/", "_")
    with open(path, 'w') as f:
        f.write(data)

def rate_limited(headers):
    limited=False
    reset_time=None
    for line in headers:
        if line.find(": ") == -1:
            continue
        (h, v) = line.split(": ")
        if h == "X-RateLimit-Remaining":
            try:
                remaining = int(v)
            except ValueError:
                continue
            if remaining < 1:
                limited=True
        if h == "X-RateLimit-Reset":
            try:
                reset_time = int(v)
            except ValueError:
                continue
    if limited:
        print "Warning: Rate Limit Reached"
        print " X-RateLimit-Reset: %d"%(reset_time)
        now = int(time.time())
        print " Current Time: %d"%(now)
        secs=reset_time-now+1
        print " Sleep Seconds: %d"%(secs)
        if secs > 0:
            time.sleep(secs)
            return True

def fetch_json(suffix):
    cached = fetch_cached_json(suffix)
    if cached is None:
        url = BASE_URL + suffix

        process = subprocess.Popen(['curl', '-i', '-s', '-u', USERNAME + ":" + TOKEN, url],
                               stdout=subprocess.PIPE)
        result = process.communicate()[0]
        write_cached_json(suffix, result)
    else:
        result = cached
    (headers, payload) = result.split("\r\n\r\n", 1)
    if rate_limited(headers.split("\r\n")):
        return fetch_json(suffix)
    return (headers, payload)
