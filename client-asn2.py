import socket
import random
import string
import time
import sys
import getopt
import argparse 
packetnum = ''
server = ''
port ='' 
timeOut = ''

# parsing the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-N","--packets", help="Enter the total numnber of packets to be sent(minimum 20)")
parser.add_argument("-t","--timeout", help="Enter the timeout value in seconds")
parser.add_argument("-s","--serverip", help="Enter the server's IP address")
parser.add_argument("-p","--serverport", help="Enter the server's port number")

args = parser.parse_args()

if(args.serverport!=None and args.packets!=None and args.timeout!=None):
	server = args.serverip
	port = int(args.serverport)
	packetnum = int(args.packets)
	timeOut = int(args.timeout)
else:
	packetnum,server,port,timeOut = None,None,None,None


if(packetnum == None or server ==None or port ==None or timeOut==None):
    print "Usage: ", sys.argv[0], " -N <No of packets> -s <port address> -p <port number> -t <timeout>"
    sys.exit(2)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
BUFFER_SIZE = 1024
Uppercase = list(string.ascii_uppercase)
#s.connect((server,port))
stop = 100
InitSeqRange = 1000
seqno = Initseqno = random.randrange(InitSeqRange)
ACK = 0
i = 0
cwnd = 1
oldcwnd = 0
count = 0
parsepacket = 0
packetinfo = {}
randomnums = []
listOfSeq = {}
for i in range(packetnum):
	randomnums.append(random.randrange(stop))

u = 0

while (u<cwnd):
	try:
		s.settimeout(timeOut)
		startTime = time.time()
		packet = ''+str(Initseqno)+','+str(ACK)+','+'SYN'+','+'Waiting'
		s.sendto(packet,(server,port))
		print 'Client:',startTime,',',packet
		serverpacket,address = s.recvfrom(BUFFER_SIZE)
		endTime = time.time()
		print 'Server:',endTime,',',serverpacket
		Seqno,ACK,Flag = serverpacket.split(',')
		seqno = int(ACK)
		ACK = int(Seqno) + 1
		u+=1
	except socket.timeout:
		#cwnd = 1
		#print "Time out Occured!!!!!!!!!!!!!!!!!!!!!!!!!!"
		continue
		
		
	
#print oldcwnd , cwnd
while(oldcwnd<=packetnum):
	#if count <=1 :
		#print cwnd
	for j in range(cwnd):
	        s.settimeout(timeOut)
		data = Uppercase[(oldcwnd+j)%26]*randomnums[(oldcwnd+j)%26]
		#print data
		#BUFFER_SIZE = len(data)
		if oldcwnd+j == packetnum-1:
		        clientpacket =  ''+str(seqno)+','+str(ACK)+','+'F'+','+data
		else:
				clientpacket =  ''+str(seqno)+','+str(ACK)+','+'SA'+','+data
		#BUFFER_SIZE = len(clientpacket)
		try:
			startTime = time.time()
			#packetinfo[''+str(seqno)] = ''+str(startTime)
			res = s.sendto(clientpacket,(server,port))
			print 'Client:',startTime,',',clientpacket
		except socket.error,e:
				s.close()
		seqno = seqno + 1
		#i+=cwnd
	oldcwnd +=cwnd
	#print oldcwnd , packetnum
	#for x in range(cwnd):
	try:
		if count <= packetnum:
			serverpacket,address = s.recvfrom(BUFFER_SIZE)
			endTime = time.time()
			print 'Server:',endTime,',',serverpacket
			cwnd *= 2
			Seqno,ACK,Flag = serverpacket.split(',')
			#listOfSeq[int(Seqno+1] = ''+str(endTime)
			h = cwnd/2
			d=oldcwnd - h			
			for a in range(h):
				if int(ACK) == seqno + randomnums[(d+a)]:
					d +=a
					if(h - a > 0):
						cwnd = 1
						oldcwnd = d
			#print 'AFTER:',cwnd , oldcwnd
			seqno=int(ACK)
			#print endTime , ACK
			ACK = int(Seqno) + 1
			#print abs(endTime - startTime)
			count+=1
			#timeout
			if count == packetnum:
				s.close()
				#print packetinfo,oldcwnd
				sys.exit()
	except socket.timeout:
		if count > 0:
			oldcwnd-=cwnd
			cwnd = 1
		else:
			cwnd = 1
			oldcwnd = 0
	if packetnum - oldcwnd < cwnd:
		cwnd = packetnum - oldcwnd
#print packetinfo,oldcwnd		
sys.exit()
