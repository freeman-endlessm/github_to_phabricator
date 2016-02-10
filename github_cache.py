#!/usr/bin/python

import os
import subprocess

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
    for line in headers:
        if line.find(": ") == -1:
            continue
        (h, v) = line.split(": ")
        if h == "X-RateLimit-Remaining":
            try:
                i = int(v)
            except ValueError:
                continue
            if i < 1:
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
        print "Warning: Rate Limit Reached, sleeping 30 seconds..."
        time.sleep(30)
        return fetch_json(suffix)
    return (headers, payload)
