ice-meta-fetcher
================

Fetches metadata from icecast stream, formats as json, and optionally posts it.

i.e.

```shell
  ice_meta_fetcher -h someradio.com -p 8000 -m /stream
```

Will return the JSON formatted stream data.

If you supply a -u argument, it'll POST that stream data to the url supplied.
