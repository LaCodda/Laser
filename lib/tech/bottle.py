import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech.python import Python


class Bottle (Python):
	techDescription = 'Bottle is a fast, simple and lightweight WSGI micro web-framework for Python.'

	def __init__ (self, **kwargs):
		super (Bottle, self).__init__ (**kwargs)

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
			'/static': {
				'alias'    : CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], 'static'),
				'autoindex': 'on'
			}
		}

		self.techConf = {
			'pythonpath': CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root']),
			'bind'      : 'unix:' + self.socket,
			'workers'   : 4,
		}

		self.confFile = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['config'], 'gunicorn_config.py')

		self.serverStart = 'gunicorn -c {} -D {} --reload'.format (self.confFile, 'index:app')

	def load (self):
		try:
			if self.checkGunicorn ():
				demoIndexPage = '''import bottle
from bottle import route, run, template

@route('/')
def index():
     return template('<b>Hello {{name}}</b>!', name='Bottle')

@route('/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

app = bottle.default_app()'''
				destinationDir = CreatePath (self.nginxConf['server']['root'])
				destinationFile = CreatePath (destinationDir, 'index.py')
				os.chdir (destinationDir)
				fw = open (destinationFile, "wt")
				fw.write (demoIndexPage)
				fw.close ()
				print ('Демонстрационный файл успешно создан!')
				os.system ('pip install --upgrade bottle')
				print ('Новая версия Bottle успешно загружена!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Bottle по причине отсутствия Gunicorn')
				return False
		except:
			print ('Ошибка загрузки Bottle!')
			return False
