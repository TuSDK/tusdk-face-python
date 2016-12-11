# -*- coding: utf-8 -*-

import time
import hashlib
import requests

#Api服务地址
API_URL = 'https://srv.tusdk.com/srv/face/'

class Face(object):
	"""TuSDK 人脸api服务 接口请求示例类.

	Attributes:
		_params: 请求初始化参数
		_file: 需要POST的图片文件路径

	"""

	_params = {}

	_file = None

	def __init__(self, pid, key):
		self.key = key
		self._params['pid'] = pid

	def request(self, method, file='', url='', **params):
		"""api请求方法.

		Args:
			method: api接口方法
			params: api接口参数

		Returns:
			api返回json字符串

		Raise:
			requests.exceptions.RequestException
		"""

		if (file):
			self._file = file
		elif (url):
			self._params['url'] = url
		else:
			raise TuError('File or url parameter is required')

		playload = dict(self._params) if len(params) == 0 else dict(self._params, **params)
		playload['t'] = int(time.time())
		playload['sign'] = self.signature(playload)
		
		#如果有文件参数, 设置 requests.post files参数
		files = None		
		if self._file != None:
			files = {'pic': open(self._file, 'rb')}

		apiUrl = API_URL + method
		r = requests.post(apiUrl, data=playload, files=files)
		if r.status_code == 200:
			return r.json()
		else:
			return None		

	def signature(self, params):
		"""获取API参数签名.

		Args:
			params: 参数列表dict

		Returns:
			对参数签名的结果字符串

		"""
		#排序并转换参数名为小写
		params = [k.lower() + str(params[k]) for k in sorted(params)]

		#加上私有key
		signStr = "".join(params) + self.key
		#返回md5值
		md5 = hashlib.md5()	
		md5.update(signStr.encode('utf-8'))
		return md5.hexdigest()	

class TuError(Exception):
	pass