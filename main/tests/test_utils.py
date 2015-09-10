# coding=utf-8
import base64
import hashlib
import hmac
import json

from unittest import TestCase

from main.utils import parse_signed_request


class TestParseSignedRequest(TestCase):
    def test_signed_request_return_data(self):
        data = {'user_id': '1231312'}
        signed_request = self._create_signed_request(data, 'app_secret')
        result = parse_signed_request(signed_request, 'app_secret')
        self.assertEquals(result, data)

    def test_signed_request_raises_error(self):
        data = {u'user_id': u'1231312'}
        signed_request = self._create_signed_request(data, 'wrong_secret')
        with self.assertRaises(ValueError):
            parse_signed_request(signed_request, 'app_secret')

    def test_signed_request(self):
        signed_request = ("yErzbIW652BnIfQ2C3arbQZWFu_NgH0vjLOCc6BeXus."
                          "eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3V"
                          "lZF9hdCI6MTQ0MTgxMjk1NiwidXNlciI6eyJjb3VudH"
                          "J5Ijoia3oiLCJsb2NhbGUiOiJydV9SVSJ9LCJ1c2VyX"
                          "2lkIjoiODE0MDcyNzE4NzEwODAxIn0")

        data = parse_signed_request(signed_request, "54ac91c2c49b39839f92dce0592eeba6")
        self.assertEquals(data['user_id'], '814072718710801')

    def _create_signed_request(self, data, app_secret):
        payload = json.dumps(data)
        encoded_data = base64.urlsafe_b64encode(payload)
        sig = hmac.new(app_secret, msg=encoded_data, digestmod=hashlib.sha256).digest()
        encoded_sig = base64.urlsafe_b64encode(sig)
        signed_request = '%s.%s' % (encoded_sig, encoded_data)
        return signed_request
