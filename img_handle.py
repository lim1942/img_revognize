import os
from PIL import Image, ImageFile


def bin_handle(filename,new_name):

	"""bin code"""
	img = Image.open(filename)
	img = img.convert('L')
	pix_ = img.load()
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if  pix_[x,y]<=120:
				pix_[x,y] = 0
			if pix_[x,y]>120:
				pix_[x,y] =255

	img.save(new_name)



def recognize(filename):

	# handle captcha
	new_name = filename.replace('.jpg','')+ '_bin.jpg'
	bin_handle(filename,new_name)

	#recognize
	os.system("tesseract {} result -psm 7 digits 2>NUL 1>NUL".format(new_name))

	#return
	with open('result.txt') as f:
		result = f.read().strip()[0:4]
	return result


if __name__ == '__main__':
	print(recognize('captcha.jpg'))


	
