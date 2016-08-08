import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech import Tech


class Python (Tech):
	techDescription = 'Python Description'

	config = ''

	def __init__ (self, **kwargs):
		super (Python, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/':
				{
					'proxy_pass'      : 'http://unix:' + self.socket,
					'proxy_set_header': [
						'Host $http_host',
						'X-Real-IP $remote_addr',
						'X-Forwarded-Proto $scheme',
						'X-Forwarded-For $proxy_add_x_forwarded_for'
					]
				}
		}

		self.techConf = {
			'pythonpath': CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root']),
			'bind'      : 'unix:' + self.socket,
			'workers'   : 4,
		}

		self.confFile = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['config'], 'gunicorn_config.py')

		self.serverStart = 'gunicorn -c {} -D {} --reload'.format (self.confFile, 'index:app')

		self.serverStop = 'sudo pkill -f gunicorn'

	def load (self):
		try:
			if self.checkGunicorn ():
				demoIndexPage = '''def app(environ, start_response):
	data = b"Hello, World!"
	start_response("200 OK", [
		("Content-Type", "text/plain"),
		("Content-Length", str(len(data)))
	])
	return iter([data])'''
				destinationDir = CreatePath (self.nginxConf['server']['root'])
				destinationFile = CreatePath (destinationDir, 'index.py')
				os.chdir (destinationDir)
				fw = open (destinationFile, "wt")
				fw.write (demoIndexPage)
				fw.close ()
				print ('Демонстрационный файл успешно создан!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Python по причине отсутствия Gunicorn')
				return False
		except:
			print ('Ошибка загрузки Python!')
			return False

	def configCreate (self):
		for confKey, confValue in self.kwargs['techConf'].items ():
			if isinstance (confValue, int):
				self.config += "{} = {}\n".format (confKey, confValue)
			else:
				self.config += "{} = '{}'\n".format (confKey, confValue)
		fw = open (self.kwargs['confFile'], "wt")
		fw.write (self.config)
		fw.close ()

	def start (self):
		# TODO: заменить более правильным решением
		os.system (self.kwargs['serverStart'])

	def stop (self):
		# TODO: заменить более правильным решением
		os.system (self.kwargs['serverStop'])

	def checkGunicorn (self):
		try:
			path = shutil.which ("gunicorn")
			if path:
				return True
			else:
				return self.installGunicorn ()
		except:
			print ('Ошибка выполнения проверки установки Gunicorn!')
			return False

	def installGunicorn (self):
		try:
			os.system ('pip install gunicorn')
			print ('Новая версия Gunicorn успешно установлена!')
			return True
		except:
			print ('Ошибка установки Gunicorn!')
			return False
