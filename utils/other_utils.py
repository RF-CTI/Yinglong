import uuid
import sys
from hashlib import md5

def getNoNoneItem(content: list):
    if not all(content):
        return -1, None
    elif not any(content):
        for i, item in enumerate(content):
            if item is not None:
                return i, item
    else:
        return 0, content[0]

def generateSecret() -> str:
    return str(uuid.uuid1())


def getErrorMessage() -> str:
    return str(sys.exc_info())


def getMD5Code(content: str) -> str:
    return md5(content).hexdigest()


def generateMD5Code(ctype: int) -> str:
    __typedict__ = {
        1: uuid.uuid1,
        4: uuid.uuid4
    }
    return getMD5Code(str(__typedict__.get(ctype)()).encode('utf-8'))
