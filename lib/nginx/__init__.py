import nginx  # pip install python-nginx
from config import Config
from lib.helper import *
from lib.nginx.config import Config as NginxConfig


class NginxConf (object):
	nginxConfDict = {}

	def configCreateAndDump (self, confDict, confOutputFile):
		nginxConf = nginx.Conf ()
		self.nginxConfDict.update ({'conf': nginxConf})
		for confKey, confValue in confDict.items ():
			self.configCreate (confKey, confValue, 'conf')
		nginx.dumpf (self.nginxConfDict['conf'], confOutputFile)

	def configCreate (self, confKey, confValue, parentKey=''):
		if isinstance (confValue, dict):
			nginxLoadClass = LoadClass ('nginx', confKey)

			if confKey == 'location':
				for key, value in confValue.items ():
					self.nginxConfDict.update ({key: nginxLoadClass (key)})
					for inKey, inValue in value.items ():
						self.configCreate (inKey, inValue, key)
					self.nginxConfDict[parentKey].add (self.nginxConfDict[key])
			elif confKey == 'types':
				if nginxLoadClass:
					self.nginxConfDict.update ({confKey: nginxLoadClass ('')})
				for key, value in confValue.items ():
					self.configCreate (key, value, confKey)
				self.nginxConfDict[parentKey].add (self.nginxConfDict[confKey])
			elif confKey == 'fastcgi_param':
				for key, value in confValue.items ():
					self.configCreate ('fastcgi_param', '{} {}'.format (key, value), parentKey)
			else:
				if nginxLoadClass:
					self.nginxConfDict.update ({confKey: nginxLoadClass ()})
				else:
					self.nginxConfDict.update ({confKey: nginx.Container (confKey)})
				for key, value in confValue.items ():
					self.configCreate (key, value, confKey)
				self.nginxConfDict[parentKey].add (self.nginxConfDict[confKey])
		elif isinstance (confValue, list):
			for value in confValue:
				self.configCreate (confKey, value, parentKey)
		elif isinstance (confValue, str):
			self.nginxConfDict[parentKey].add (nginx.Key (confKey, confValue))


class NginxCustomConf (NginxConf):
	def __init__ (self, jsonData):
		confOutputFile = CreatePath (NginxConfig.nginxDir, NginxConfig.nginxConfDir, jsonData['serverName'] + '.conf')
		self.configCreateAndDump (jsonData['nginxConf'], confOutputFile)
		# confOutputFile = CreatePath ('/home/vagrant/Scripts/Laser/', jsonData['serverName'] + '.conf')
		# self.configCreateAndDump (confDict, confOutputFile)
		print(confOutputFile)


class NginxMainConf (NginxConf):
	def __init__ (self):
		confOutputFile = CreatePath (NginxConfig.nginxDir, NginxConfig.nginxConfFileName)
		# confOutputFile = CreatePath ('/home/vagrant/Scripts/Laser/', NginxConfig.nginxConfFileName)
		self.configCreateAndDump (NginxConfig.nginxConf, confOutputFile)


class NginxTypesConf (NginxConf):
	def __init__ (self):
		confOutputFile = CreatePath (NginxConfig.nginxDir, NginxConfig.nginxTypesFileName)
		# confOutputFile = CreatePath ('/home/vagrant/Scripts/Laser/', NginxConfig.nginxTypesFileName)
		self.configCreateAndDump (NginxConfig.nginxTypes, confOutputFile)


class NginxProxyConf (NginxConf):
	def __init__ (self):
		confOutputFile = CreatePath (NginxConfig.nginxDir, NginxConfig.nginxProxyFileName)
		# confOutputFile = CreatePath ('/home/vagrant/Scripts/Laser/', NginxConfig.nginxProxyFileName)
		self.configCreateAndDump (NginxConfig.nginxProxy, confOutputFile)


class NginxFcgiConf (NginxConf):
	def __init__ (self):
		confOutputFile = CreatePath (NginxConfig.nginxDir, NginxConfig.nginxFcgiFileName)
		# confOutputFile = CreatePath ('/home/vagrant/Scripts/Laser/', NginxConfig.nginxFcgiFileName)
		self.configCreateAndDump (NginxConfig.nginxFcgi, confOutputFile)
