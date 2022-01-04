from flask import Flask, request
from utils.UrlShortener import UrlShortener
from utils.enumCollection import JsonKeys
import json
import validators

app = Flask(__name__)
url_shortener = UrlShortener()


@app.route('/')
def home() -> str:
    """Default route

        Returns:
            str: Returns "Hello World"
    """
    return "Hello World"


@app.route('/api/encode', methods=['POST'])
def encoding() -> str:
    """Receives a URL as an input in the JSON format for example
                {"url" : "https://foobar.withgoogle.com/"}

        Returns:
            str:  Returns the short link in JSON format
                  Returns errors in case in incorrect json format or incorrect URL format in JSON format
    """
    request_data = request.get_json(force=True)
    if JsonKeys.url.value in request_data:
        url = request_data[JsonKeys.url.value]
        if validators.url(value=url):
            return json.dumps(url_shortener.encode(url=url))
        else:
            return json.dumps({JsonKeys.error.value: "URL is not in the correct format"})
    else:
        return json.dumps({JsonKeys.error.value: "Input is not in the correct format"})


@app.route('/api/decode', methods=['POST'])
def decoding() -> str:
    """Receives a short link as an input in the JSON format for example
                {"ShortLink": "https://short.est/ZQw6Y5rSEEk"}

        Returns:
            str: Returns the mapped URL in JSON format
                  Returns errors in case in incorrect json format or incorrect short link format in JSON format
    """
    request_data = request.get_json(force=True)
    code = request_data.get(JsonKeys.code.value)

    if code.startswith("""https://short.est/""") and validators.url(value=code):
        return json.dumps(url_shortener.lookup(code=code[18:]))
    else:
        return json.dumps({JsonKeys.error.value: "Short URL is not in the correct format"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
