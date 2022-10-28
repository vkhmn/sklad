from base64 import b64encode, b64decode
from io import BytesIO
from os import getenv

from django.urls import reverse_lazy
from config.settings import BASE_URL
from qrcode import make


SOLT = getenv('SOLT')


def decode(code):
    try:
        return b64decode(bytes.fromhex(code)).decode().replace(SOLT, '')
    except ValueError:
        return None


def encode(document_id):
    return b64encode(f'{document_id}{SOLT}'.encode()).hex().upper()


def get_confirm_url(document_id):
    url = reverse_lazy('document_confirm')
    code = encode(document_id)
    return f'{BASE_URL}{url}?code={code}'


def make_qrcode(document_id):
    confirm_url = get_confirm_url(document_id)
    img = make(confirm_url)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, 'png')
    res = img_byte_arr.getvalue()
    return b64encode(res).decode('ascii')
