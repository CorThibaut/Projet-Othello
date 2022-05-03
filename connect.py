import sys
import socket
import json
from IA_Game import next

serverAddress=('localhost',3000)

def Id():
    MyPort = 3088
    MyName = "Co"
    MyMatricule = "195038"
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('name='):
            MyName = arg[len('name='):]
        elif arg.startswith('matricule='):
            MyMatricule = arg[len('matricule='):]
        else:
            MyPort = int(arg)
    return MyPort, MyName, MyMatricule

def SendToServer(port, req):
    s = socket.socket()
    s.bind(('localhost', port))
    s.connect(serverAddress)
    req = json.dumps(req).encode('utf8')
    s.send(req)

def Subscribe(MyPort,MyName,MyMatricules):
    req = {
        "request": "subscribe",
        "port": MyPort,
        "name": MyName,
        "matricules": [MyMatricules]
    }
    SendToServer(MyPort, req)

def ListenRequest(port):
    while True:
        finished=False
        request = ""
        with socket.socket() as a:
            a.bind(('localhost',port))
            a.listen()
            while not finished:
                client, address = a.accept()
                request = json.loads(client.recv(4096).decode('utf8'))
                print(request)
                finished = ProcessRequest(request, client, port)

def ProcessRequest(request, client, port):
    if request["request"]=="ping":
        reponse = {"response": "pong"}
        req= json.dumps(reponse).encode('utf8')
        client.send(req)
        return False
    if request["request"] == "play":
        move = next(request["state"])
        message = "bip boop"
        reponse = {
            "response": "move",
            "move": move,
            "message": message
            }
        req = json.dumps(reponse).encode('utf8')
        client.send(req)
        return False
    return True

def start(MyPort,MyName, MyMatricules):
    Subscribe(MyPort, MyName , MyMatricules)
    ListenRequest(MyPort)

if __name__ == "__main__":
    start(*Id())
