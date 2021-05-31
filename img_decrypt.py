from PIL import Image
import sys

color=lambda tuple_: sum([tuple_[i]<<(8*i) for i in range(len(tuple_))])

sys.argv.pop(0)

img=Image.open(sys.argv[0])

data=bytearray()
pos=2
length=-1

bpc=2 # bits per channel. recommended 2

for x in range(img.size[0]):
	if length==0:
		break
	for y in range(img.size[1]):
		if length==0:
			break
		pix=img.getpixel((x,y))
		if pos>0:
			pos-=1
		if length>0:
			length-=1
		if length:
			byte=0
			for i in pix[::-1]:
				byte=(byte<<bpc)+i%(1<<bpc)
			data.append(byte)
		if pos==0:
			length=int.from_bytes(data,'little')+1
			full_length=length
			data=bytearray()
			pos=-1
#			print(length)
#			exit()
#			print(data)
#		img.putpixel((x,y),color(pix)) # argb
#		img.putpixel((x,y),0xffff00ff) # argb

#print(data)
#print(data.bit_length())
#print(full_length)
with open('out.bin','wb') as f:
	f.write(data)
#img.save('b.png')
