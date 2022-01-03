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
    from config import URL

    # put it in the environment variable
    global url

except Exception as e:
    print("Some Modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    # check for response 200 for to encode API
    def test_encode_index(self):
        payload = read_file(file_name='inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200, "The encode API is not functioning")

    # check output is JSON or dict for to encode API
    def test_encoder_json(self):
        payload = read_file(file_name='inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True, "The return value from encode API is not a JSON/Dictionary")

    # check for data returned for correct data for to encode API
    def test_encoder_data(self):
        payload = read_file(file_name='inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        response_dict = response.json()
        self.assertEqual(
            (JsonKeys.code.value in response_dict) and (validators.url(response_dict.get(JsonKeys.code.value))), True,
            "The return value from encode API is not in the correct JSON or URL format")

    # check for response 200 for to decode API
    def test_decode_index(self):
        payload = read_file(file_name='inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200, "The decode API is not functioning")

    # check output is JSON or dict for to decode API
    def test_decoder_json(self):
        payload = read_file(file_name='inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True, "The return value from decode API is not a JSON/Dictionary")

    # check for data returned for correct data type for to decode API
    def test_decoder_data(self):
        payload = read_file(file_name='inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        response_dict = response.json()
        self.assertEqual((JsonKeys.error.value in response_dict) or ((JsonKeys.url.value in response_dict) and
                                                                     (validators.url(
                                                                         response_dict.get(JsonKeys.url.value)))), True,
                         "The return value from decode API is not in the correct JSON or URL format")

    # E2E testing
    def test_e2e_testing(self):
        payload = read_file(file_name='inputEncode.json')
        response_encode = requests.post(url + "/api/encode", payload)
        response_decode = requests.post(url + "/api/decode", json.dumps(response_encode.json()))
        json_dict = json.loads(payload)
        self.assertEqual(json_dict.get(JsonKeys.url.value), response_decode.json().get(JsonKeys.url.value),
                         "End to End testing failed, url was not mapped correctly to the shortlink")


if __name__ == "__main__":
    url = URL.get("environment1")
    unittest.main()
