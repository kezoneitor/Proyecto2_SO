import socket
from client.Filters import *

mySocket = socket.socket()
message = 'conectado'
def Main(ip, carpeta):
    global message
    host = ip
    port = 5000
    mySocket.connect((host,port))
    while message != 'terminar':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
        print ('Received from server: ' + data)
        if data == 'estado_esperar':
            message = 'esperando'
        elif 'filtros' in data:
            datos = data.split(" ")
            generar_Imagenes(carpeta, int(datos[1]), int(datos[2]))
            message = 'proceso_terminado'
        elif data == 'terminar':
            message = data
    mySocket.close()

if __name__ == '__main__':
        Main("172.24.120.243","C:/Users/Kezo/Documents/GitProjects/Project2_SO_VKP/Proyecto2_SO/client/imagenes/")
