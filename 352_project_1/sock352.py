# Rutgers CS352 Project 1
# Authors: Zetao Yu, Chuanqi Xiong
import binascii
import socket as syssock
import struct
import sys
import threading
import random
import time

## usage:
# python server2.py -f recv.txt -u 1212 -v 3434
# python client2.py -d localhost -f send.txt -u 3434 -v 1212


# Global variables for init
PORTTX = 0      # transmitter port
PORTRX = 0      # receiver port
other_address = ""      # the address of the other side
# Global variables for send function
fileSeg = [""]      # divde the whole file into several segments        
segmentNo = 0     # numbers of segments
currsegIndex = 0            # current segment index
ACKIndex = 0                # current ACK check index
time_tracker = [0]    # list to keep track of time
# flags
SOCK352_SYN = 0x01    # Connection initiation
SOCK352_FIN = 0x02    # Connection end
SOCK352_ACK = 0x04    # Acknowledgement
SOCK352_RESET = 0x08  # Reset the connection
SOCK352_HAS_OPT = 0xA0    # Option field is valid
# locks for multi-threading
lock1 = threading.Lock()    
lock2 = threading.Lock()    


# store two udp ports; TX is for sending message
def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    global PORTTX, PORTRX
    PORTTX = int(UDPportTx)
    if(UDPportRx):
        PORTRX = int(UDPportRx)
    else:
        PORTRX = int(UDPportTx) 
    pass 

# function to divide a buffer into several segments 
# return a list of file segments
def fileDivder(buffer):
    buffer_string = buffer
    # compute the number of segments
    remainder = len(buffer_string)%63900
    seg_no = int(len(buffer_string)/63900)
    if remainder != 0:
        seg_no += 1
    # take substring and store in the list
    fileSeg = ["" for i in range(seg_no)]
    for x in range(0,seg_no-1):
        fileSeg[x] = buffer_string[x*63900:(x+1)*63900]
    fileSeg[seg_no-1] = buffer_string[(seg_no-1)*63900:]

    return fileSeg
    

class socket:
    
    def __init__(self):  # fill in your code here 
        global PORTRX

        # create udp socket
        self.udpSocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        # bind to receiver port
        self.udpSocket.bind(('', PORTRX))
        # set timeout
        self.udpSocket.settimeout(0.2)
        # debug info
        print "Successfully initialized!"

        # initialize all fields in packet header structure
        self.version = 0x1
        self.flags = 0x0
        self.opt_ptr = 0x0
        self.protocol = 0x0
        self.header_len = 77 # the length of header in number of bytes
        self.checksum = 0x0
        self.source_port = 0x0
        self.dest_port = 0x0
        self.sequence_no = 0x0
        self.ack_no = 0x0
        self.window = 0x0
        self.payload_len = 0x0
        # setup header format
        self.sock352PktHdrData = '!BBBBHHLLQQLL'
        self.udpPkt_hdr_data = struct.Struct(self.sock352PktHdrData)
        # initialize termination flag
        self.termination = False

        return
    
    def bind(self,address):
        # bind to a receiving port Rx
        return 

    # three way handshake from clinet side
    def connect(self,address): 
        global PORTTX, SOCK352_SYN

        # record address and port
        tup = (address[0], PORTTX)
        # Generate sequence number
        self.sequence_no = random.randint(1, 100)
        # set syn flag
        self.flags = SOCK352_SYN
        # set ack_no
        self.ack_no = 0
        # pack the message
        header = self.autopack()
        # send the first message
        self.ack_no = -1
        old_sequence_no = self.sequence_no
        while (self.ack_no != old_sequence_no+1):  
            try:      
                tup = (address[0], PORTTX)
                self.udpSocket.sendto(header, tup)
                print "Try to connect..."
            except:
                # print "Fail to connect!"
                continue
            
            # listen for ACK from server side
            try:
                recv_string, portnum = self.udpSocket.recvfrom(4096)
            except syssock.timeout:
                continue

            if len(recv_string) is not None:
                # unpack the message from server
                recv_header = self.udpPkt_hdr_data.unpack(recv_string)
                # if no connection before
                if(recv_header[1] == SOCK352_SYN):
                    print "No connection exists before."
                    # record the ack_no and seq_no from server
                    self.ack_no = recv_header[9]
                    self.sequence_no = recv_header[8]
                    break
                # if having existing connection
                elif (recv_header[1] == SOCK352_RESET):
                    self.sequence_no += 1
                    print "Connection already exists."
                    break
                else:
                    print "Fail to establish connection!"
        
        # send the returning message to server again
        temp = self.sequence_no
        self.sequence_no = self.ack_no
        self.ack_no = temp + 1
        header = self.autopack()
        self.udpSocket.sendto(header, portnum)
        # store the address of the other port
        global other_address
        other_address = portnum
        # call built-in connect()
        try:
            self.udpSocket.connect(other_address)
            print "Connecting successfully!"
        except: 
            print "Connecting failed!"
            return
        
        return 
    
    def listen(self,backlog):
        return

    # three way handshake from server side
    def accept(self):
        global SOCK352_SYN, SOCK352_RESET

        send_string = ""
        # try to recv the message from client
        while send_string == "":
            try:
                send_string, portnum = self.udpSocket.recvfrom(4096)
            except syssock.timeout:
                continue
            if len(send_string) != 0:
                # unpack the message from server
                send_header = self.udpPkt_hdr_data.unpack(send_string)
                if self.flags == 0:  # no connection before
                    self.flags = SOCK352_SYN
                elif (self.flags == SOCK352_SYN) or (self.flags == SOCK352_RESET): # have an existing connection
                    self.flags = SOCK352_RESET
                self.sequence_no = random.randint(1, 100)
                self.ack_no = send_header[8] + 1
        # pack header and send
        header = self.autopack()
        self.udpSocket.sendto(header, portnum)
        print "Connection built!"
        # update sequence_no and ack_no
        temp = self.sequence_no
        self.sequence_no = self.ack_no
        self.ack_no = temp + 1
        # store the address of the other port
        global other_address
        other_address = portnum
        # recv another message to finish three way handshake
        try:
            send_string, portnum = self.udpSocket.recvfrom(4096)
            print "Three way handshake finished!"
        except:
            print "Three way handshake not yet finished!"

        return (self,portnum)
    
    # close the connection if there is no more transmission
    def close(self): 
        global other_address, SOCK352_FIN, SOCK352_ACK

        # close if last packet received; else set close variable
        if self.termination == False:
            print "The transmission has not yet finished!"
            return
        # create a header with FIN bit set
        self.flags = SOCK352_FIN
        self.sequence_no += 1
        header = self.autopack()
        # send close info 
        self.ack_no = -1 
        double_handshake = 0
        try: 
            self.udpSocket.sendto(header, other_address)
        except:
            self.udpSocket.send(header)
        self.udpSocket.settimeout(0.2)
        # check ACKs from the other side
        while self.termination:    
            try:
                recv_string, portnum = self.udpSocket.recvfrom(4096)
            except syssock.timeout:
                print("No ACKs received in termination step!")
                continue
            if (recv_string is not None) and (len(recv_string) >= 40):  # listen for messages from the other side
                # unpack the message
                recv_header = self.udpPkt_hdr_data.unpack(recv_string)
                if recv_header[1] == SOCK352_FIN:   # receive the close request
                    double_handshake += 1
                    # create ACK header and send back
                    self.ack_no = recv_header[8]+1
                    self.flags = SOCK352_ACK
                    ACKheader = self.autopack()
                    try: 
                        self.udpSocket.sendto(ACKheader, other_address)
                    except:
                        self.udpSocket.send(ACKheader)
                elif (recv_header[1] == SOCK352_ACK) and (recv_header[9] == self.sequence_no + 1): # receive the ACK
                    double_handshake += 1
                    print "Close successfully!"
            if double_handshake == 2:
                break
        # call built-in close()
        try:
            self.udpSocket.close()
        except:
            print "Socket has already been closed by the other side!"
            return 

        return 

    # Go-Back-N from client side
    def send(self, buffer):
        global fileSeg, segmentNo, currsegIndex, ACKIndex, time_tracker
        # initialize all variables for sending
        self.termination = False    
        currsegIndex = 0            # current segment index
        ACKIndex = 0                # current ACK check index
        fileSeg = fileDivder(buffer)   # divde the whole file into several segments
        segmentNo = len(fileSeg)     # numbers of segments 
        time_tracker = [0 for i in range(segmentNo)]    # list to record starting sending time of each segment
        old_sequence_no = self.sequence_no
        
        if segmentNo == 0:  # buffer size is 0
            print "No buffer is passed!"
            return 0

        # inner function to keep receiving ACK
        def recvthread(): 
            global fileSeg, segmentNo, currsegIndex, ACKIndex, time_tracker
            while True:
                with lock1:
                    if time_tracker[ACKIndex] == 0:     # in the case this packet has not yet been sent out
                        continue
                    if (time.time() - time_tracker[ACKIndex]) >= 0.2:    # timeout
                        # notify the another thread to retransmit
                        print "Time is out!"
                        currsegIndex = ACKIndex
                        lock1.release()
                        continue
                    else:
                        try:
                            recv_string, portnum = self.udpSocket.recvfrom(4096)
                            # unpack the header and update ACKIndex
                            if recv_string is not None:
                                print "Succeed to get No. %d ACK!" %ACKIndex
                                ACKIndex += 1
                        except:
                            print "Fail to get No. %d ACK!" %ACKIndex
                            continue
                # check whether all ACKs have been received
                with lock2:
                    if ACKIndex == segmentNo:
                        self.termination = True     # set the termination flag to be True
                        break

        # create one thread to keep checking ACKs
        t1 = threading.Thread(target=recvthread)
        t1.start()

        # keep sending segments
        while True:
            with lock1:
                if currsegIndex < segmentNo:    # if packets have not all been sent out
                    # update sequence no
                    self.sequence_no = old_sequence_no + 1 + currsegIndex
                    # assemble the chunk
                    chunk = self.__assemble_chunk(fileSeg[currsegIndex])
                    # call built-in send() to send the packet
                    self.udpSocket.send(chunk)
                    print "SENT!!"
                    # record send time
                    time_tracker[currsegIndex] = time.time()
                    # update segment index
                    currsegIndex += 1
            # check whether all ACKs have been received
            with lock2:
                if self.termination:
                    break

        print "Finished a single send!"
        return len(buffer)

    # accept packets in order and send back ACKs
    # return number of bytes received
    # the maximum packet is 40 + 63900 bytes
    def recv(self,nbytes):
        
        global other_address

        self.termination = False     # set termination flag to be False
        bytesreceived = ""
        print "Start to receive data..."

        allData = ""
        currBytes = ""
        currSeqNo = 0
        expSeqNo = self.sequence_no + 1

        while nbytes>0:
            
            # unpack the packet
            try:
                allData = self.udpSocket.recv(63940)
            except syssock.timeout:
                print "Time out for receiving bytes"
                continue
            if len(allData) != 0:
                (header, currBytes) = (allData[:40],allData[40:])
                currHeader = self.udpPkt_hdr_data.unpack(header)
                currSeqNo = currHeader[8]
                currPayload = currHeader[11]
                
            # check if payload exceeds 64000 bytes
            if currPayload>63900:
                print "Data exceeds payload"
                return 0

            print "Received sequence number is " + str(currSeqNo)

            # check if there are packets lost
            if currSeqNo != (expSeqNo):
                print "Expected " + str(expSeqNo) + ", but can not get it."
                continue

            # send ACK if received correct packet
            self.flags = SOCK352_ACK
            ackHeader = self.autopack()
            self.udpSocket.sendto(ackHeader, other_address)

            bytesreceived = bytesreceived + currBytes
            nbytes = nbytes - currPayload
            expSeqNo = expSeqNo + 1

        self.termination = True     # set termination flag to be True
        self.sequence_no = expSeqNo - 1     # update sequence no
        print "Done a single receiving\n"
        print "***************************************\n"
        return bytesreceived 

    # helper function to pack the header
    def autopack(self):
        return self.udpPkt_hdr_data.pack(self.version, self.flags, self.opt_ptr, self.protocol, self.header_len, self.checksum, 
            self.source_port, self.dest_port, self.sequence_no, self.ack_no, self.window, self.payload_len)

    # helper function to assemble header and content data
    def __assemble_chunk(self, seg):
        # update payload_len
        if len(seg) > 63900:   # in the case the payload length plus header is over 64k (for debug use)
            print "Oversized segment!"
            return None
        else:
            self.payload_len = len(seg)
        header = self.autopack()
        chunk = header + seg
        return chunk



    


