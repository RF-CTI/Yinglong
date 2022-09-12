def getIp(domain):
    import socket
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    print(myaddr)


def commonQueryOrder(ModelName, ItemName, Limit):
    return ModelName.query.order_by(ItemName.desc()).limit(Limit).all()


def commonQueryCompare(ModelName, ItemName, Limit, _type):
    if _type == '>':
        return ModelName.query.filter(ItemName >= Limit).all()
    elif _type == '<':
        return ModelName.query.filter(ItemName <= Limit).all()
    elif _type == '==':
        return ModelName.query.filter(ItemName == Limit).all()


if __name__ == "__main__":
    getIp('wcp.cscxas.com')
