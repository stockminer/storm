import socket, traceback

host = ''
port = 51423

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)
print "done"

while 1:
    #when connect error happen, skip the error
    print '==========='
    try:
        ClientSock, ClientAddr = s.accept()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
        continue

    #Get informaion form client and reply
    try:
        print "Get connect from ", ClientSock.getpeername()
        data = ClientSock.recv(1024)
        print "The information we get is %s" % str(data)
        ClientSock.sendall("I`ve got the information: ")
        ClientSock.sendall(data)
        while 1:
            str = raw_input("What you want to say:")
            ClientSock.sendall(str)
            ClientSock.sendall('\n')
    except (KeyboardInterrupt ,SystemError):
        raise
    except:
        traceback.print_exc()

    #Clocs socket
    try:
        ClientSock.close()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
