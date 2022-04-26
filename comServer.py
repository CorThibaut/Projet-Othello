import sys
import socket
import json
import random
#from othello import next

serverAddress=('127.0.0.1',3000)


def SendToServer(port, req):
    s = socket.socket()
    s.bind(('localhost', port))
    s.connect(serverAddress)
    req = json.dumps(req).encode('utf8')
    s.send(req)

def Identity():
    myPort = 3088
    myName = "Co"
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('name='):
            myName = arg[len('name='):]
        else:
            myPort = int(arg)
    return myPort, myName

def subscribe(myPort,myName):
    req = {
        "request": "subscribe",
        "port": myPort,
        "name": myName,
        "matricules": ["195038","123456"]
    }
    SendToServer(myPort, req)

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
        reque = ""
        with socket.socket() as s:
            s.bind(('localhost', port))
            s.listen()
            while not finished:
                client, address = s.accept()
                request = json.loads(client.recv(4096).decode('utf8'))
                print(request)
                finished = ProcessRequest(request, client, port)


def start(myName,myPort):
    subscribe(myName, myPort)
    ListenRequest(myPort)
