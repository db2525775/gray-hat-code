#-*- coding:utf-8 -*-
import socket
import os
import struct
from ctypes import *

#监听主机
host = "192.168.2.100"

#定义IP头
class IP(Structure):
    _fields_ =[
        ("ihl",        c_ubyte,4),
        ("version",    c_ubyte,4),
        ("tos",        c_ubyte),
        ("len",        c_ushort),
        ("id",        c_ushort),
        ("offset",    c_ushort),
        ("ttl",       c_ubyte),
        ("protocol_num",c_ubyte),
        ("sum",        c_ushort),
        ("src",        c_ulong),
        ("dst",        c_ulong)

    ]
    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    def __init__(self,socket_buffer=None):
        #协议字段名称
        self.protocol_map={1:'ICMP',6:'tcp',17:'udp'}
        #可读性更强的IP地址
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))
        #协议类型
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

#创建原始套接字，然后绑定到主机
if os.name == "nt":
    socket_protocal = socket.IPPROTO_IP
else:
    socket_protocal = socket.IPPROTO_ICMP

capture_socket = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocal)

capture_socket.bind((host,0))

#设置在捕获的数据包中包含IP头部：
capture_socket.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

#在Windows平台上，我们需要设置IOCTL以启动混杂模式。
if os.name =='nt':
    capture_socket.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

#读取单个数据包
try:
    while True:
        raw_buffer = capture_socket.recvfrom(65535)[0]
        ip_header  = IP(raw_buffer[0:20])

        #输出协议和通信双方IP地址：
        print("Protocol:%s  %s->%s"%(ip_header.protocol,ip_header.src_address,\
                                     ip_header.dst_address))
except KeyboardInterrupt:
    

    #在windows平台上关闭混杂模式

    if os.name =='nt':
        capture_socket.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
        capture_socket.close()
    
