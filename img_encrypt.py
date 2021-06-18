#!/usr/bin/env python3

config={
	'bpc':3, #bits per color channel. recommended 2
	'hs':3,  #head size. max secret file size equals 256**hs bytes
}

hs=config.get('hs',2)
bpc=config.get('bpc',2)

try:
	from PIL import Image, UnidentifiedImageError
except ImportError:
	print('please install Pillow\npip install Pillow')
	exit(1)

import bytegen as bg

try:
	import sys
except ImportError:
	print('cannot import sys. wtf?') # what must happen for someone to see it?
	exit(66)

suml=lambda tuple_: sum([tuple_[i]<<(8*i) for i in range(len(tuple_))])

if len(sys.argv)!=4 or any([i in sys.argv for i in ('--help','--usage','-h')]): # chech count of arguments
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
		'8: cannot write to outfile')
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

img=img.convert('RGBA')



try:
	with open(sys.argv.pop(0),'rb') as f: # open secret data file
		data=f.read()
		data=len(data).to_bytes(hs,'big')+data #concatenate two bytes of length to data
		data=bytearray(data)
except FileNotFoundError:
	print('secret file not found')
	exit(4)
except OverflowError:
	print('secret data is too big')
	exit(5)

binary=bg.bytes_iter(data)
done=False

for x in range(img.size[0]): # iterate through all pixels
	if done: #used to speed up program
		break
	for y in range(img.size[1]):
		if done: #used to speed up program
			break
		pix=list(img.getpixel((x,y))) #get pixel normal color
		for j in range(len(pix)): #always 4, RGBA
			try:
				pix[j]>>=bpc
				for _ in range(bpc):
					pix[j]<<=1
					pix[j]+=binary.__next__()
			except StopIteration:
				done=True
		img.putpixel((x,y),suml(pix)) #set new color of pixel

try:
	binary.__next__()
	# not ok
	print('base file is too small for this secret data')
	exit(6)
except:
	pass #ok

try:
	img.save(sys.argv.pop(0)) # save as <path to final image>
except (KeyError, ValueError) as ex:
	print(ex)
	print('can you mean ".png"?')
	exit(7)
except (PermissionError, FileNotFoundError) as ex:
  print('Cannot write to',ex.filename)
  exit(8)
