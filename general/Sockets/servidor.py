import socket

def Main(ip):
    host = ip
    port = 5000

    print("Open server in", ip)
    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(5)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if data == "end":
            break
        print ("from connected  user: " + str(data))
        data = str(data).upper()
        print ("sending: " + str(data))
        conn.send(data.encode())

    conn.close()

