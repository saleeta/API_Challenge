from flask import Flask, request
from URLShortener.UrlShortener import UrlShortener
import json
import validators
import base64
import hashlib

app = Flask(__name__)
url_shortener = UrlShortener()


@app.route('/')
def home() -> str:
    """[summary]

    Returns:
        str: [description]
    """
    return "App Works!!!"


@app.route('/api/encode', methods=['POST'])
def encoding() -> json:
    request_data = request.get_json(force=True)
    url = request_data['URL']
    if validators.url(url):
        return json.dumps(url_shortener.encode(url))
    else:
        return json.dumps({"Message": "URL is not in the correct format"})


@app.route('/api/decode', methods=['GET'])
def decoding() -> json:
    request_data = request.get_json(force=True)
    code = request_data['code']
    if code.startswith("""https://short.est/""") and validators.url(code):
        return json.dumps(url_shortener.lookup(code[18:]))
    else:
        return json.dumps({"Message": "Short URL is not in the correct format"})
