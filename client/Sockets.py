import socket
from client.Filters import *

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message = 'conectado'

def Main(ip, carpeta):
    global message
    host = ip
    port = 5000
    mySocket.connect((host,port))
    while message != 'terminar':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
        if data == 'estado_esperar':
            message = 'esperando'
        elif 'filtros' in data:
            datos = data.split(" ")
            generar_Imagenes(carpeta, int(datos[1]), int(datos[2]))
            message = 'proceso_terminado'
        elif data == 'terminar':
            message = data
    mySocket.close()
