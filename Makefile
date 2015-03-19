all:
	# Create temp deploy copy
	cp -r site _site
	# Create dgl-status.json
	./dgl-status-collect.py -v _site/servers.json _site/dgl-status.json /tmp/dgl-status-collect.lock
	# Create feed.rss
	wget --no-check-certificate -O _site/feed.rss https://crawl.develz.org/wordpress/feed
	# Minify, etc
	grunt
	# Upload to s3 / invalidate CF
	s3_website push

# for development
quick:
	rm -rf _site
	cp -r site _site
	#grunt
	s3_website push

clean:
	rm -rf _site
