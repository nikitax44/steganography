i2b_=[i.to_bytes(1, 'little') for i in range(256)]
def bytes_iter(data):
	assert (type(data) in (bytes, bytearray))
	data=bytearray(data)
	while len(data):
		buf=data.pop(0)
		for i in int_iter(buf, 8):
			yield i

def int_iter(num, bl=None):
	num<<=1
	if bl==None:
		bl=num.bit_length()
	for i in range(bl):
		y=num>>(bl-i)
#		print(y)
		yield y
		num&=((1<<bl)-1)>>i


def assembly(iterator):
	byte=0
	bits=0
	for i in iterator:
		byte<<=1
		byte+=i
		bits+=1
		if bits==8:
			yield byte
			byte=0
			bits=0
	if bits:
		raise ValueError('bit count is not 8*n')
def i2b(iterator):
	for i in iterator:
		yield i2b_[i]

if __name__=='__main__':
	import time
	st=None
	def timer(message=''):
		global st
		current=time.time()
		if st!=None:
			print(current-st, message)
		st=current

	timer('init timer')

	sample_len=1<<10*1

	sample=__import__('random').randint(0, 1<<8*sample_len).to_bytes(sample_len, 'little')
	timer('sample generation time')
#	with open('secret.txt', 'rb') as f:
#		sample=f.read()

	decoded_sample=assembly(bytes_iter(sample))
	timer('generator creating time')
	for i in range(len(sample)):
		sa=sample[i]
		de=decoded_sample.__next__()
		if sa!=de:
			print(f'at pos {i}: expected {i2b_[sa]}, got {i2b_[de]}')
	timer('verifyng time')
