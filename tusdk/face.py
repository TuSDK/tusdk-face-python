# -*- coding: utf-8 -*-

import time
import hashlib
import requests

# API 服务地址
API_URL = 'https://srv.tusdk.com/srv/face/'


class Face(object):
	"""TuSDK 人脸 API 服务接口请求示例类

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
		"""api 请求方法

		Args:
			method: api 接口方法
			file: 图片文件
			url: 图片 url
			params: api 接口参数

		Returns:
			api 返回 json 字符串

		Raise:
			requests.exceptions.RequestException
		"""

		if file:
			self._file = file
		elif url:
			self._params['url'] = url
		else:
			raise TuError('File or url parameter is required')

		if len(params) == 0:
			playload = dict(self._params)
		else:
			playload = dict(self._params, **params)
		playload['t'] = int(time.time())
		playload['sign'] = self.signature(playload)

		# 如果有文件参数, 设置 requests.post files 参数
		files = None
		if self._file is not None:
			files = {'pic': open(self._file, 'rb')}

		api_url = API_URL + method
		r = requests.post(api_url, data=playload, files=files)
		if r.status_code == 200:
			return r.json()
		else:
			return None

	def signature(self, params):
		"""获取 API 参数签名.

		Args:
			params: 参数列表 dict

		Returns:
			对参数签名的结果字符串

		"""
		# 排序并转换参数名为小写
		params = [k.lower() + str(params[k]) for k in sorted(params)]

		# 加上私有 key
		signature = "".join(params) + self.key
		# 返回 md5 值
		md5 = hashlib.md5()
		md5.update(signature.encode('utf-8'))
		return md5.hexdigest()


class TuError(Exception):
	pass
