import os
import shutil
import sys
import tarfile
import urllib.request

from lib.helper import *
from lib.tech.php import Php


class Yii2 (Php):
	techDescription = 'Yii is a high-performance PHP framework best for developing Web 2.0 applications'

	def __init__ (self, **kwargs):
		super (Yii2, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'                                                    : {
				'try_files': '$uri $uri/ /index.php$is_args$args'
			},
			'~ \.php$'                                             : {
				'try_files'                    : '$uri =404',
				'fastcgi_index'                : 'index.php',
				'include'                      : 'fcgi.conf',
				'fastcgi_pass'                 : 'unix:' + self.socket,
				'fastcgi_param SCRIPT_FILENAME': '$document_root$fastcgi_script_name',
				'fastcgi_param SCRIPT_NAME'    : '$fastcgi_script_name',
				'fastcgi_split_path_info'      : '^(.+\.php)(/.+)$',
			},
			'~ \.(js|css|png|jpg|gif|swf|ico|pdf|mov|fla|zip|rar)$': {
				'try_files': '$uri =404',
			},
			'~ ^/assets/.*\.php$'                                  : {
				'deny': 'all',
			},
			'~* /\.'                                               : {
				'deny': 'all',
			}

		}

	def load (self):
		try:
			if self.checkComposer ():
				destinationDir = CreatePath (self.nginxConf['server']['root'])
				os.chdir (destinationDir)
				os.system ('composer require "fxp/composer-asset-plugin:~1.1.1"')
				os.system ('composer create-project yiisoft/yii2-app-advanced advanced 2.0.8')
				print ('Новая версия Yii2 успешно загружена!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Yii2 по причине отсутствия Composer')
				return False
		except:
			print ('Ошибка загрузки Slim!')
			return False
