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
    """

    :return:
    """
    request_data = request.get_json(force=True)
    if "url" in request_data:
        url = request_data["url"]
        if validators.url(url):
            return json.dumps(url_shortener.encode(url))
        else:
            return json.dumps({"Error": "URL is not in the correct format"})
    else:
        return json.dumps({"Error": "Input is not in the correct format"})


@app.route('/api/decode', methods=['GET'])
def decoding() -> json:
    request_data = request.get_json(force=True)
    code = request_data.get('code')
    if code.startswith("""https://short.est/""") and validators.url(code):
        return json.dumps(url_shortener.lookup(code[18:]))
    else:
        return json.dumps({"Error": "Short URL is not in the correct format"})
