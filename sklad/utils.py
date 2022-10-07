import base64

SOLT = 'DF'


def decode(code):
    return base64.b64decode(bytes.fromhex(code)).decode().replace(SOLT, '')


def encode(document_id):
    return base64.b64encode(f'{document_id}{SOLT}'.encode()).hex().upper()
