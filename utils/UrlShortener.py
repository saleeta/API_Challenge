import base64
import hashlib
from .enumCollection import JsonKeys


class UrlShortener:
    url_dict = {}
    domain = """https://short.est/"""

    def __init__(self):
        self.urls_dict = self.url_dict
        self.domain = self.domain

    def shortener(self, url: str) -> str:
        # get md5 digest and encode the last 8 bytes with base 64 and remove trailing ='s and /
        md5_digest = hashlib.md5(url.encode()).digest()
        base_64 = base64.b64encode(md5_digest[-8:]).decode("UTF-8").replace("=", "").replace("/", "_")
        while base_64 in self.urls_dict and self.urls_dict.get(base_64) != url:

            incremented = int.from_bytes(md5_digest, 'big') + 1
            try:
                md5_digest = bytearray(incremented.to_bytes(len(md5_digest), 'big'))
                base_64 = base64.b64encode(md5_digest[-8:]).decode("UTF-8").replace("=", "").replace("/", "_")
            except OverflowError:
                # value won't fit into the payload, wrap round to 0
                md5_digest = bytearray(len(md5_digest))
                base_64 = base64.b64encode(md5_digest[-8:]).decode("UTF-8").replace("=", "").replace("/", "_")

        self.urls_dict[base_64] = url
        return base_64

    def encode(self, url: str) -> dict:

        if url in self.urls_dict.values():
            return {JsonKeys.code.value: self.domain + list(self.urls_dict.keys())[
                list(self.urls_dict.values()).index(url)]}
        else:
            code = self.shortener(url)
            return {JsonKeys.code.value: self.domain + code}

    def lookup(self, code: str) -> dict:

        if code in self.urls_dict:
            return {JsonKeys.url.value: self.urls_dict.get(code)}
        else:
            return {JsonKeys.error.value: "There is no such short link"}
