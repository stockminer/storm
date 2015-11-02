# -*- coding:utf-8 -*-
from socket import *

def SocketClient():
    try:
        #建立socket对象
        s=socket(AF_INET,SOCK_STREAM,0)

        Colon = ServerUrl.find(':')
        IP = ServerUrl[0:Colon]
        Port = ServerUrl[Colon+1:]

        #建立连接
        s.connect((IP,int(Port)))
        sdata='GET /Test HTTP/1.1\r\n\
Host: %s\r\n\r\n'%ServerUrl

        print "Request:\r\n%s\r\n"%sdata
        s.send(sdata)
        sresult=s.recv(1024)

        print "Response:\r\n%s\r\n" %sresult
        #关闭Socket
        s.close()
    except Exception,ex:
        print ex

ServerUrl = "127.0.0.1:8091"
SocketClient()
