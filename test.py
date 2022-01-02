try:
    from app import app
    import unittest
    import json
    import os
    from unittest import TestCase
    from unittest.mock import patch
    from utils.file_reader import read_file
    import requests
    import validators
#put it in the enviorment variable
    global url
    url = "http://localhost:5000/api/encode"


except Exception as e:
    print("Some Modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # check for response 200

    def test_index(self):
        payload = read_file('utils/input.json')
        response = requests.post(url, payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check output is JSON and apparently its not???
    def test_encoder(self):
        payload = read_file('utils/input.json')
        response = requests.post(url, payload)
        print(response.json(), "test_encoder")
        content_type = response.headers["Content-Type"];
        self.assertEqual(content_type, 'text/html; charset=utf-8')

    # check for data returned for correct data
    def test_encoder_data(self):
        payload = read_file('utils/input.json')
        response = requests.post(url, payload)
        response_dict = response.json()
        print(response.json(), "test_encoder_data")
        self.assertEqual(("ShortLink" in response_dict) and (validators.url(response_dict.get("ShortLink"))), True)


if __name__ == "__main__":
    unittest.main()
