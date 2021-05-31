#!/usr/bin/env python3
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

color=lambda tuple_: sum([tuple_[i]<<(8*i) for i in range(len(tuple_))])

if len(sys.argv)!=4: # chech count of arguments
	print(f'usage: {sys.argv[0]} <path to base image> '
		'<path to secret data> <path to final image>\n'
		f'example: {sys.argv[0]} base.png secret.bin out.png')
	print('exit codes:\n'
		'1: cannot find Pillow ( install Pillow )\n'
		'2: cannot find base image\n'
		'3: base file is not image ( select base image )\n'
		'4: cannot find secret data file\n'
		'5: secret data is too big ( you need to enlarge header size (hardcoded but may be changed) )\n'
		'6: base file is too small ( you need to use larger base file )\n'
		'7: unknown file extension ( you need to use another file extension eg .png )\n'
		'8: unknown error. if you see this error, please send bug report to nikita@okic.ru')
	exit(0)

sys.argv.pop(0) # remove self from args

try:
	img=Image.open(sys.argv.pop(0)) # try to load base image
except FileNotFoundError:
	print('base image not found')
	exit(2)
except UnidentifiedImageError:
	print('base file is not image')
	exit(3)

img.convert('RGBA')

bpc=2 #bits per color channel. recommended 2
hs=2  #head size. max secret file size equals 256**hs bytes

try:
	with open(sys.argv.pop(0),'rb') as f: # open secret data file
		data=f.read()
		data=len(data).to_bytes(hs,'little')+data #concatenate two bytes of length to data
		data=bytearray(data)
except FileNotFoundError:
	print('secret file not found')
	exit(4)
except OverflowError:
	print('secret data is too big')
	exit(5)

try:
	for x in range(img.size[0]): # iterate through all pixels
		if len(data)==0: #used to speed up program
			break
		for y in range(img.size[1]):
			if len(data)==0: #used to speed up program
				break
			byte=data.pop(0) # get one byte of data
			pix=list(img.getpixel((x,y))) #get pixel normal color
			for i in range(len(pix)): #always 4, RGBA
				pix[i]=((pix[i]>>bpc)<<bpc)+byte%(1<<bpc) # drop last <bpc> bits and concatenate new <bpc>
				byte=byte>>bpc
			if byte:
				data.insert(0,byte)
			img.putpixel((x,y),color(pix)) #set new color of pixel
except Exception as ex:
	print('unknown error:',type(ex),ex)
	print('please, send this bug report to nkudravcev49@gmail.com')
	exit(8)

if len(data)>0:
	print('base file is too small for this secret data')
	exit(6)

try:
	img.save(sys.argv.pop(0)) # save as <path to final image>
except (KeyError, ValueError) as ex:
	print(ex)
	print('can you mean ".png"?')
	exit(7)
