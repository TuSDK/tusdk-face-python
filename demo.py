# -*- coding: utf-8 -*-
#TuSDK 人脸api 请求示例


from TuSDK.face import *

def main():
	#请修改为您的 公有key
	pid = ''
	#请修改为您的 私有key
	key = ''

	try:
		#初始化
		face = Face(pid, key)		
				
		detectionData = face.request('detection', file="path_to_file")
		print(detectionData)

	except BaseException as e:
		print(e)	


if __name__ == '__main__':
	main();

