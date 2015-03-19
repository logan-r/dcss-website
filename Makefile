all:
	cp -r site _site
	# Create dgl-status.json
	./dgl-status-collect.py -v _site/servers.json _site/dgl-status.json /tmp/dgl-status-collect.lock
	# Create feed.rss
	wget --no-check-certificate -O _site/feed.rss https://crawl.develz.org/wordpress/feed
	grunt
	s3_website push

quick:
	s3_website push
