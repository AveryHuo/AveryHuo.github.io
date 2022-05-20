---
title: Python Core Programming Note 2
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Python
tags: 
- Python
- Core Programming
- Note
---

## Net Programming

#### 1. TCP
+ Server:

```python
from socket import *
from time import ctime

HOST = ''
PORT = 21111
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSocket = socket(AF_INET, SOCK_STREAM)
tcpSerSocket.bind(ADDR)
tcpSerSocket.listen(5)

try:
    while True:
        print("waiting for connection...")
        tcpCliSocket, addr = tcpSerSocket.accept()
        print("connected from :",addr)
        while True:
            data = tcpCliSocket.recv(BUFSIZ)
            if not data:
                break
            print("rec:",data)
            send_str = '[%s] %s' %(bytes(ctime(), 'utf-8'), 'Oh?')
            tcpCliSocket.send(send_str.encode('utf-8'))
        tcpCliSocket.close()
except EOFError:
    print("Error: EOFEError")
except KeyboardInterrupt:
    print("Error: EOFEError")
finally:
    tcpSerSocket.close()
```

+ Client

```python
from socket import *

HOST = '127.0.0.1' 
PORT = 21111
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSocket = socket(AF_INET, SOCK_STREAM)
tcpCliSocket.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break

    tcpCliSocket.send(data.encode('utf-8'))
    data = tcpCliSocket.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))

tcpCliSocket.close()

```

#### 2. UDP

+ Server

```python
from socket import *
from time import ctime

HOST = ''
PORT = 21111
BUFSIZ = 1024
ADDR = (HOST, PORT)

udpSerSocket = socket(AF_INET, SOCK_DGRAM)
udpSerSocket.bind(ADDR)

try:
    while True:
        print("waiting for message...")
        msg, addr = udpSerSocket.recvfrom(BUFSIZ)
        if msg.decode('utf-8') == ' ':
            break
        print('Rev client:',msg)
        send_str = '[%s] %s' %(bytes(ctime(), 'utf-8'), msg)
        udpSerSocket.sendto(send_str.encode('utf-8'),addr)
        
except EOFError:
    print("Error: EOFEError")
except KeyboardInterrupt:
    print("Error: EOFEError")
finally:
    udpSerSocket.close()
```

+ Client

```python
from socket import *

HOST = '127.0.0.1' 
PORT = 21111
BUFSIZ = 1024
ADDR = (HOST, PORT)

udpCliSocket = socket(AF_INET, SOCK_DGRAM)
while True:
    data = input('> ')
    if not data:
        break

    udpCliSocket.sendto(data.encode('utf-8'),ADDR)
    if data == ' ':
        break
    data,ADDR = udpCliSocket.recvfrom(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))

udpCliSocket.close()
```

### 使用SocketServer
+ Server

```python
from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
from time import ctime


HOST = ''
PORT = 21111
BUFSIZ = 1024
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print("connected from..", self.client_address)
        send_str = '[%s] %s' %(bytes(ctime(), 'utf-8'), self.rfile.readline())
        self.wfile.write(send_str.encode('utf-8'))

tcpServ = TCP(ADDR, MyRequestHandler)
print("waiting for connection...")
tcpServ.serve_forever()
        
```

+ Client
不同之处：需要把建立和连接放在每次循环中

```
from socket import *

HOST = '127.0.0.1' 
PORT = 21111
BUFSIZ = 1024
ADDR = (HOST, PORT)



while True:
    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)
    data = input('> ')
    if not data:
        break

    send_data = "%s\n" % data
    tcpCliSocket.send(send_data.encode('utf-8'))
    data = tcpCliSocket.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))
    tcpCliSocket.close()

```
