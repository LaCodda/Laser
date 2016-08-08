import os

from config import *
from lib.helper import *


class Tech ():
	techName = ''

	techDescription = 'Description'

	maintenanceMode = False

	enabled = True

	ports = [
		{
			'spdy'   : False,
			'default': False,
			'ssl'    : False,
			'host'   : '*',
			'http2'  : False,
			'port'   : 80
		}
	]

	sslKeyPath = ''

	sslCertPath = ''

	owner = 'root'

	serverName = ''

	techConf = {}

	nginxConf = {
		'server': {}
	}

	socket = ''

	def __init__ (self, **kwargs):

		self.kwargs = kwargs

		if 'serverName' in kwargs:
			self.setTechName ()

			self.setServerName (kwargs['serverName'])

			self.setSocket (kwargs['serverName'])

			self.nginxConf['server']['server_name'] = kwargs['serverName']

			self.nginxConf['server']['access_log'] = CreatePath (Config.serverRoot, kwargs['serverName'], Config.serverDirs['log'], 'access.log')

			self.nginxConf['server']['error_log'] = CreatePath (Config.serverRoot, kwargs['serverName'], Config.serverDirs['log'], 'error.log')

			self.nginxConf['server']['root'] = CreatePath (Config.serverRoot, kwargs['serverName'], Config.serverDirs['document_root'])

			self.nginxConf['server']['client_max_body_size'] = '32m'

		if 'serverAlias' in kwargs:
			serverAlias = [alias.strip () for alias in kwargs['serverAlias'].split (',')]

			serverAlias.insert (0, kwargs['serverName'])

			self.nginxConf['server']['server_name'] = ' '.join (serverAlias)

		if 'listen' in kwargs:
			self.nginxConf['server']['listen'] = kwargs['listen']
		else:
			self.nginxConf['server']['listen'] = '*:80'

	def setTechName (self):
		self.techName = self.__class__.__name__

	def setServerName (self, serverName):
		self.serverName = serverName

	def setSocket (self, serverName):
		self.socket = CreatePath (Config.socketRoot, serverName.replace ('.', '-') + '-laser-0.sock')

	def hello (self):
		print ('Hello ' + self.techName)

	def configCreate (self):
		pass

	def load (self):
		pass

	def install (self):
		pass

	def start (self):
		pass

	def stop (self):
		pass
