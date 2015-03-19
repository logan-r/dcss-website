# These are the shortcuts users should use
all : | clean site
quick : | clean quicksite

.PHONY: clean site quicksite
site:
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

# for development, skip external fetches
quicksite:
	cp -r site _site
	grunt
	s3_website push

clean:
	rm -rf _site
