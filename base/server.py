# -*- coding:utf-8 -*-
from socket import *
import threading
ServerUrl = "127.0.0.1:8091"
class SocketServer(threading.Thread):
    def __init__(self, monitor):
        threading.Thread.__init__(self)
        self.monitor = monitor
    def run(self): 
        try:
            Colon = ServerUrl.find(':')
            IP = ServerUrl[0:Colon]
            Port = int(ServerUrl[Colon+1:])
    
            #建立socket对象
            print 'Server start:%s'%ServerUrl
            sockobj = socket(AF_INET, SOCK_STREAM)
            sockobj.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    
            #绑定IP端口号
            sockobj.bind((IP, Port))
            #监听，允许5个连结
            sockobj.listen(5)
    
            #直到进程结束时才结束循环
            while True:
                #等待client连结
                connection, address = sockobj.accept( )
                while True:
                    #读取Client消息包内容
                    data = connection.recv(1024)
                    #如果没有data，跳出循环
                    if not data: break
                    #发送回复至Client
                    out = self.monitor.get_group(0)
                    connection.send(out)
                #关闭Socket
                connection.close( )
    
        except Exception,ex:
            print ex
