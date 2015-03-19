#!/usr/bin/env node

var FeedParser = require('feedparser')
var request = require('request')
var cheerio = require('cheerio')
var fs = require('fs');

var req = request('https://crawl.develz.org/wordpress/feed');
var feedparser = new FeedParser({});

req.on('response', function (res) {
    var stream = this;
    if (res.statusCode != 200) return this.emit('error', new Error('Bad status code'));
    stream.pipe(feedparser);
});

items = [];
feedparser.on('readable', function() {
    var stream = this
        , item;

    while (item = stream.read()) {
        items.push(item);
    }
});

feedparser.on('end', function() {
    index = fs.readFileSync('_site/index.html', {encoding: 'utf8'});
    $ = cheerio.load(index);
    items.slice(0, 4).forEach(function(i) {
        link = i.link;
        title = i.title;
        $('#newsList').append("<li><a href=\"" + link + "\">" + title + "</a></li>");
    });
    fs.writeFileSync('_site/index.html', $.html());
});
