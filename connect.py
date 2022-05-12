import sys
import socket
import json
from IA_Game import next

serverAddress=('localhost',3000)  #adresse du serveur

def Id():                         # permet de changer le nom, port et matricule en ajoutant des arguments à la commande pour lancé les communications avec le serveur
    MyPort = 3088            #valeur par défaut
    MyName = "Co"            #valeur par défaut
    MyMatricule = "195038"   #valeur par défaut
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('name='):
            MyName = arg[len('name='):]
        elif arg.startswith('matricule='):
            MyMatricule = arg[len('matricule='):]
        else:
            MyPort = int(arg)
    return MyPort, MyName, MyMatricule

def SendToServer(port, req):    # envoi les requetes aux serveur     
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.connect(serverAddress)
    req = json.dumps(req).encode('utf8')
    s.send(req)

def Subscribe(MyPort,MyName,MyMatricules):   # requete speciale pour se connecter au serveur
    req = {
        "request": "subscribe",
        "port": MyPort,
        "name": MyName,
        "matricules": [MyMatricules]
    }
    SendToServer(MyPort, req)

def ListenRequest(port):              # ecoute les requetes du serveur
    while True:
        finished=False
        request = ""
        with socket.socket() as a:
            a.bind(('0.0.0.0',port))
            a.listen()
            while not finished:
                client, address = a.accept()
                request = json.loads(client.recv(4096).decode('utf8'))
                print(request)
                finished = ProcessRequest(request, client, port)

def ProcessRequest(request, client, port):    # traite les requetes du serveur
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

def start(MyPort,MyName, MyMatricules):          # lance le programme
    Subscribe(MyPort, MyName , MyMatricules)
    ListenRequest(MyPort)

if __name__ == "__main__":
    start(*Id())
