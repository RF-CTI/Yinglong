def getIp(domain):
    import socket
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    print(myaddr)


if __name__ == "__main__":
    getIp('wcp.cscxas.com')
