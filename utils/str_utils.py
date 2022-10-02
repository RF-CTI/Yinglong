import base64


def encodeBase64(content: str) -> str:
    b64_byt = base64.b64encode(content.encode('utf-8'))
    return b64_byt.decode('utf-8')
