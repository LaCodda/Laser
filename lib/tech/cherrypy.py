import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech.python import Python


class Cherrypy (Python):
	techDescription = 'CherryPy allows developers to build web applications in much the same way they would build any other object-oriented Python program.'

	def __init__ (self, **kwargs):
		super (Cherrypy, self).__init__ (**kwargs)

		self.socket = '127.0.0.1:6544'

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
				'alias'    : CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], 'static'),
				'autoindex': 'on'
			}
		}

		self.techConf = {
			'global': {
				'server.socket_host': "127.0.0.1",
				'server.socket_port': 6544,
				'server.thread_pool': 10,
			},
		}
		# self.techConf = {
		# 	'global': {
		# 		'server.socket_host': 'unix:' + self.socket,
		# 	},
		# }

		self.confFile = CreatePath (self.nginxConf['server']['root'], 'server.conf')

		self.serverStart = 'cd {} && cherryd -c {} -d -i {}'.format (self.nginxConf['server']['root'], self.confFile, 'index')

		self.serverStop = "sudo pkill -f cherryd"

	def configCreate (self):
		for confKey, confValue in self.kwargs['techConf'].items ():
			if isinstance (confValue, dict):
				self.config += "[{}]\n".format (confKey)
				self.configCreateSection (confValue)
			elif isinstance (confValue, int):
				self.config += "{} : {}\n".format (confKey, confValue)
			else:
				self.config += "{} : '{}'\n".format (confKey, confValue)
		fw = open (self.kwargs['confFile'], "wt")
		fw.write (self.config)
		fw.close ()

	def configCreateSection (self, section):
		for confKey, confValue in section.items ():
			if isinstance (confValue, int):
				self.config += "{} : {}\n".format (confKey, confValue)
			else:
				self.config += "{} : '{}'\n".format (confKey, confValue)

	def load (self):
		try:
			demoIndexPage = '''import cherrypy
from cherrypy.process.plugins import Daemonizer

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		return "Hello World!"

d = Daemonizer(cherrypy.engine)
d.subscribe()

cherrypy.quickstart(HelloWorld())'''
			destinationDir = CreatePath (self.nginxConf['server']['root'])
			destinationFile = CreatePath (destinationDir, 'index.py')
			os.chdir (destinationDir)
			fw = open (destinationFile, "wt")
			fw.write (demoIndexPage)
			fw.close ()
			print ('Демонстрационный файл успешно создан!')
			os.system ('pip install cherrypy')
			print ('Новая версия CherryPy успешно загружена!')
			return True
		except:
			print ('Ошибка загрузки CherryPy!')
			return False
