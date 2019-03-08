
import binascii
import socket as syssock
import struct
import sys
import threading

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

# class sock352_pkt_hdr():
#     def __init__(self, field1, field2, field3):
#         self.field1 = field1
#         self.field2 = field2
#         self.field3 = field3

# Global variables
PORTTX      # transmitter port
PORTRX      # receiver port
sock352PktHdrData       # packet format
udpPkt_hdr_data     # packet format struct
udpSocket       # udp socket for communication

SOCK352_SYN = 0x01    # Connection initiation
SOCK352_FIN = 0x02    # Connection end
SOCK352_ACK = 0x04    # Acknowledgement
SOCK352_RESET = 0x08  # Reset the connection
SOCK352_HAS_OPT = 0xA0    # Option field is valid


def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    # store two udp ports; TX is for sending message
    # setup header format
    sock352PktHdrData = '!BBBBHHLLQQLL'
    udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
    # setup port numbers
    PORTTX = UDPportTx
    if(UDPportRx)
        PORTRX = UDPportRx
    else
        PORTRX = UDPportTx
    
    pass 
    
class socket:
    
    def __init__(self):  # fill in your code here 
        # create udp socket
        if(!self.udpSocket)
            self.udpSocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        # bind to receiver port
        self.udpSocket.bind(('', PORTRX))
        # set timeout
        self.udpSocket.settimeout(0.2)
        # debug info
        print "Successfully initialized!"

        # initialize all fields in packet header structure
        self.version = 1
        self.flags = 0
        self.opt_ptr = 0
        self.protocol = 0
        self.header_len = 80 # the length of header in number of bytes
        self.checksum = 0
        self.source_port = 0
        self.dest_port = 0
        self.sequence_no = 0
        self.ack_no = 0
        self.window = 0
        self.payload_len = 0
        # pack the initial struct
        # self.header = self.autopack()

        return
    
    def bind(self,address):
        # bind to a receiving port Rx
        return 

    def connect(self,address):  # fill in your code here 
        # Generate sequence number
        self.sequence_no = random.randint(1, 100)
        # set syn flag
        self.flags = SOCK352_SYN
        # set ack_no
        self.ack_no = -1
        # pack the message
        header = self.autopack()
        # send the message to transmitter
        self.ack_no = -1
        while (self.ack_no != self.sequence_no+1):        
            self.udpSocket.sendto(header, PORTTX)
            print "Try to connect..."
            try:
                recv_string, portnum = syssock.recvfrom(4096)
            except syssock.timeout:
                print("Fail to establish connection!")
                continue

            if len(recv_string) is not None:
                # unpack the message from server
                recv_header = udpPkt_hdr_data.unpack(recv_string)
                # if no connection before
                if(recv_header[1] == SOCK352_SYN)
                    print "No connection exists before. Connected!"
                    # record the ack_no and seq_no from server
                    self.ack_no = recv_header[9]
                    self.sequence_no = recv_header[8]
                    # send the returning message to server again
                    temp = self.sequence_no
                    self.sequence_no = self.ack_no
                    self.ack_no = temp + 1
                    header = self.autopack()
                    self.udpSocket.sendto(header, PORTTX)
                    break
                # if having existing connection
                elif (recv_header[1] == SOCK352_RESET)
                    self.sequence_no += 1
                    print "Connection already exists. Connected!"
                    break
                else
                    print "Fail to establish connection!"

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
        send_string = ""
        # try to recv the message from client
        while send_string == "":
            send_string, portnum = syssock.recvfrom(4096)
            if len(send_string) != 0:
                # unpack the message from server
                send_header = udpPkt_hdr_data.unpack(send_string)
                if self.flags == 0:  # no connection before
                    self.flags = SOCK352_SYN
                elif self.flags == SOCK352_SYN || self.flags == SOCK352_RESET: # have an existing connection
                    self.flags = SOCK352_RESET
                self.sequence_no = random.randint(1, 100)
                self.ack_no = send_header[8] + 1
        # pack header and send
        header = self.autopack()   
        clientsocket = self
        clientsocket.udpSocket.sendto(header, PORTTX)
        return (clientsocket,portnum)
    
    def close(self):   # fill in your code here
        # close if last packet received; else set close variable 
        return 

    # def send(self,buffer):
    #     def recvthread:
    #         while acks left:
    #             recv acks
    #             mark message acked
    #     # go back n
    #     # send length of file
        
    #     bytessent = 0     # fill in your code here 
    #     while bytesleft:
    #         send bytes
    #         check timeout
    #     return bytesent 
    def send(self,buffer):
        fileSeg, ACKList = fileDivder(buffer)
        segmentNo = len(fileSeg)
        segStartTime = []*segmentNo
        segSendList = [0]*segmentNo

        # keep receiving ACK
        def recvthread():    
            while True:
                totalACK = 0
                for x in xrange(0,segmentNo):
                    totalACK = totalACK + ACKList[x]

                while (totalACK != segmentNo):
                    headerdata = syssock.recvfrom(4096)
                    headerdatalist = headerdata.unpack()
                    # if receive ACK 
                    if (headerdatalist[1] == 4):
                        ACKList[headerdatalist[8]-self.sequence_no] = 1
                        # current sequence number is acked
                        return endTime = time.clock()
            return 0

        # create one thread to keep checking ACKs
        t1 = threading.Thread(target=recvthread)
        t1.start()

        # keep sending segments
        while True:
            totalSent = 0
            for x in xrange(0,segmentNo):
                totalSent = totalSent + segSendList[x]

            sequence = 0
            while (totalSent != segmentNo):

                syssock.send(fileSeg[sequence])
 
                
                segStartTime[sequence] = time.clock()
                segSendList[sequence] = 1

                sequence = sequence + 1
                # check time out
                
                








        # def recvthread:
        #     while acks left:
        #         recv acks
        #         mark message acked
        # go back n
        # send length of file

        
        # bytessent = 0
        # bytesleft = buffer.unpack()


    def recv(self,nbytes):
        # only accept expected packets
        # send acks
        # return number of bytes received
        # reassemble packets
        bytesreceived = 0     # fill in your code here
        return bytesreceived 

    def autopack():
        return udpPkt_hdr_data.pack(self.version, self.flags, self.opt_ptr, self.protocol, self.checksum, 
            self.source_port, self.dest_port, self.sequence_no, self.ack_no, self.window, self.payload_len)

    # divide a buffer into several segments 
    # return a list of file segments and a list of ACK list
    def fileDivder(self, buffer):
        # delcare a list of file segments
        if sys.getsizeof(buffer)%65536 == 0:
            fileSeg = []*sys.getsizeof(buffer)%65536
        else
            fileSeg = []*(sys.getsizeof(buffer)/65536+1)

        for x in xrange(0,len(fileSeg)):
            fileSeg[x] = buffer[x*65536:(x+1)*65536]

        # declare a list of ACK
        # 0 indicates not yet acked
        # 1 indicates acked
        ACKList = []*len(fileSeg)
        for x in xrange(0,len(ACKList)):
            ACKList[x] = 0

        return fileSeg, ACKList

    


