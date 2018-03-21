import socket
from os import path
from os import system

def sendstr(pkt):
    global c
    SIZE = len(pkt)
    c.send(str(SIZE))
    c.recv(2)
    sent = 0
    while True:
        print 'Sending'
        sent += c.send(pkt[sent:])
        print sent
        if sent==SIZE:
            print 'SENT!!!!!!! \~O~/'
            break

def recv():
    recfile=''
    #while True:
    SIZE = c.recv(128)
    print SIZE
    SIZE = int(SIZE)
    recvd = 0
    c.send('Y')
    while recvd<SIZE:
        chunk = c.recv(128)
        print 'receiving'
        recvd += len(chunk)
        recfile += chunk
    return recfile

def updatels():
    system('ls -l ./servershare > sls')

def lshash():
    global slshash
    system('sha256sum sls > slshash')
    f=open('slshash')
    slshash = f.read().split()[0]
    f.close()


def getlist():
    global c,cls,clshash
    print 'confirm'
    clshash = recv()
    cls = recv()

def sendlist():
    global sls
    sendstr(slshash)
    f=open('sls')
    sls=f.read()
    f.close()
    sendstr(sls)


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 23453
s.bind((host,port))
s.listen(5)

slshash=''
sls=''
cls=''
clshash=''
updatels()
lshash()
print slshash


c,addr = s.accept()
print 'Got Connection from',addr


getlist()
sendlist()

inp=''
while inp is not "null":
    inp=recv()
#    print inp
    inp=inp.split()
    if inp[0]=="FileDownload":
        if inp[1][0]=='-':
            filename=inp[2]
        else:
            filename=inp[1]
        conf=''
#        while conf is not "confirm":
        f=open('./servershare/'+filename)
        string=f.read()
        f.close()
        sendstr(string)
        print 'file sent'
        system('sha256sum ./servershare/'+filename+'> tmphash')
        f=open('./tmphash')
        has=f.read()
        f.close()
        sendstr(has)
        system('stat -c %y ./servershare/' + filename+'>temptime')
        f=open('temptime')
        timestamp = f.read()
        f.close()
        sendstr(timestamp)
#         conf=recv()

exit(0)
sent = 0
f = open('servershare/file.txt')
fil = f.read()
f.close()
print 'filestream : ',repr(fil)


c.close
s.close
