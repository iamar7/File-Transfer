import socket
from os import system
from hashlib import sha256

def recv():
    recfile=''
    #while True:
    SIZE = s.recv(128)
    SIZE = int(SIZE)
    recvd = 0
    s.send('Y')
    while recvd<SIZE:
        chunk = s.recv(128)
        print 'receiving'
        recvd += len(chunk)
        recfile += chunk
    return recfile

def sendstr(pkt):
    global s
    SIZE = len(pkt)
    s.send(str(SIZE))
    print s.recv(2)
    sent = 0
    while True:
        print 'Sending'
        sent += s.send(pkt[sent:])
        print sent
        if sent==SIZE:
            print 'SENT!!!!!!! \~O~/'
            break


def updatels():
    system('ls -l ./clientshare > cls')

def lshash():
    global clshash
    system('sha256sum cls > clshash')
    f=open('clshash')
    clshash = f.read().split()[0]
    f.close()

def sendlist():
    global s,cls
    sendstr(clshash)
    f=open('cls')
    cls=f.read()
    f.close()
    sendstr(cls)

def getlist():
    global s,sls,slshash
    slshash= recv()
    sls = recv()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 23453                # Reserve a port for your service.
s.connect((host, port))
print 'Connected to',host,port

clshash=''
cls=''
sls=''
slshash=''
updatels()
lshash()
print clshash

sendlist()
getlist()

inp=''
while inp!='null':
    inp = raw_input('>>')
    sendstr(inp)
    fle = recv()
    print fle
    has = recv().split()[0]
    if has==sha256(fle).hexdigest():
        print "No file transfer errors"
        timestamp = recv()
        print inp.split()[1],len(fle),timestamp,has
        

exit(0)

recfile=''
while True:
    chunk = s.recv(128)
    print 'receiving'
    if chunk=='':
        break
    recfile += chunk
print recfile
f=open('recfile','w')
f.write(recfile) 
f.close()
s.close
