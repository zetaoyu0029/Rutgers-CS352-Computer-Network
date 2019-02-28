
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
PORTTX
PORTRX
sock352PktHdrData
udpPkt_hdr_data

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    # setup header format
    sock352PktHdrData = '!BBBBHHLLQQLL'
    udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
    # setup port numbers
    PORTTX = UDPportTx
    PORTRX = UDPportRx
    pass 
    
class socket:
    
    def __init__(self):  # fill in your code here 
        # initialize all fields in packet header structure
        version = 1
        flags = 0
        opt_ptr = 0
        protocol = 0
        header_len = 292 # the length of header in number of bytes
        checksum = 0
        source_port = 0
        dest_port = 0
        sequence_no = 0
        ack_no = 0
        window = 0
        payload_len = 0
        # pack the initial struct
        header = udpPkt_hdr_data.pack(version, flags, opt_ptr, protocol, checksum, 
            source_port, dest_port, sequence_no, ack_no, window, payload_len)
        return
    
    def bind(self,address):
        return 

    def connect(self,address):  # fill in your code here 
        return 
    
    def listen(self,backlog):
        return

    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 


    


