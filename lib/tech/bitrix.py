import os
import shutil
import sys
import tarfile
import urllib.request

from lib.helper import *
from lib.tech.php import Php


class Bitrix (Php):
	techDescription = 'Bitrix Description'

	def __init__ (self, **kwargs):
		super (Bitrix, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'               :
				{
					'try_files': '$uri $uri/ /index.php?$args'
				},
			'~ [^/]\.php(/|$)':
				{
					'fastcgi_index'       : 'index.php',
					'include'             : 'fcgi.conf',
					'fastcgi_pass'        : 'unix:' + self.socket,
					'fastcgi_param'       : 'SCRIPT_FILENAME $document_root$fastcgi_script_name',
					'fastcgi_read_timeout': '300',
				}
		}

		self.techConf = {
			'user'                : 'vagrant',
			'group'               : 'www-data',
			'listen'              : self.socket,
			'listen.owner'        : 'www-data',
			'listen.group'        : 'www-data',
			'listen.mode'         : '0660',
			'pm'                  : 'dynamic',
			'pm.max_children'     : '5',
			'pm.start_servers'    : '1',
			'pm.min_spare_servers': '1',
			'pm.max_spare_servers': '5',
			'php_admin_value'     : {
				'open_basedir'              : 'none',
				'error_reporting'           : 'E_ALL & ~E_NOTICE & ~E_WARNING',
				'display_errors'            : 'On',
				'display_startup_errors'    : 'On',
				'short_open_tag'            : 'On',
				'max_execution_time'        : '0',
				'session.gc_maxlifetime'    : '100000',
				'mbstring.func_overload'    : '0',
				'mbstring.internal_encoding': 'windows-1251',
				'default_charset'           : 'windows-1251',
				'date.timezone'             : 'Europe/Samara',
				'max_input_vars'            : '10000',
				'post_max_size'             : '200M',
				'upload_max_filesize'       : '200M',
				'sendmail_path'             : '/usr/sbin/ssmtp -t',
				'session.use_cookies'       : '1',
				'session.use_only_cookies'  : '1',
				'opcache.revalidate_freq'   : '0',
			}
		}

	def load (self):
		try:
			url = 'http://dev.1c-bitrix.ru/download/scripts/'
			files = ['bitrixsetup.php', 'restore.php', 'bitrix_server_test.php']
			destinationDir = CreatePath (self.nginxConf['server']['root'])
			for file in files:
				urllib.request.urlretrieve (url + file, CreatePath (destinationDir, file))
			print ('Новая версия файла bitrixsetup.php успешно загружена!')
			return True
		except:
			print ('Ошибка загрузки bitrixsetup.php')
			return False

	def install (self):
		try:
			url = 'http://dev.1c-bitrix.ru/download/scripts/'
			files = ['bitrixsetup.php', 'restore.php', 'bitrix_server_test.php']
			destinationDir = CreatePath (self.nginxConf['server']['root'])
			for file in files:
				urllib.request.urlretrieve (url + file, CreatePath (destinationDir, file))
			print ('Новая версия файла bitrixsetup.php успешно загружена!')
			return True
		except:
			print ('Ошибка загрузки bitrixsetup.php')
			return False
