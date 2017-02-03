# TCPSlowStartImplementaion

Execution of the program:
						   Through command line- python client-asn2.py -N packetSize -s serverAddress -p serverPortNumber -t timeoutValue
						   example : python client-asn2.py -N 8 -s 127.0.0.1 -p 3000 -t 2

Working:

		This program is to implement TCP conection using the underlying UDP channel for communication between the client and the server.Firstly the client sends a request to establish connection known as handshaking, where the client sends random seq no, ACK(being 0),TCP Flag(SYN),data(WAITING).The server responds with SeqNo,ACK,TCP flag and without any data. Now we have established connection, we send the first packet with sequence number equal to the ACK from the response of server,ACK equal to seqNo + 1 from the response of server and TCP flag set to "SA" and then the required data.We send the TCP requests in exponential order increasing by power of 2 every time in the field called congestion window(cwnd),slow start phase is when we keep increasing the cwnd by power of 2 until we see that timeout occurs and then once we hit a timeout then we set the cwnd to 1 and then start once again with the packet that was timed out. We exponentially increase the number of packets we send at a time and then once we start getting timeouts we decrease the cwnd and start it from 1 once again.

Challenges Faced:

		The challanges faced was to map each packet and it's corresponding ACK response and to retransmit a packet that was timed out as we are using UDP which is unreliable in tranferring data and therefore we need to maintain a timer value and then start the time for a particular packet sent and then retransmit it back once the timer is timed out, here we need to see which packet timedout and then send that packet as once cwnd starts to increase then we would be sending multiple packets at once and therefore we need to keep track. Keeping track of cwnd and then increasing it expontential and then to set it to 1 on timeout was ticky as well, as once cwnd was set to 1 after a timeout we had to then start retransmitting from the packet that was timed out and made the cwnd to be set to 1. So we solved this by setting cwnd to 1 and then going back by amount of cwnd size that was before timeout, so we eventually are transmitting the whole thing once again.

Example: 
		A simple example would be to run a server for this client first and then execute python client-asn2.py -N 8 -s 127.0.0.1 -p 3000 -t 2, which would send 8 packets to the server 127.0.0.1 which is our local loop back address on port number 3000 with timeout value as 2. The output is shown in result.txt for the same example with a server running on our local machine.
