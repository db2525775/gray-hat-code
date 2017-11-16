#-*- coding:utf-8 -*-
import sys
import socket
import threading
import copy
import time

receive_first = False

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    """创建Tcp socket
    检查本地端口是否可用，并弹出提示
    监听本地端口
    开启线程于远程主机通信，当一个请求到达时，使用proxy_handler()函数处理，并发送到远程主机"""
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #对绑定 端口做错误检查
    try:
        server.bind((local_host,local_port))
    except:
        print("[!!]Failed to listen on %s:%d"%(local_host,local_port))
        sys.exit(0)

    print("[*]Lisening on %s:%d"%(local_host,local_port))

    server.listen(5)

    while True:
        client_socket,addr = server.accept()
        #打印连接进来的IP和port
        print("[==> Received incoming connection from %s:%d]"%(addr[0],addr[1]))

        #开启一个线程与远程主机通信
        proxy_thread = threading.Thread(target=proxy_handler,\
                                         args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()
        proxy_thread.join()
        sys.exit(0)
        

def proxy_handler(client_socket,remote_host,remote_port,recive_first):
    """
    连接远程主机
    如有必要，先从远端主机接受数据，使用response_handler()函数处理数据，并将其传给本地
    实现数据从 本地->代理->远程主机的功能
    """
   #连接远程主机
    remote_socket    = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,int(remote_port)))
   
   #如果必要，从远程主机接受数据
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        #发送给我们的响应函数处理数据
        remote_buffer = response_handler(remote_buffer)
        #如果我们有数据传递给本地客户端，发送
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost."%len(remote_buffer))
            client_socket.send(remote_buffer)
    #现在我们冲本地循环读取数据，发送给远程主机和本地主机

    while True:
        #从本地提取数据
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>Received %d bytes from localhost.]"%len(local_buffer))
            hexdump(local_buffer)

            #发送给我们的本地请求函数处理数据
            local_buffer = request_handler(local_buffer,remote_host,remote_port)
            #将本地收到的数据向远程主机发送

            remote_socket.send(local_buffer)
            print("[==>]Sent to remote")
            hexdump(local_buffer)
            
        #接收响应的数据
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==]Received %d bytes from remote."%len(remote_buffer))
            hexdump(remote_buffer)
            #将响应数据发送给响应处理函数处理
            remote_buffer = response_handler(remote_buffer)

            #将响应发送到本地socket
            client_socket.send(remote_buffer)
            print("[<==]Sent to localhost.")

        #如果两边都没数据，关闭连接
        if not len(local_buffer) or not len(remote_buffer):
            time.sleep(10)
            client_socket.close()
            remote_socket.close()
            print("[*]No moredata,Closeing Connections.")
            break
            
 #修改请求包（依据实际情况添加需要的函数功能）       
def request_handler(buffer,remote_host,remote_port):
    #执行包修改

    returnBuff=""
    
    returnBuff=copy.deepcopy(buffer[0:16])
    if 'HTTP' in returnBuff:
        returnBuff=returnBuff+remote_host+':'+remote_port+buffer[36:]
        print("change %s to %s"%(buffer[16:32],returnBuff[16:64]))
        return returnBuff
    else:    
        return buffer
#修改响应包（依据实际情况添加需要的函数功能）

def response_handler(buffer):
    return buffer

#使用recv（）接受并返回数据
def receive_from(connection):
    buffer = ''
    #我们设置了两秒超时，这取决于目标情况，可能需要调整
    connection.settimeout(2)
    try:
        #持续从缓存中读取数据直到没数据或者超时
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer+=data
    except:
        print('recive data error')
    return buffer

#漂亮的十六进制导出函数
def hexdump(src,length=16):
    result = []
    digits = 4 if isinstance(src,str) else 2
    for i in range(0,len(src),length):
        s = src[i:i+length]
        hexa = b''.join(["%0*X"%(digits,ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else  b'.' for x in s])
        result.append(b"%04x %-*s %s"%(i,length*(digits+1),hexa,text))
    print(b'\n'.join(result))

def main():
    global receive_first
    if len(sys.argv[1:])!=5:
        print('Usage: ./tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]')
        print("Example:./tcpproxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    #设置本地监听参数
    local_host    = sys.argv[1]
    local_port    = int(sys.argv[2])
    # 设置目标参数
    remote_host   = sys.argv[3]
    remote_port   = sys.argv[4]
    #告诉代理在发送给远程主机前先连接和接受数据
    if 'True' in sys.argv[5]:
        
        receive_first = True
    #设置监听socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)
    sys.exit(0)
if __name__ == '__main__':
    main()


    
        
