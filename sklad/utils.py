import base64

SOLT = 'DF'


def decode(code):
    try:
        return base64.b64decode(bytes.fromhex(code)).decode().replace(SOLT, '')
    except ValueError:
        return None


def encode(document_id):
    return base64.b64encode(f'{document_id}{SOLT}'.encode()).hex().upper()
