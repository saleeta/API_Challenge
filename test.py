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
    import sys
    from utils.enumCollection import JsonKeys

    # put it in the enviorment variable
    global url
    url = "http://localhost:5000"


except Exception as e:
    print("Some Modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # check for response 200

    def test_encode_index(self):
        payload = read_file('utils/input.json')
        response = requests.post(url + "/api/encode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check output is JSON or dict
    def test_encoder_json(self):
        payload = read_file('utils/input.json')
        response = requests.post(url + "/api/encode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True)

    # check for data returned for correct data
    def test_encoder_data(self):
        payload = read_file('utils/input.json')
        response = requests.post(url + "/api/encode", payload)
        response_dict = response.json()
        self.assertEqual((JsonKeys.code.value in response_dict) and (validators.url(response_dict.get(JsonKeys.code.value))), True)

    def test_decode_index(self):
        payload = read_file('utils/input.json')
        response = requests.post(url + "/api/decode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check output is JSON or dict
    def test_decoder_json(self):
        payload = read_file('utils/input.json')
        response = requests.post(url + "/api/decode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True)

    # check for data returned for correct data
    def test_decoder_data(self):
        payload = read_file('utils/input.json')
        response = requests.post(url + "/api/decode", payload)
        response_dict = response.json()
        self.assertEqual((JsonKeys.error.value in response_dict) or ((JsonKeys.url.value in response_dict) and
                                                               (validators.url(response_dict.get(JsonKeys.url.value)))), True,
                         "The data returned from decoder is in the incorrect format")


if __name__ == "__main__":
    unittest.main()
