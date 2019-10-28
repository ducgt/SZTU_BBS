# 项目：SZTU_BBS
# 文件名：upload_notice
# 创建时间：2019-08-12
# 仅在校园网环境下运行
from notice.models import Notice
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from PIL import Image

import sys
import logging
import requests
from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
from datetime import date

dir = ['student_work','school_life']

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = '********************************'      # 替换为用户的 secretId
secret_key = '********************************'      # 替换为用户的 secretKey
region = '********************************'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

def upload_image(path, title, part):
	add_water_mask(path)
	key = 'notic_image/{}/{}.png'.format(dir[part],title)
	client.upload_file(
		Bucket='********************************',
		LocalFilePath=path,
		Key=key
	)
	print(client._conf.uri(bucket='********************************', path=key))
	return client._conf.uri(bucket='********************************', path=key)


def add_water_mask(path):
	img = Image.open(path)
	logo = Image.open('logo.png')
	logo = logo.convert('RGBA')
	x, y = logo.size
	x_, y_ = img.size

	for i in range(x):
		for k in range(y):
			color = logo.getpixel((i, k))
			if color[:-1] == (255, 255, 255):
				color = color[:-1] + (0,)
			else:
				color = color[:-1] + (30,)
			logo.putpixel((i, k), color)

	layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
	layer.paste(logo, (int((x_ - x) / 2), 300))
	out = Image.composite(layer, img, layer)
	out.save(path)


def get_notice_screenshot(url_list, title_list, part):
	chromedriver:str = r'D:\软件\chromedriver.exe'
	geturl:str = 'http://10.1.0.29'

	src:list = []
	sum:int = len(url_list)
	done:int =0
	option = webdriver.ChromeOptions()
	option.add_argument('--headless')
	browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=option)
	browser.get(geturl)
	browser.execute_script("Sub('/WebUsers/NewsReadList.aspx?typeSubclass=0')")
	for (url, title) in zip(url_list, title_list):
		if Notice.objects.filter(title=title,part=part).count()==0:
			browser.get(r'http://10.1.0.29/WebUsers/'+url)
			scroll_height = browser.execute_script('return document.body.parentNode.scrollHeight')
			browser.set_window_size(1100,scroll_height)
			browser.get_screenshot_as_file('{}/{}.png'.format(dir[part], title))
			done += 1
			src.append(r'{}/{}.png'.format(dir[part], title))
			print('{}网页截图进度:{}/{}'.format(dir[part], done, sum))
		else:
			done += 1
			print('该公文已存在,{}网页截图进度:{}/{}'.format(dir[part],done, sum))
			src.append(False)
	return src


# part的值 0代表学生工作，1代表校园生活
def get_all_screenshot(part):
	COOKIES = {'ASP.NET_SessionId':'wipvggzuls3prciydhe5hkrw',
				'C_UserName': 'eMhx4XzFQu7i+DQ+JTEQuQ==',
				'C_User_UserName':'eMhx4XzFQu7i+DQ+JTEQuQ=='}

	sess = requests.session()
	requests.utils.add_dict_to_cookiejar(sess.cookies, COOKIES)
	res = sess.get('http://10.1.0.29/WebUsers/NewsReadList.aspx?typeSubclass={}'.format(part+4))
	soup = BeautifulSoup(res.text, 'html.parser')

	tbody = soup.find('tbody')
	tbody_list = tbody.find_all('tr')
	# 抽取表头
	table_head = [i.string for i in tbody_list[0].find_all('th')]
	# 抽取表格内容
	table_body = [[j.string for j in i.find_all('td')] for i in tbody_list]
	# 合并表头与内容
	table_body[0] = table_head
	table = np.array(table_body)  # table即为表格矩阵
	# print(table)
	# print(table[:, 3][1:])
	# print(len(table[:, 3]))

	# 获取公文通内容链接
	href = [i.find_all('td')[3].a.get('href') for i in tbody_list[1:]]
	print(href)

	return get_notice_screenshot(href, table[:, 3][1:], part), table[1:]


def create_notice(image_path, date_str, title, part):
	_date = date(*map(int, date_str.split('-')))
	_notice = Notice(part=part,
					 date=_date,
					 detail_image_url=upload_image(image_path, title, part),
					 title=title)
	_notice.save()
	print(_notice.id,_notice.title)
	print('成功上传:',_notice.title)


def run():
	for i in [0, 1]:
		paths, table = get_all_screenshot(i)
		for j in range(len(paths)):
			if paths[j]:
				create_notice(paths[j],table[j][5],table[j][3],i)
				print('新建公文通进度:{}/{}'.format(j+1, len(paths)),paths[j])
			else:
				print('新建公文通进度:{}/{}'.format(j+1, len(paths)),paths[j])
