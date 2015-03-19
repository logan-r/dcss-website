all:
	# Create dgl-status.json
	./dgl-status-collect.py -v _site/servers.json _site/dgl-status.json /tmp/dgl-status-collect.lock
	# Create feed.rss
	wget --no-check-certificate -O _site/feed.rss https://crawl.develz.org/wordpress/feed
	s3_website push
