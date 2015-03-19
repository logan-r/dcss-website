# DCSS Website Readme

This is the Dungeon Crawl Stone Soup landing page, intended to run on a
standalone domain as the "homepage" of DCSS. It's implemented as an
Amazon S3 bucket + Cloudfront distribution, which gives good global
performance at negligible cost.

The current AWS account maintainer is Alex "chequers" Jurkiewicz.

## System Requirements

* Python 2
* s3_website (`gem install s3_website`)

## Updating the live website

You need to update the website every few minutes, so spectator data is live.

* Change directory to the root of this repository.
* Add your AWS credentials to .env:
  ```
  S3_ID: xxx
  S3_SECRET: xxx
  ```
* Run `make`. This will take several minutes.

## Static content compression.

* *png*: Optionally perform a lossy compresion step with
  `pngquant 64 file.png` (64 = ncolours, tweak as neccessary), and always
  lossless compress with `advpng -z4 file.png`.
  Lossy compression is fantastic for DCSS screenshots and similar sprite
  images.
* *html, css, js, json, rss*: These files will be compressed by s3_website
  during upload, so don't worry about that.

