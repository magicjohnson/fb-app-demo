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
        data = {'user_id': '1231312'}
        signed_request = self._create_signed_request(data, 'wrong_secret')
        with self.assertRaises(ValueError):
            parse_signed_request(signed_request, 'app_secret')

    def _create_signed_request(self, data, app_secret):
        payload = json.dumps(data)
        encoded_data = base64.urlsafe_b64encode(payload)
        sig = hmac.new(app_secret, msg=encoded_data, digestmod=hashlib.sha256).digest()
        encoded_sig = base64.urlsafe_b64encode(sig)
        signed_request = '%s.%s' % (encoded_sig, encoded_data)
        return signed_request
