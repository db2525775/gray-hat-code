# -*- coding:utf-8 -*-
import sys
import socket
import copy
import threading
class Cli():
    def __init__(self):
        self._input=''
        self._output=''        
        pass
    def getinput(self,strbuff):
        if strbuff:
           self._input=copy.deepcopy(strbuff)
           print("%s\n"%self._input)
        else:
           self._input=''
        return self._input
        
    def getoutput(self):  
        if self._output =='':
            self._output=raw_input('>')
            if self._output=='':
               self._output='\r'               
        else:
            self._output =''
        return self._output
                     
            
            
    def sdata(self,client):
        # print out what the client sends 
        recvbuff=''
        recv_len=1
        while True:
            try:
                while recv_len:
                    input=client.recv(1024)
                    recv_len = len(input)
                    recvbuff+=input
                    if recv_len<1024:
                        break
                    if input =='exit!':
                        client.close()
                        print('exit nt!')                        
                        sys.exit()
                self.getinput(recvbuff) 
                
                output=self.getoutput()
                if output == 'exit!':
                    client.send(output)
                    client.close()
                    sys.exit()                
                client.send(output)
                self._output =''                
                                  
            except Exception as e:
                print('ERR:%s'%e)
                client.close()   
                sys.exit()
            
        
    def rdata(self,client):
        # print out what the client sends 
        recvbuff=''
        recv_len=1
        while recv_len:
            try:
                input=client.recv(1024)
                print(input)
                recv_len = len(input)
                recvbuff+=input
                if recv_len<1024:
                    break
                if input =='exit!':
                    break                         
            except Exception as e:
                print('ERR:%s'%e)
                client.close()
                sys.exit()
        self.getinput(recvbuff)                    
    def rsthread(self,client):
        print('conected sucessful,begin send and recv data!')
        client_send = threading.Thread(target=self.sdata,args=(client,))        
        #client_recev = threading.Thread(target=self.rdata,args=(client,))
        #client_recev.start()
        client_send.start()
        
        client_send.join()
#        client_recev.join()
        
        
class Netcon():
        def __init__(self,srcip='127.0.0.1',srcport=8080,dstip='127.0.0.1',dstport=8080,proto='tcp'):
            self.srcip   = srcip
            self.srcport = srcport
            self.dstip   = dstip
            self.dstport = dstport
            self.proto   = proto
        
        def sock(self):
            if self.proto == 'tcp':
               return socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            else:
               return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
               
        def tcpserver(self):
            server = self.sock()
            server.bind((self.srcip,self.srcport))
            server.listen(5)
            print("server is listen on %s %d"%(self.srcip,self.srcport))
            client,addr = server.accept()
            print('start transmit data....')
            cli=Cli()
            cli.rsthread(client)
            print('socket is closed!')
            client.close()
            sys.exit()
            
        def tcpconR(self):
            #tcp client  connect remote tcp server,retrun rcvdata
            sock=self.sock()
            print('conect to %s:%d'%(self.dstip,self.dstport))
            sock.connect((self.dstip,self.dstport))
            cli=Cli()
            cli.rsthread(sock) 
            print('exit! socket close')            
            sock.close()
            sys.exit()
                
            
        def udpconR(self,buff):
            #udp client connect remote udp,return sock,data and ip
            with self.sock() as sock:
                sock=self.sock()
                sock.sendto(buff,(self.dstip,self.dstport))
                response,ip=sock.recvfrom(4096)
                return response,ip
            
if __name__ == "__main__":
   cli=Cli()
   netcon=Netcon(srcip=sys.argv[1],srcport=int(sys.argv[2]))
   #netcon.tcpconR()
   netcon.tcpserver()

   
       
   