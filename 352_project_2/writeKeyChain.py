import binascii 
import nacl.utils
import nacl.secret
import nacl.utils

from nacl.public import PrivateKey, Box


def writeKeyChain():
	file = open("keychain.txt","w")
	# generate wild card private key at the first line
	wildcardPrivKey = PrivateKey.generate()
	wildcardPrivKeyHex = wildcardPrivKey.encode(encoder=nacl.encoding.HexEncoder)
	file.write("private * * "+wildcardPrivKeyHex+"\n")

	# assume there is only one local host and 4 port numbers in a list
	host = "localhost"
	ports = ["8888","9999","7777","6666"]

	for i in xrange(0,len(ports)):
		# generate a pair for each host and port
		pair = {host,ports[i]}
		# generate private key 
		pairPrivKey = PrivateKey.generate()
		pairPrivKeyHex = pairPrivKey.encode(encoder=nacl.encoding.HexEncoder)
		file.write("private "+host+" "+ports[i]+" "+pairPrivKeyHex+"\n")
		# generate cooresponding public key
		pairPublKey = pairPrivKey.public_key
		pairPublKeyHex = pairPublKey.encode(encoder=nacl.encoding.HexEncoder)
		file.write("public "+host+" "+ports[i]+" "+pairPublKeyHex+"\n")

	file.close()



writeKeyChain()