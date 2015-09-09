# coding=utf-8
import base64
import hashlib
import hmac
import json


def parse_signed_request(signed_request, app_secret):
    encoded_sig, payload = signed_request.split('.', 2)

    sig = base64.urlsafe_b64decode(encoded_sig)
    data = base64.urlsafe_b64decode(payload)

    data = json.loads(data)
    expected_sig = hmac.new(app_secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        raise ValueError("Bad Signed JSON signature!")
    else:
        return data
