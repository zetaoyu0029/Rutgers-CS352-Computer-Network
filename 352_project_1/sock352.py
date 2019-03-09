
import binascii
import socket as syssock
import struct
import sys
import threading
import random

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

# class sock352_pkt_hdr():
#     def __init__(self, field1, field2, field3):
#         self.field1 = field1
#         self.field2 = field2
#         self.field3 = field3

## usage:
# python server2.py -f ./test.txt -u 1212 -v 3434
# python client2.py -d localhost -f ./test.txt -u 3434 -v 1212


# Global variables for init
PORTTX = 0      # transmitter port
PORTRX = 0     # receiver port
other_address = ""      # the address of the other side
# Global variables for send function
fileSeg = [""]      # divde the whole file into several segments
ACKList = [0]        
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

lock = threading.Lock()


def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    # store two udp ports; TX is for sending message
    # setup port numbers
    global PORTTX, PORTRX
    PORTTX = int(UDPportTx)
    if(UDPportRx):
        PORTRX = int(UDPportRx)
    else:
        PORTRX = int(UDPportTx)

    print "UDPportTx is: %d\n" %PORTTX
    print "UDPportRx is: %d\n" %PORTRX
    
    pass 

# divide a buffer into several segments 
# return a list of file segments and a list of ACK list
def fileDivder(buffer):
    # delcare a list of file segments
    if sys.getsizeof(buffer)%63950 == 0:
        fileSeg = []*sys.getsizeof(buffer)%63950
    else:
        fileSeg = []*(sys.getsizeof(buffer)/63950+1)

    for x in xrange(0,len(fileSeg)):
        fileSeg[x] = buffer[x*63950:(x+1)*63950]

    # declare a list of ACK
    # 0 indicates not yet acked
    # 1 indicates acked
    ACKList = []*len(fileSeg)
    for x in xrange(0,len(ACKList)):
        ACKList[x] = 0
   
    print "from fileDivder:"
    print fileSeg
    print ACKList

    return fileSeg, ACKList

    
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
        self.header_len = 40 # the length of header in number of bytes
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
        # pack the initial struct
        # self.header = self.autopack()

        return
    
    def bind(self,address):
        # bind to a receiving port Rx
        return 

    def connect(self,address):  # fill in your code here 
        global PORTTX, SOCK352_SYN
        print "address is: \n"
        print address
        tup = (address[0], PORTTX)
        print tup
        # Generate sequence number
        self.sequence_no = random.randint(1, 100)
        # set syn flag
        self.flags = SOCK352_SYN
        # set ack_no
        self.ack_no = 0
        # pack the message
        header = self.autopack()
        # send the message
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
            
            try:
                recv_string, portnum = self.udpSocket.recvfrom(4096)
            except syssock.timeout:
                print("Fail to establish connection!")
                continue

            if len(recv_string) is not None:
                # unpack the message from server
                recv_header = self.udpPkt_hdr_data.unpack(recv_string)
                # if no connection before
                if(recv_header[1] == SOCK352_SYN):
                    print "No connection exists before. Connected!"
                    # record the ack_no and seq_no from server
                    self.ack_no = recv_header[9]
                    self.sequence_no = recv_header[8]
                    break
                # if having existing connection
                elif (recv_header[1] == SOCK352_RESET):
                    self.sequence_no += 1
                    print "Connection already exists. Connected!"
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
            syssock.connect(address)
        except: 
            print "Connecting failed!"
            return
        
        return 
    
    def listen(self,backlog):
        # find size of socket array
        return

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
        clientsocket = self
        clientsocket.udpSocket.sendto(header, portnum)
        # update sequence_no and ack_no
        temp = self.sequence_no
        self.sequence_no = self.ack_no
        self.ack_no = temp + 1
        # store the address of the other port
        global other_address
        other_address = portnum
        return (clientsocket,portnum)
    
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
        # send close info and check ACKs from the other side
        self.ack_no = -1 
        double_handshake = 0
        self.udpSocket.sendto(header, other_address)
        self.udpSocket.settimeout(0.2)
        while self.termination:    
            try:
                recv_string, portnum = self.udpSocket.recvfrom(4096)
            except syssock.timeout:
                print("No ACKs received in termination step!")
                continue
            if recv_string is not None:
                recv_header = self.udpPkt_hdr_data.unpack(recv_string)
                if recv_header[1] == SOCK352_FIN:
                    double_handshake += 1
                    # create ACK header and send
                    self.ack_no = recv_header[8]+1
                    self.flags = SOCK352_ACK
                    ACKheader = self.autopack()
                    self.udpSocket.sendto(ACKheader, other_address)
                elif (recv_header[1] == SOCK352_ACK) and (recv_header[9] == self.sequence_no + 1):
                    double_handshake += 1
                    # close
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

    def send(self,buffer):
        global fileSeg, ACKList, segmentNo, currsegIndex, ACKIndex, time_tracker
        
        fileSeg, ACKList = fileDivder(buffer)   # divde the whole file into several segments
        segmentNo = len(fileSeg)     # numbers of segments 
        time_tracker = [0]*segmentNo
        
        if segmentNo == 0:
            print "No buffer is found in the location directory!"
            return
            
        print "from send function:"
        print fileSeg
        print ACKList
        print segmentNo
        print time_tracker

        # keep receiving ACK
        def recvthread(): 
            global fileSeg, ACKList, segmentNo, currsegIndex, ACKIndex, time_tracker
            while True:
                with lock:
                    print "ACKIndex: %d"%ACKIndex
                    print time_tracker
                    if time_tracker[ACKIndex] == 0:     # in the case this packet has not yet been sent out
                        continue
                    if time.clock() - time_tracker[ACKIndex] < 0.00000001:    # timeout
                        # notify the another thread to retransmit
                        currsegIndex = ACKIndex
                        print "Time is out!"
                        break
                    self.udpSocket.settimeout(0.2 - (time.clock() - time_tracker[ACKIndex]))       #set timeout value
                    try:
                        recv_string, portnum = self.udpSocket.recvfrom(4096)
                        # unpack the header and update ACKIndex
                        if recv_string is not None:
                            ACKIndex += 1
                            print "Succeed to get No. %d ACK!" %ACKIndex
                    except syssock.timeout:
                        # notify the another thread to retransmit
                        currsegIndex = ACKIndex
                        print "Fail to get No. %d ACK!" %ACKIndex
                        continue
                # check whether all ACKs have been received
                with lock:
                    if ACKIndex == segmentNo:
                        self.termination = True     # set the termination flag to be True
                        break

        # create one thread to keep checking ACKs
        t1 = threading.Thread(target=recvthread)
        t1.start()

        # keep sending segments
        while True:
            with lock:
                if currsegIndex < segmentNo:    # if packets have not all been sent out
                    # update sequence no
                    self.sequence_no += (1 + currsegIndex)
                    # assemble the chunk
                    chunk = self.__assemble_chunk(fileSeg[currsegIndex])
                    # update segment index
                    currsegIndex += 1
                    # call built-in send() to send the packet
                    syssock.send(chunk)
                    # record send time
                    time_tracker[currsegIndex] = time.clock()
            # check whether all ACKs have been received by another thread
            with lock:
                if self.termination:
                    break

        return len(buffer)


    def recv(self,nbytes):
        # only accept expected packets
        # send acks
        # return number of bytes received
        # reassemble packets
        # header length 40 bytes
        # one packet maximum lenth 6400 bytes
        global other_address

        bytesreceived = ""
        print "Start to receive data..."

        allData = ""
        currBytes = ""
        currSeqNo = 0
        expSeqNo = self.sequence_no + 1

        while nbytes>0:

            # unpack the packet
            try:
                allData, portnum = self.udpSocket.recvfrom(4096)
            except syssock.timeout:
                continue
            if len(allData) != 0:
                (currHeader, currBytes) = (allData[:40],allData[40:])
                currHeader = self.udpPkt_hdr_data.unpack(allData)
                currSeqNo = currHeader[8]
                currPayload = currHeader[11]
                
            # check if payload exceeds 64000 bytes
            if currPayload>63950:
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
            syssock.sendto(ackHeader, other_address)

            bytesreceived = bytesreceived + currBytes
            nbytes = nbytes - len(currBytes)

            expSeqNo = expSeqNo + 1

        self.termination = True     # set termination flag to be True
        print "Done receiving\n"
        print "***************************************\n"
        print bytesreceived
        print "***************************************\n"
        return bytesreceived 

    def autopack(self):
        return self.udpPkt_hdr_data.pack(self.version, self.flags, self.opt_ptr, self.protocol, self.header_len, self.checksum, 
            self.source_port, self.dest_port, self.sequence_no, self.ack_no, self.window, self.payload_len)

    
    def __assemble_chunk(self, seg):
        # update payload_len
        self.payload_len = len(seg)
        if len(seg) > 63950:   # in the case the payload length plus header is over 64k (for debug use)
            print "Oversized segment!"
            return None
        header = self.autopack()
        chunk = header + seg
        return chunk



    


