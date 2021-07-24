#!/usr/bin/python
import socket
import struct
import time
f=open('vlc.pcap', 'rb')
header=struct.unpack('IHHIIII',f.read(24))
print('%#x %#x %#x %#x %#x %#x %#x'%(header[0], header[1],header[2],header[3], header[4],header[5],header[6]) )

lasttime=0
curtime=0;
udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('', 7788))
startcode=struct.pack('!I',1)
print(startcode)
outfile=open("out.264","wb")
while 1:
	packheader=struct.unpack('IIII',f.read(16))
	pkt=f.read(packheader[3])
	rtp=pkt[32:]
	#print(len(pkt))
	rtptime=rtp[4:8]
	curtime=struct.unpack('!I', rtptime)
	#time.sleep(0.01)
	h264_first=struct.unpack('B',rtp[12])[0]
	h264_second=struct.unpack('B',rtp[13])[0]
	#print("%#x %#x" % (h264_first, h264_second))
	if h264_first & 0x1f == 0x07:
		print("SPS and header = 0x%02x"% h264_first)
		outfile.write(startcode)
		outfile.write(rtp[12:])
		
	elif h264_first & 0x1f == 0x08:
		print("PPS and header = 0x%02x" % h264_first)
		outfile.write(startcode)
		outfile.write(rtp[12:])
	elif h264_first & 0x1f == 0x06:
		print("SEI and header = 0x%02x" % h264_first)
		#outfile.write(startcode)
		outfile.write(struct.pack('B', 0x00))
		outfile.write(struct.pack('B', 0x00))
		outfile.write(struct.pack('B', 0x01))
		outfile.write(rtp[12:])
	elif h264_first & 0x1f == 28:
		if lasttime != curtime:
			lasttime = curtime
			print("new key frame")
			#outfile.write(startcode)
			outfile.write(struct.pack('B', 0x00))
			outfile.write(struct.pack('B', 0x00))
			outfile.write(struct.pack('B', 0x01))
			if h264_second & 0x1f == 0x05:
				outfile.write(struct.pack('B', 0x65))
			else:
				outfile.write(struct.pack('B',0x41))
		print("FU-A")
		if h264_second & 0x1f == 0x05:
			print("this is iframe header eq 0x65")
			
			#outfile.write(struct.pack('B', 0x65))
			outfile.write(rtp[14:])
			print(len(rtp[14:]))
		elif h264_second & 0x1f == 0x01:
			print("this is pframe header eq 0x41")
			#outfile.write(struct.pack('B', 0x41))
			outfile.write(rtp[14:])
			print(len(rtp[14:]))
	elif h264_first & 0x1f == 0x01:
		outfile.write(startcode)
		outfile.write(rtp[12:])
		print(len(rtp[12:]))
		print("SINGLE pframe header eq 0x41")	
	else:
		print("unknown")
	#time.sleep(1)
	#print("%#x %#x %#x %#x"%(curtime[0],curtime[1],curtime[2],curtime[3]))
	udp.sendto(rtp, ('127.0.0.1', 1234))
udp.close()
f.close()

