from base64 import b64encode, b64decode
from io import BytesIO
from qrcode import make

SOLT = 'DF'
ROOT_URL = 'http://127.0.0.1:8000/document/confirm/?code='


def decode(code):
    try:
        return b64decode(bytes.fromhex(code)).decode().replace(SOLT, '')
    except ValueError:
        return None


def encode(document_id):
    return b64encode(f'{document_id}{SOLT}'.encode()).hex().upper()


def get_confirm_url(document_id):
    code = encode(document_id)
    return f'{ROOT_URL}{code}'


def make_qrcode(document_id):
    url = get_confirm_url(document_id)
    img = make(url)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, 'png')
    res = img_byte_arr.getvalue()
    return b64encode(res).decode('ascii')
