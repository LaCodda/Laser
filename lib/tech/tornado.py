import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech.python import Python


class Django (Python):
	techDescription = 'Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.'

	def __init__ (self, **kwargs):
		super (Django, self).__init__ (**kwargs)

		self.projectName = self.serverName.replace ('.', '_')

		self.nginxConf['server']['location'] = {
			'/'       :
				{
					'proxy_pass'      : 'http://unix:' + self.socket,
					'proxy_set_header': [
						'Host $http_host',
						'X-Real-IP $remote_addr',
						'X-Forwarded-Proto $scheme',
						'X-Forwarded-For $proxy_add_x_forwarded_for'
					]
				},
			'/static/': {
				'alias': CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], 'static')
			}
		}

		self.nginxConf['server']['root'] = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], self.projectName)

		self.techConf = {
			'pythonpath': self.nginxConf['server']['root'],
			'bind'      : 'unix:' + self.socket,
			'workers'   : 3,
			# 'user': 'nobody',
		}

		self.confFile = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['config'], 'gunicorn_config.py')

		self.serverStart = 'gunicorn -c {} -D {} --reload'.format (self.confFile, self.projectName + '.wsgi')

	def load (self):
		try:
			if self.checkGunicorn ():
				destinationDir = CreatePath (CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root']))
				# destinationFile = CreatePath (destinationDir, 'index.php')
				os.chdir (destinationDir)
				os.system ('pip install Django')
				os.system ('django-admin startproject {}'.format (self.projectName))
				# fw = open (destinationFile, "wt")
				# fw.write (demoIndexPage)
				# fw.close ()
				print ('Новая версия Django успешно загружена!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Django по причине отсутствия Gunicorn')
				return False
		except:
			print ('Ошибка загрузки Django!')
			return False
