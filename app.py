from flask import Flask, request
from utils.UrlShortener import UrlShortener
from utils.enumCollection import JsonKeys
import json
import validators

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
    if JsonKeys.url.value in request_data:
        url = request_data[JsonKeys.url.value]
        if validators.url(url):
            return json.dumps(url_shortener.encode(url))
        else:
            return json.dumps({JsonKeys.error.value: "URL is not in the correct format"})
    else:
        return json.dumps({JsonKeys.error.value: "Input is not in the correct format"})


@app.route('/api/decode', methods=['POST'])
def decoding() -> json:
    request_data = request.get_json(force=True)
    code = request_data.get(JsonKeys.code.value)

    if code.startswith("""https://short.est/""") and validators.url(code):
        return json.dumps(url_shortener.lookup(code[18:]))
    else:
        return json.dumps({JsonKeys.error.value: "Short URL is not in the correct format"})
