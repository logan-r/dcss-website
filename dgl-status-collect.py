#!/usr/bin/python

"""Collect dgl-status files from every server and write them to a local 'dgl-status' file.

Intended to be run every few minutes from cron."""

import json
import sys
import urllib2

if len(sys.argv) != 3:
    print 'error: incorrect number of arguments'
    print 'usage: %s servers.json outfile' % sys.argv[0]
    print 'eg: %s /var/www/servers.json /var/www/dgl-status.json' % sys.argv[0]
    sys.exit(1)

OUTFILE = sys.argv[2]
SERVERS = json.load(open(sys.argv[1], 'r'))

games = []

for server in SERVERS:
    if 'dgl-status' not in server:
        continue
    url = server['dgl-status']
    if not url: 
        continue
    response = urllib2.urlopen(url)
    if response.getcode() != 200:
        print "Warning: %s returned status code %s, skipping." % (url, response.getcode())
    for line in response.read().splitlines():
        if not 3 < line.count('#') < 7:
            print "Warning: ignoring line '%s' from %s (doesn't have 4-6 # characters)" % (line, url)
            continue
        split = line.split('#')
        game = {}
        game['name'] = split[0]
        game['rawversion'] = split[1]
        if 'trunk' in split[1] or 'git' in split[1]:
            game['version'] = 'Trunk'
        elif '-' in split[1]:
            game['version'] = split[1].split('-', 1)[1]
        if split[2]:
            game['XL'] = split[2].split(',')[0].split(' ')[0][1:]
            game['species'] = split[2].split(' ')[1][:-1][:2]
            game['background'] = split[2].split(' ')[1][:-1][-2:]
            game['location'] = split[2].split(', ')[1]
        game['termwidth'], game['termheight'] = split[3].split('x')
        game['idle'] = split[4]
        game['viewers'] = split[5]
        games.append(game)

# compact dump format
json.dump(games, open(OUTFILE, 'w'), separators=(',', ':'))
