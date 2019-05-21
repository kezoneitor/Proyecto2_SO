import socket
from threading import Thread

mySocket = socket.socket()
item = ""
ports = {}

def socketServer(ip):
    global mySocket
    host = ip
    port = 5000
    print("Open server in", ip)
    mySocket.bind((host,port))
    mySocket.listen(5)
    while True:
        conn, addr = mySocket.accept()
        print("Connection from: " + str(addr))
        if conn:
            p = Thread(target=socket, args=(conn, addr,))
            p.start()

def repartir(size):
    global item
    global ports
    part = size // len(ports)
    init = 0
    for key in ports.keys():
        ports[key][0] = [init, part]
        init += part + 1
    item = 'filtros'


def allFinish():
    global ports
    fin = True
    for key in ports.keys():
        if ports[key][1]:
            return False
    return fin

def socket(conn, addr):
    global item
    global ports
    ports[addr[1]] = [[], True]
    while True:
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            break
        if allFinish():
            item = ""
        if item == 'filtros':
            if ports[addr[1]][1]:
                msg = 'filtros '+str(ports[addr[1]][0][0])+" "+str(ports[addr[1]][0][1])
                ports[addr[1]][1] = False
                conn.send(msg.encode())
            else:
                conn.send(b'esperar')
        elif data == 'conectado':
            conn.send(b'estado_esperar')
        elif data == 'proceso_terminado':
            print("terminar proceso")
            ports.pop(addr[1])
            conn.send(b'terminar')
        else:
            conn.send(b'esperar')