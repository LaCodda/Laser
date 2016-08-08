import os
import shutil
import sys
import tarfile
import urllib.request

from lib.helper import *
from lib.tech.php import Php


class Yii (Php):
	techDescription = 'Yii is a high-performance PHP framework best for developing Web 2.0 applications'

	def __init__ (self, **kwargs):
		super (Yii, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'                                                    : {
				'index'    : 'index.php',
				'try_files': '$uri $uri/ /index.php$is_args$args',
			},
			'~ \.(js|css|png|jpg|gif|swf|ico|pdf|mov|fla|zip|rar)$': {
				# включать только после  прочтения этого http://ruhighload.com/post/%D0%9A%D0%B0%D0%BA+%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BD%D0%BE+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C+Cache-control+%D1%81+%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D1%8F%D0%B5%D0%BC%D0%BE%D0%B9+%D1%81%D1%82%D0%B0%D1%82%D0%B8%D0%BA%D0%BE%D0%B9
				# expires max
				'try_files': '$uri =404',
			},
			'~ ^/(protected|framework|themes/\w+/views)'           : {
				'deny': 'all',
			},
			'~* \.(php)$'                                          : {
				'fastcgi_pass'             : 'unix:' + self.socket,
				'fastcgi_index'            : 'index.php',
				'include'                  : 'fcgi.conf',
				'fastcgi_param SCRIPT_NAME': '$document_root$fastcgi_script_name',
			},
			'~ /\.'                                                : {
				'deny'         : 'all',
				'log_not_found': 'off',
			},

		}

	def load (self):
		try:
			destinationDir = CreatePath (self.nginxConf['server']['root'])
			fileName = 'yii-1.1.17.467ff50'
			sourceDir = CreatePath (destinationDir, fileName)
			arcSourceName = 'latest.tar.gz'
			arcSourcePath = CreatePath (destinationDir, arcSourceName)
			urllib.request.urlretrieve ('https://github.com/yiisoft/yii/releases/download/1.1.17/' + fileName + '.tar.gz', arcSourcePath)
			tar = tarfile.open (arcSourcePath)
			tar.extractall (destinationDir)
			tar.close ()
			sourceList = os.listdir (sourceDir)
			for files in sourceList:
				shutil.move (CreatePath (sourceDir, files), destinationDir)
			os.rmdir (sourceDir)
			os.remove (arcSourcePath)
			print ('Новая версия Yii успешно загружена!')
			return True
		except:
			print ('Ошибка загрузки Yii!')
			return False
