from base64 import b64encode
from io import BytesIO
from qrcode import make


def make_code(url):
    img = make(url)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, 'png')
    res = img_byte_arr.getvalue()
    return b64encode(res).decode('ascii')
