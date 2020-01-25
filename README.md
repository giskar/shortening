URL shortening service======

test application `(python 3.8)`

### Endpoints
 - POST `/api/short_url/` Creates new short url
 - GET `/api/short_url/` Returns a set of all short urls that were created by you
 - GET `/api/short_url/<short_url_id>` Returns info about short url (only for author)
 - DELETE `/api/short_url/<short_url_id>` Deletes short url (only for author)
 - GET `/<short_id>/` Redirects to real url

#### How to start
1) `make init`
2) `make start`