try:
    import sys
    import unittest
    import json
    import os
    import requests
    import validators
    sys.path.append('..')

    from app import app
    from unittest import TestCase
    from unittest.mock import patch
    from utils.file_reader import read_file
    from utils.enumCollection import JsonKeys
    from config import CONFIG

    # put it in the environment variable
    global url

except Exception as e:
    print("Some Modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):

    def test_encode_index(self):
        """Checks for response 200 for to encode API
        """
        payload = read_file(file_name='../test/inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200, "The encode API is not functioning")

    def test_encoder_json(self):
        """Checks output is JSON or dict for to encode API
        """
        payload = read_file(file_name='../test/inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True, "The return value from encode API is not a JSON/Dictionary")

    def test_encoder_data(self):
        """Checks for data returned for correct data for to encode API
        """
        payload = read_file(file_name='../test/inputEncode.json')
        response = requests.post(url + "/api/encode", payload)
        response_dict = response.json()
        self.assertEqual(
            (JsonKeys.code.value in response_dict) and (validators.url(response_dict.get(JsonKeys.code.value))), True,
            "The return value from encode API is not in the correct JSON or URL format")

    def test_decode_index(self):
        """Checks for response 200 for to decode API
        """
        payload = read_file(file_name='../test/inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200, "The decode API is not functioning")

    def test_decoder_json(self):
        """Checks output is JSON or dict for to decode API
        """
        payload = read_file(file_name='../test/inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        try:
            response.json()
            json_test = True
        except ValueError:
            json_test = False
        self.assertEqual(json_test, True, "The return value from decode API is not a JSON/Dictionary")

    def test_decoder_data(self):
        """Checks for data returned for correct data type for to decode API
        """
        payload = read_file(file_name='../test/inputDecode.json')
        response = requests.post(url + "/api/decode", payload)
        response_dict = response.json()
        self.assertEqual((JsonKeys.error.value in response_dict) or ((JsonKeys.url.value in response_dict) and
                                                                     (validators.url(
                                                                         response_dict.get(JsonKeys.url.value)))), True,
                         "The return value from decode API is not in the correct JSON or URL format")

    def test_e2e_testing(self):
        """End-to-End testing
        """
        payload = read_file(file_name='../test/inputEncode.json')
        response_encode = requests.post(url + "/api/encode", payload)
        response_decode = requests.post(url + "/api/decode", json.dumps(response_encode.json()))
        json_dict = json.loads(payload)
        self.assertEqual(json_dict.get(JsonKeys.url.value), response_decode.json().get(JsonKeys.url.value),
                         "End to End testing failed, url was not mapped correctly to the shortlink")


if __name__ == "__main__":
    url = CONFIG.get("HOST")+":"+CONFIG.get("PORT")
    unittest.main()