#!/usr/bin/python

"""Returns icecast metadata from a stream as a JSON object.
   Optionally posts it to a url."""

import socket
import json
import urllib3
import getopt
import sys


def usage ():
    print("""usage:
    -h host to get metadata from
    -m mount to get metadata from
    [-f to get full header metadata]
    [-p port to get metadata from (default 8000)]
    [-u url to post metadata to as json]""")

try:
    optlist, cmdline = getopt.getopt(sys.argv[1:],'h:p:m:u:f')
except getopt.GetoptError:
    sys.stderr.write("invalid options\n")
    usage()
    sys.exit(1)

# defaults
port = 8000

# check options
full_headers = False
for opt in optlist:
    if opt[0] == '-h':
        host=opt[1]
    if opt[0] == '-p':
        port=int(opt[1])
    if opt[0] == '-m':
        mount=opt[1]
    if opt[0] == '-u':
        posturl=opt[1]
    if opt[0] == '-f':
        full_headers = True

# required options
try:
    host
    port
    mount
except NameError:
    usage()
    sys.exit(1)


def get_data(host, port, mount):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((host, port))
    req ='GET %s HTTP/1.0\r\nHost: %s:%d\r\nUser-Agent: Ice Meta Fetcher\r\nConnection: close\r\nIcy-Metadata: 1\r\n\r\n' % (mount, host, port)
    req = req.encode('utf-8')
    s.sendall(req)
    data = s.recv(1024).decode('utf-8', 'ignore')
    s.close()
    pdata = dict()
    if full_headers:
        pdata = dict([d.split(':',1) for d in data.split('\r\n') if d.count(":")])
    else:
        pdata = dict([d.split(':',1) for d in data.split('\r\n') if d.count("icy")])
    return  json.dumps(pdata)

jdata = get_data(host, port, mount)
#skip empty crap
if jdata:
    print(jdata)

try:
    # this post is optional
    req = urllib3.request(posturl, data=jdata, headers={
        'Content-Type': 'application/json',
        'Referer': 'http://%s' % (host)})
    r = urllib2.urlopen(req)
except NameError:
    pass

