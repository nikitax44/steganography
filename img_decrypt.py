#!/usr/bin/env python3
from PIL import Image
import sys

sys.argv.pop(0) # remove self from args

img=Image.open(sys.argv[0]) # open image

data=bytearray()

bpc=2 # bits per channel. recommended 2
hs=2  # header size. secret data size equals 256**hs


done=False
length=-1
bits=0
byte=0

for x in range(img.size[0]):
	if done:
		break
	for y in range(img.size[1]):
		if done:
			break
		pix=img.getpixel((x,y))
		for i in pix[::-1]:
			byte=(byte<<bpc)+i%(1<<bpc)
			bits+=bpc
			while bits>=8: #if is enough, but just in case, I wrote while
				data.append(byte>>(bits-8))
				byte=byte%(1<<(bits-8))
				bits-=8
		if len(data)>=hs:
			if length==-1:
				length=int.from_bytes(data[:hs],'little')
				data=data[hs:]
			if len(data)>=length:
				done=True
if not done:
	print('broken input file')
	exit(2)

#for _ in range(hs):
#	data.pop(0) #remove length mark

#while length<len(data): # remove not used bytes
#	data.pop()

with open('out.bin','wb') as f:
	f.write(data)
