import socket


def checkAccount(URL, username, password):
    f = open(URL, 'r')
    data = f.read()
    f.close()
    list = data.split('\n')
    for i in list:
        temp = i.split(' ')
        if username == temp[0] and password == temp[1]:
            return True
    return False


def CTE(connection, myFile):
    file = open(myFile, 'rb')
    sizeChunk = 64 * 1024
    while True:
        chunk = file.read(sizeChunk)
        connection.send(bytes('%s\r\n' % hex(len(chunk))[2:], 'utf8'))
        chunk += bytes('\r\n', 'utf8')
        if len(chunk) == 2:
            break
        connection.send(chunk)
    connection.send(bytes('0\r\n\r\n', 'utf8'))
    file.close()


def startConnection():
    size = 1024
    while True:
        mySocket.listen(5)
        connection, address = mySocket.accept()
        request = connection.recv(size).decode('utf-8')
        list = request.split(' ')
        method = list[0]
        print('Client request:', request)

        if method == 'GET':
            myFile = list[1].lstrip('/')
            if myFile == '':
                myFile = 'index.html'
            try:
                fId = open(myFile, 'rb')
                response = fId.read()
                fId.close()
                header = 'HTTP/1.1 200 OK\n'
            except:
                f = open('404.html', 'rb')
                response = f.read()
                f.close()
                header = 'HTTP/1.1 404 Not Found\n'
            type = ''
            if myFile.endswith('html'):
                type = 'text/html'
            elif myFile.endswith('jpg'):
                type = 'image/jpg'
            elif myFile.endswith('png'):
                type = 'image/png'
            header += 'Content-Type:' + str(type) + '\n\n'

        elif method == 'POST':
            index1 = request.find('Username')
            index1 = index1 + len('Username=')
            index2 = request.find('&', index1)
            username = request[index1:index2]
            s = len('Password=') + 1
            password = request[(index2 + s):]

            if checkAccount(URL, username, password):
                myFile = 'info.html'
                fInfo = open('info.html', "rb")
                response = fInfo.read()
                fInfo.close()
                header = 'HTTP/1.1 301 Moved Permanently\n'
                header += 'Location: /info.html\n'

            else:
                myFile = '404.html'
                fErr = open('404.html', "rb")
                response = fErr.read()
                fErr.close()
                header = 'HTTP/1.1 301 Moved Permanently\n'
                header += 'Location: /404.html\n'

            header += 'Transfer-Encoding: chunked\n'
            print(header)
            connection.send(header.encode('utf-8') + response)
            CTE(connection, myFile)
            connection.close()
            continue

        finalResponse = header.encode('utf-8')
        finalResponse += response
        connection.send(finalResponse)
        connection.close()


URL = 'account.txt'
HOST, PORT = 'localhost', 8082
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mySocket.bind((HOST, PORT))
    print('Serving on port', PORT)
except:
    PORT2 = 9000
    print('Could not bind to port', PORT, '. We can change it to port ', PORT2)
    print('Serving on port', PORT2)
    mySocket.bind((HOST, PORT2))


if __name__ == "__main__":
    startConnection()
    mySocket.close()


