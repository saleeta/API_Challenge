# URL Shortening API
## Getting started
This is a demo application for a URL shortening service. There are 2 endpoints `/encode` and `/decode`.
The shortening algorithm uses MD5 Hash to hash the url into a unique 128-bit hash value.
The last 8 bits are picked and encoded with base64 with the assumption that the probability of collisions in a 64^8 permutation space is small.
In the case of collision, linear probing is used by adding 1 to the 128-bit value and wrapping around in the case of an overflow.

This app relies on:

**FLASK** : A python micro web framework

##Configuration
You can modify the config.py file to configure url_shortener. The following variables can be tweaked:

>**HOST**: *Address at which the redis server lives, defaults to 127.0.0.1.*  
>**PORT**: *Port on which to contact redis, defaults to 6379.*  
>**URL PREFIX**: *URL scheme for your short url host.*

##Usage
The service can simply be started by deployments can be done via Docker:  

Building a docker image file: `docker build . -t doc-flask:v1`

Running a docker image file: `docker run -p 5000:5000 doc-flask:v1`


## Running tests
Tests can be run via  

`python -m test`

## Commands
The encode api can be called using 
`HOST:PORT/api/encode` and being passed a JSON value like:`{
  "url": "https://www.google.com/"
}`

The decode api can be called using 
`HOST:PORT/api/decode` and being passed a JSON value like:`{
  "ShortLink": "https://short.est/ZQw6Y5rSEEk"
}`

## Documentation
The sphinx generated documentation can be found int the main folder as an HTML.
