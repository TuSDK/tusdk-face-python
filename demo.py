# -*- coding: utf-8 -*-
# TuSDK 人脸 API 请求示例

from tusdk.face import *


def main():
	# 请修改为您的公有 key
	pid = ''
	# 请修改为您的私有 key
	key = ''

	try:
		# 初始化
		face = Face(pid, key)

		faces = face.request('detection', file="path_to_file")
		print(faces)

	except BaseException as e:
		print(e)

if __name__ == '__main__':
	main()
