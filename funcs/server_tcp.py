#protocolo TCP

import socket
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
buffer = 1024
address = (HOST,PORT)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))

serversocket.listen(10)
       
print('Starting listening... ', address)
while True:
    
    clientsocket, addr = serversocket.accept()
    
    print("Received a connection from " + str(addr[0]) +" " + str(addr[1]))
    from_client = clientsocket.recv(buffer)
    
    if (from_client.decode('ascii') == "upload"):
        clientsocket.send(("Uploading...").encode('ascii'))
        print("Receiving...")
        
        from_client = clientsocket.recv(buffer)
        file = open("documentsServer/" + from_client.decode('ascii'),"w+")
        
        while True:
             from_client = clientsocket.recv(buffer) 
             if not from_client:
                 break
             file.write(from_client.decode('ascii'))
             
        file.close()
        print("Received !")
        clientsocket.close()
        
    elif(from_client.decode('ascii') == "download"):
        
        clientsocket.send(("Downloading...").encode('ascii'))
        print("Sending...")
        from_client = clientsocket.recv(buffer)
        file = open('documentsServer/' + from_client.decode('ascii'), "r")
        for dat in file:
            clientsocket.sendall(dat.encode('ascii'))
        clientsocket.close()
        
    elif(from_client.decode('ascii') == "list"):
        
        files = os.listdir('documentsServer/')
        
        for file in files:
            variable = file + '\n'
            clientsocket.send(variable.encode('ascii'))

        clientsocket.close()

    print('Client disconnected')
   
