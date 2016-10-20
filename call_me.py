import socket
import struct
import binascii
import time
import json
import urllib2

IF_Key = 'abcdefghrcy9SxCN-EcI88rB' # add your key from the IFTTT maker channel
IF_trigger = 'https://maker.ifttt.com/trigger/dash_button_pressed/with/key/' + IF_Key	# trigger event url

button_macs= {'74754a563773' : 'AlienBob'}

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

def trigger_url(url):	# function to send the trigger url
	data = '{ "value1" : "' + time.strftime("%Y-%m-%d") + '", "value2" : "' + time.strftime("%H:%M") + '" }'
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    	f = urllib2.urlopen(req)
    	response = f.read()
    	f.close()
	return response

while True:
	packet = rawSocket.recvfrom(2048)
	ethernet_header = packet[0][0:14]
	ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
	# skip non-ARP packets
	etherType = ethernet_detailed[2]
	if etherType != '\x08\x06':
		continue
	
	# read out the data	
	arp_header = packet[0][14:42]
	arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
	source_mac = binascii.hexlify(arp_detailed[5])
	source_ip = socket.inet_ntoa(arp_detailed[6])
	dest_ip = socket.inet_ntoa(arp_detailed[8])
	
	if source_mac in button_macs:
		print "calling trigger " + trigger_url(IF_trigger)	# multiple client buttons can be added
	else:
		print "Unknown MAC " + source_mac + " from IP " + source_ip
