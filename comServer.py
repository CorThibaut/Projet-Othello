import sys
import socket
import json

serverAddress=('localhost',3000)

def SendToServer(port, req):
    s = socket.socket()
    s.bind(('localhost', port))
    s.connect(serverAddress)
    req = json.dumps(req).encode('utf8')
    s.send(req)
    print(type(port),"1")

def Identity():
    MyPort = 3088
    MyName = "Co"
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('name='):
            MyName = arg[len('name='):]
        else:
            MyPort = int(arg)
            #print(type(MyPort))
    return MyPort, MyName

def Subscribe(MyPort,MyName):
    req = {
        "request": "subscribe",
        "port": MyPort,
        "name": MyName,
        "matricules": ["195038","123456"]
    }
    SendToServer(MyPort, req)

def ProcessRequest(request, client, port):
    if request["request"]=="ping":
        response = {"response": "pong"}
        req= json.dumps(response).encode('utf8')
        client.send(req)
        return False
    return True

def ListenRequest(port):
    while True:
        finished=False
        request = ""
        print(type(port),"2")
        with socket.socket() as a:
            a.bind(('localhost',port))
            a.listen()
            while not finished:
                client, address = a.accept()
                request = json.loads(client.recv(4096).decode('utf8'))
                print(request)
                finished = ProcessRequest(request, client, port)

def start(MyPort,MyName):
    Subscribe(MyPort, MyName)
    ListenRequest(MyPort)
