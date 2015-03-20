# These are the shortcuts users should use
all : | clean site
quick : | clean quicksite

.PHONY: clean site quicksite
site:
	# Create temp deploy copy
	cp -r site _site
	# Create dgl-status.json
	build-scripts/dgl-status-collect.py -v _site/servers.json _site/dgl-status.json /tmp/dgl-status-collect.lock
	# Load news into index
	build-scripts/fetch-feed.js
	# Minify, etc
	grunt
	# Upload to s3 / invalidate CF
	s3_website push

# for development, skip slow steps
quicksite:
	cp -r site _site
	build-scripts/fetch-feed.js
	grunt
	s3_website push

clean:
	rm -rf _site
