#!/usr/bin/python

"""Collect dgl-status files from every server and write them to a local 'dgl-status' file.

Intended to be run every few minutes from cron."""

import json
import sys
import urllib2

if len(sys.argv) != 3:
    print 'error: incorrect number of arguments'
    print 'usage: %s servers.json outfile' % sys.argv[0]
    print 'eg: %s /var/www/servers.json /var/www/dgl-status' % sys.argv[0]
    sys.exit(1)

LOCAL_FILE = sys.argv[2]
REMOTE_URLS = (s.get('dgl-status') for s in json.load(open(sys.argv[1], 'r')))

content = ''

for url in REMOTE_URLS:
    if not url: 
        continue
    response = urllib2.urlopen(url)
    if response.getcode() != 200:
        print "Warning: %s returned status code %s, skipping." % (url, response.getcode())
    content += response.read()

with open(LOCAL_FILE, 'w') as f:
    f.write(content)
