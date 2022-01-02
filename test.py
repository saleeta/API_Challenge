try:
    import sys
    from app import app
    import unittest
    import json
    import os
    from unittest import TestCase
    from unittest.mock import patch
    from utils.file_reader import read_file
    import requests
    import validators
    from utils.enumCollection import JsonKeys

    # put it in the enviorment variable
    global url
    url = "http://localhost:5000"


except Exception as e:
    print("Some Modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # check for response 200

    def test_encode_index(self):
        payload = read_file('inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check output is JSON or dict
    def test_encoder_json(self):
        payload = read_file('inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True)

    # check for data returned for correct data
    def test_encoder_data(self):
        payload = read_file('inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        response_dict = response.json()
        self.assertEqual(
            (JsonKeys.code.value in response_dict) and (validators.url(response_dict.get(JsonKeys.code.value))), True)

    def test_decode_index(self):
        payload = read_file('inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check output is JSON or dict
    def test_decoder_json(self):
        payload = read_file('inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True)

    # check for data returned for correct data
    def test_decoder_data(self):
        payload = read_file('inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        response_dict = response.json()
        self.assertEqual((JsonKeys.error.value in response_dict) or ((JsonKeys.url.value in response_dict) and
                                                                     (validators.url(
                                                                         response_dict.get(JsonKeys.url.value)))), True,
                         "The data returned from decoder is in the incorrect format")

    # E2E testing
    def test_e2e_testing(self):
        payload = read_file('inputEncode.json')
        response_encode = requests.post(url + "/api/encode", payload)
        response_decode = requests.post(url + "/api/decode", json.dumps(response_encode.json()))
        json_dict= json.loads(payload)
        self.assertEqual(json_dict.get(JsonKeys.url.value), response_decode.json().get(JsonKeys.url.value),
                         "The data returned from decoder was not mapped correctly to the shortlink")


if __name__ == "__main__":
    unittest.main()
