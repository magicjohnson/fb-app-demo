# coding=utf-8
import base64
import hashlib
import hmac
import json


def base64_url_decode(data):
    data = data.encode(u'ascii')
    data += '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data)


def parse_signed_request(signed_request, app_secret):
    encoded_sig, payload = signed_request.split('.', 2)

    sig = base64_url_decode(encoded_sig)
    data = base64_url_decode(payload)

    data = json.loads(data)
    expected_sig = hmac.new(app_secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        raise ValueError("Bad Signed JSON signature!")

    return data
