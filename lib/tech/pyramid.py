import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech.python import Python


class Pyramid (Python):
	techDescription = 'Pyramid is a very general open source Python web framework.'

	def __init__ (self, **kwargs):
		super (Pyramid, self).__init__ (**kwargs)

		self.projectName = self.serverName.replace ('.', '_')

		self.socket = '127.0.0.1:6543'

		self.nginxConf['server']['location'] = {
			'/'      :
				{
					'proxy_pass'      : 'http://{}'.format (self.socket),
					'proxy_set_header': [
						'Host $http_host',
						'X-Real-IP $remote_addr',
						'X-Forwarded-Proto $scheme',
						'X-Forwarded-For $proxy_add_x_forwarded_for'
					]
				},
			'/static': {
				'alias'    : CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], self.projectName, self.projectName, 'static'),
				'autoindex': 'on'
			}
		}

		self.nginxConf['server']['root'] = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], self.projectName)

		self.confFile = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], self.projectName, 'development.ini')

		self.serverStart = 'gunicorn -D --paste {}'.format (self.confFile)

	def configCreate (self):
		pass

	def load (self):
		try:
			if self.checkGunicorn ():
				destinationDir = CreatePath (CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root']))

				os.chdir (destinationDir)
				os.system ('pip install --upgrade pyramid')
				os.system ('pcreate -s starter {}'.format (self.projectName))

				os.chdir (os.path.join (destinationDir, self.projectName))
				os.system ('python setup.py develop')

				print ('Новая версия Pyramid успешно загружена!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Pyramid по причине отсутствия Gunicorn')
				return False
		except:
			print ('Ошибка загрузки Pyramid!')
			return False
