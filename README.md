# DCSS Website Readme

Currently visible at https://crawl.project357.org/static/dcss-web/index.htm

This is a small readme to describe what everything is for/how it works.

For background information, see the crawl-ref-discuss thread "Proposal: website visual refresh" from 24 Jan 2015.

## Static Content

Simple static web content:

* index.htm
* play.htm -- geolocates your closest server and redirects you to it
* download.htm -- information for offline downloads
* about.htm -- background information about DCSS
* splashimgs/ -- images that form the frontpage carousel
* bootstrap-\*/ -- bootstrap resources (css, js, fonts)
* servers.json -- static hardcoded list of DCSS servers
* feed.rss -- placeholder for the real Wordpress blog feed (during testing, the real URL is on another domain)

## Dynamic Content

* dgl-status-collect.py -- should be run from cron every few minutes to generate dgl-status, which is a user-accessible file

## Minification, compression & etc

All locally hosted css & js should be minified.

All locally hosted PNGs should be losslessly compressed with pngcrush/pngout and then likely lossy compressed with pngquant: `pngquant 64 img.png` will create a 64-colour dithered version of the image. This will generally reduce dcss screenshot size to a quarter of the original with minimal perceptual changes.
