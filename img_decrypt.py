#!/usr/bin/env python3

config={
  'bpc':2, #bits per color channel. recommended 2
  'hs':2,  #head size. max secret file size equals 256**hs bytes
}

hs=config.get('hs',2)
bpc=config.get('bpc',2)

try:
  from PIL import Image, UnidentifiedImageError
except ImportError:
  print('please install Pillow\npip install Pillow')
  exit(1)

try:
  import sys
except ImportError:
  print('cannot import sys. wtf?') # what must happen for someone to see it?
  exit(66)

if len(sys.argv)!=3 or any([i in sys.argv for i in ('--help','--usage','-h')]):
	print(f'usage: {sys.argv[0]} <path to image> <path to outfile>')
	print(f'example: {sys.argv[0]} image.png secret.bin')
	print('exit codes:\n'
		'1: cannot find Pillow ( install Pillow )\n'
		'2: cannot find image\n'
		'3: file is not image ( select image )\n'
		'8: cannot write to outfile\n'
		'9: broken image')
	exit()

sys.argv.pop(0) # remove self from args

try:
	img=Image.open(sys.argv.pop(0)) # try to load base image
except FileNotFoundError:
	print('image file not found')
	exit(2)
except UnidentifiedImageError:
	print('file is not image')
	exit(3)

data=bytearray()


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
	print('broken image')
	exit(9)

#for _ in range(hs):
#	data.pop(0) #remove length mark

while length<len(data): # remove not used bytes
	data.pop()

try:
	with open(sys.argv.pop(0),'wb') as f:
		f.write(data)
except (PermissionError, FileNotFoundError) as ex:
	print('Cannot write to',ex.filename)
	exit(8)
