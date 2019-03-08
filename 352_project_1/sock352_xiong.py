
import binascii
import socket as syssock
import struct
import sys

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

SOCK352_SYN = 1    # Connection initiation
SOCK352_FIN = 2    # Connection end
SOCK352_ACK = 4    # Acknowledgement
SOCK352_RESET = 8  # Reset the connection
SOCK352_HAS_OPT = 10    # Option field is valid


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
    # setup udp socket
    if(!udpSocket)
        udpSocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    # bind to receiver port
    udpSocket.bind(('', PORTRX))
    # set timeout
    udpSocket.settimeout(0.2)
    # debug info
    print "Successfully initialized!"
    
    pass 
    
class socket:
    
    def __init__(self):  # fill in your code here 
        # create sockets?

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
        self.header = autopack()

        return
    
    def bind(self,address):
        # bind to a receiving port Rx
        return 

    def connect(self,address):  # fill in your code here 
        # Generate sequence number
        do
            sequence_No = random.randint(1, 100)
        while
            sequence_No != self.sequence_no
        self.sequence_no = sequence_No
        # change flags
        self.flags = 1
        # set ack_no
        self.ack_no = -1
        # pack the message
        header = autopack()
        # send the message to transmitter (i.e. the other machine's receiver port)
        recv_SYN = -1
        recv_ACK = -1
        while (recv_ACK != self.sequence_no+1)
            udpSocket.sendto(header, PORTTX)
            print "Try to connect..."
            recv_string, portnum = recvfrom(4096)
            recv_header = udpPkt_hdr_data.unpack(recv_string)
            recv_ACK = getACK()
            # if no connection before
            if(checkflag(recv_header) == SOCK352_SYN || checkflag(recv_header) == SOCK352_ACK)
                print "No connection before. Connected!"
                break
            # if having existing connection
            elif (checkflag(recv_header) == SOCK352_RESET)
                print "Existing connection. Connected!"
                break
            else
                print "Unable to connect!"

        return 
    
    def listen(self,backlog):
        # find size of socket array
        return

    def accept(self): # create connection from server side; 
        (clientsocket, address) = (1,1)  # change this to your code 
        clientsocket = self
        # other option
        # self.socket = [socket ... ]   #socket list
        # clientsocket = self.socket[0]
        return (clientsocket,address)
    
    def close(self):   # fill in your code here
        # close if last packet received; else set close variable 
        return 

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
                    if (headerdatalist[1] = 4):
                        ACKList[headerdatalist[8]-self.sequence_no] = 1
                        # current sequence number is acked
                        return endTime = time.clock()
            return 0

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

            


