#!/usr/bin/python

"""Returns icecast metadata from a stream as a JSON object.
   Optionally posts it to a url."""

import socket
import json
import urllib2
import getopt
import sys


def usage ():
    print """usage:
    -h host to get metadata from
    -p port to get metadata from
    -m mount to get metadata from
    [-u url to post metadata to as json]"""

try:
    optlist, cmdline = getopt.getopt(sys.argv[1:],'h:p:m:u:')
except getopt.GetoptError:
    sys.stderr.write("invalid options\n")
    usage()
    sys.exit(1)

for opt in optlist:
    if opt[0] == '-h':
        host=opt[1]
    if opt[0] == '-p':
        port=int(opt[1])
    if opt[0] == '-m':
        mount=opt[1]
    if opt[0] == '-u':
        posturl=opt[1]

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
    s.sendall('GET %s HTTP/1.0\r\n'
              'Host: %s:%d\r\n'
              'User-Agent: Ice Meta Fetcher\r\n'
              'Connection: close\r\n'
              'Icy-Metadata: 1\r\n'
              '\r\n' % (mount, host, port))
    data = s.recv(1024).decode('utf-8', 'ignore').encode('utf-8')
    s.close()
    return dict([d.split(':',1) for d in  data.split('\r\n') if d.count("icy")])


#skip empty crap
pdata = get_data(host, port, mount)
if pdata.has_key("icy-br"):
    jdata = json.dumps(pdata)
    print jdata
    try:
        # this post is optional
        req = urllib2.Request(posturl, data=jdata, headers={'Content-Type': 'application/json',
                                                            'Referer': 'http://%s' % (host)})
        r = urllib2.urlopen(req)
    except NameError:
        pass

