import base64
import hashlib
from .enumCollection import JsonKeys
import sys
sys.path.append('..')
from config import CONFIG


class UrlShortener:
    url_dict = {}
    domain = CONFIG.get("URL_PREFIX")

    def __init__(self):
        self.urls_dict = self.url_dict
        self.domain = self.domain

    def shortener(self, url: str) -> str:
        """ Gets the md5 digest and encodes the last 8 bytes with base 64. It then removes any trailing "=" and "/".
        In the case of collision 1 is added to the digest and the last 8 bytes are encoded with base 64 again and
        checked for collision In the case of overflow, wrap around to 0

                Args:
                    url (str): The long URL

                Returns:
                    str: Returns the base64 encoded string
        """
        md5_digest = hashlib.md5(url.encode()).digest()
        base_64 = base64.b64encode(s=md5_digest[-8:]).decode(encoding="UTF-8").replace("=", "").replace("/", "_")
        while base_64 in self.urls_dict and self.urls_dict.get(base_64) != url:

            incremented = int.from_bytes(md5_digest, 'big') + 1
            try:
                md5_digest = bytearray(incremented.to_bytes(len(md5_digest), 'big'))
                base_64 = base64.b64encode(md5_digest[-8:]).decode("UTF-8").replace("=", "").replace("/", "_")
            except OverflowError:
                md5_digest = bytearray(len(md5_digest))
                base_64 = base64.b64encode(md5_digest[-8:]).decode("UTF-8").replace("=", "").replace("/", "_")

        self.urls_dict[base_64] = url
        return base_64

    def encode(self, url: str) -> dict:
        """ Checks if the URL has been shortened before
                    If it has, the dictionary for URLs is scanned for the previously calculated short link
                    If not, the shortener function is called

                Args:
                    url (str): The long URL

                Returns:
                    dict: Returns a dictionary containing the short link
        """
        if url in self.urls_dict.values():
            return {JsonKeys.code.value: self.domain + list(self.urls_dict.keys())[
                list(self.urls_dict.values()).index(url)]}
        else:
            code = self.shortener(url=url)
            return {JsonKeys.code.value: self.domain + code}

    def lookup(self, code: str) -> dict:
        """ Checks if the short link exists in the dictionary for URLs


                Args:
                    code (str): The short link

                Returns:
                    dict: Returns a dictionary containing the URL
        """
        if code in self.urls_dict:
            return {JsonKeys.url.value: self.urls_dict.get(code)}
        else:
            return {JsonKeys.error.value: "There is no such short link"}
