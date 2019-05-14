#protocolo TCP

import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def subirArchivo(socket,file):
     
     socket.send(("upload").encode('ascii'))
    
     from_server = socket.recv(1024)
     print(from_server.decode('ascii'))
     
     file_client = open("documentsClient/" + file, "r")
     socket.send(file.encode('ascii'))
     
     for datos in file_client:
         socket.send(datos.encode('ascii'))
     file_client.close()
     
     print("Done upload !")
     socket.close()

def descargarArchivo(socket,file):

    socket.send(("download").encode('ascii'))
    from_server = socket.recv(1024)
    print((from_server).decode('ascii'))
    
    socket.send((file).encode('ascii'))
    
    newfile = open("documentsClient/" + file , "w+")
    while True:
        from_server = socket.recv(1024)
        if not from_server:
            break
        newfile.write(from_server.decode('ascii'))
    
    newfile.close()
    print("Download done !")
    socket.close()

def listar(socket):

    socket.send(("list").encode('ascii'))
    
    while True:

        from_server = socket.recv(1024)
        if not from_server:
            break

        print(from_server.decode('ascii'))

if (len(sys.argv) > 5) or (len(sys.argv) < 3):
    print ("Parameters not defined")
else:
    
    HOST = (sys.argv[1])
    PORT = int(sys.argv[2])
    address = (HOST,PORT)
    
    client.connect(address)

    if (sys.argv[3] == "-d"):
       descargarArchivo(client,sys.argv[4])
    elif (sys.argv[3] == "-u"):
       subirArchivo(client,sys.argv[4])
    elif (sys.argv[3] == "-l"):
         listar(client)


