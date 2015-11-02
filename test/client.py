import socket, sys

host = '10.99.19.18'
# host = raw_input("Plz imput destination IP:")
# data = raw_input("Plz imput what you want to submit:")
port = 51423

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.connect((host, port))
except socket.gaierror, e:
    print "Address-related error connecting to server: %s" %e
    sys.exit(1)
except socket.error, e:
    print "Connection error: %s" %e
    sys.exit(1)

data = raw_input("Plz imput what you want to submit:")
s.send(data)
s.shutdown(1)
print "Submit Complete"
while 1:
        buf = s.recv(1024)
        sys.stdout.write(buf)

