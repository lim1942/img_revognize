import json
import execjs  
import random
import requests
from lxml import etree

from img_handle import recognize


def login():

	param_dict = dict()
	user_name = 'reader'
	param_dict['i'] = user_name
	user_pwd = 'trsreader@123'
	param_dict['p'] = user_pwd

	headers = {
	"Host":"10.200.73.10:5555",
	"Connection":"keep-alive",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
		"/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"),
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,imag"
		"e/webp,image/apng,*/*;q=0.8",
	"Referer":"http://10.200.73.10:5555/admin/protected/main.do?p=status",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"zh-CN,zh;q=0.9",
	}


	# 1.get session id for index
	try:
		base_url = 'http://10.200.73.10:5555/admin/index.jsp'
		r = requests.get(base_url,headers=headers)
		if r.status_code == 200:
			#for login issue	
			xml = etree.HTML(r.text)
			currenttime = xml.xpath("//input[@id='currenttime']/@value")[0]
			param_dict['t'] = currenttime
			currentrandom = xml.xpath("//input[@id='currentrandom']/@value")[0]
			param_dict['r'] = currentrandom
			modulus = xml.xpath("//input[@id='modulus']/@value")[0]
			exponent = xml.xpath("//input[@id='exponent']/@value")[0]
			cookies =  r.cookies.get_dict()
		else:
			raise Exception('status_code error 1 get index error')
	except Exception as e:
		print(e,'something wrong...')
		return


	# 2.get captcha image
	try:
		img_url = 'http://10.200.73.10:5555/admin/verifycode.do?r={}'.format(random.random())
		r = requests.get(img_url,headers=headers,cookies=cookies)
		if r.status_code == 200:
			cap_content = r.content
			cap_name = 'captcha.jpg'
			with open(cap_name,'wb') as f:
				f.write(cap_content)
		else:
			raise Exception('status_code error 2 get captcha error')
	except Exception as e:
		print(e,'something wrong...')
		return


	# 3.use tesseract-ocr recognize captcha`s value
	cap_value = recognize(cap_name)


	# 4.login to active session-id for spider
	try:
		login_url = 'http://10.200.73.10:5555/admin/login.do'
		data = json.dumps(param_dict)

		# use execjs run js_code to get encrypted data 
		js_file = open("security.js","r")
		js_code = js_file.read()
		ctx = execjs.compile(js_code)  
		data = ctx.call('my_help',exponent,modulus,data)

		data = {'logindata':data,'randcode':cap_value}
		r = requests.post(login_url,data=data,cookies=cookies,headers=headers,allow_redirects=False)
		if r.status_code == 302:
			print('Congratulation login successful !!!  you can use this cookie ...')
			cookies = r.cookies.get_dict()
			print(cookies)
			with open('cookies','w') as f:
				f.write(str(cookies))
			return cookies
		else:
			raise Exception('status_code error 3 login error')
	except Exception as e:
		print (e,'something wrong...')



if __name__ == '__main__':
	login()
