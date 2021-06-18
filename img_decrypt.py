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
import bytegen as bg

def get_data_from_image(img):
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			pix=img.getpixel((x,y))
			for i in pix:
				buf=i&((1<<bpc)-1)
				for yi in bg.int_iter(buf, bpc):
					yield yi


def parse_data(img):
	bits=byte=head=hl=0
	iterator=bg.assembly(get_data_from_image(img))
	for i in iterator:
		if hl!=hs:
			head<<=8
			head+=i
			hl+=1
		else:
			head-=1
			yield i
			if head==0:
				break



try:
	with open(sys.argv.pop(0),'wb') as f:
		f.write(bytearray(parse_data(img)))
except (PermissionError, FileNotFoundError) as ex:
	print('Cannot write to',ex.filename)
	exit(8)
