import json
import os
import pwd
import shutil

import lib.nginx
from config import *
from lib.helper import *
from lib.tech.php import *


class Host:
	def __init__ (self):
		pass

	def createHostDirs (self, host):
		try:
			pathDict = {}
			for key, value in Config.serverDirs.items ():
				pathDict[key] = CreatePath (Config.serverRoot, host, value)
				if not os.path.exists (pathDict[key]):
					os.makedirs (pathDict[key])
				else:
					print ('Папка "{}" уже существует'.format (host))
					return False
			return pathDict
		except:
			print ('Ошибка создания папки проекта')
			return False

	def getConfig (self, host=False):
		try:
			configDict = {}
			for dir in os.listdir (Config.serverRoot):
				configFile = CreatePath (Config.serverRoot, dir, Config.serverDirs['config'], Config.configFile)
				if os.path.exists (configFile):
					with open (configFile) as jsonFile:
						configDict[dir] = json.load (jsonFile)
			if host and configDict[host]:
				return configDict[host]
			elif host and not configDict[host]:
				print ('Ошибка! Указанного хоста не существует!')
				return False
			else:
				return configDict
		except:
			print ('Ошибка получения конфигов хостов')
			return False

	def new (self, **kwargs):
		if kwargs['tech'] != 'none':
			techClass = LoadClass ('lib', 'tech', kwargs['tech'], kwargs['tech'], serverName=kwargs['serverName'], serverAlias=kwargs['serverAlias'])
			if techClass:
				techClass.hello ()
				pathDict = self.createHostDirs (kwargs['serverName'])
				if pathDict != False and os.path.exists (pathDict['config']):
					json = Json (ClassAttr (techClass), CreatePath (pathDict['config'], Config.configFile))
					json.update ()
					print ('Хост "{}" был успешно создан с использованием шаблона "{}"'.format (kwargs['serverName'], kwargs['tech']))
					if kwargs['load'].lower () == 'yes':
						techClass.load ()
					if kwargs['adminer'].lower () == 'yes':
						techAdminerClass = LoadClass ('lib', 'tech', 'adminer', 'adminer', serverName=kwargs['serverName'], destinationFile='adminer.php')
						if techAdminerClass:
							techAdminerClass.load ()
			else:
				print ('Tехнологического шаблона "{}" не существует! Укажите правильный шаблон. (к примеру: --tech=php)'.format (kwargs['tech']))
		else:
			print ('Укажите технологический шаблон хоста (к примеру: --tech=php)')
		if kwargs['db'] != 'none':
			dbClass = LoadClass ('lib', 'db', kwargs['db'], kwargs['db'], serverName=kwargs['serverName'], dbname=kwargs['dbname'])
			if dbClass:
				dbClass.createDb ()
				json = Json (ClassAttr (dbClass), CreatePath (Config.serverRoot, kwargs['serverName'], Config.serverDirs['config'], Config.configFile))
				json.update ()
			else:
				print ('Шаблонa баз данных "{}" не существует! Укажите правильный шаблон. (к примеру: --db=mysql)'.format (kwargs['tech']))

	def delete (self, name):
		try:
			hostDir = CreatePath (Config.serverRoot, name)
			jsonData = self.getConfig (name)
			if jsonData:
				if 'dbTechName' in jsonData:
					loadDbClass = LoadClass ('lib', 'db', jsonData['dbTechName'], jsonData['dbTechName'], dbname=jsonData['dbName'])
					if loadDbClass:
						loadDbClass.dropDb ()
				shutil.rmtree (hostDir)
				print ('Проект "{}" успешно удален'.format (name))
				return True
			else:
				print ('Проекта "{}" не существует'.format (name))
				return False
		except:
			print ('Ошибка удаления проекта')
			return False

	def list (self):
		try:
			jsonData = self.getConfig ()
			for key, value in jsonData.items ():
				print ('{} - {} - {}'.format (value['serverName'], value['techName'], value['techDescription']))
		except:
			print ('Ошибка вывода списка проектов')
			return False

	def up (self):
		# os.chmod(r'/etc/nginx/conf.d/', 0o777)
		# TODO: заменить более правильным решением
		# os.system ('sudo groupadd nobody')
		os.system ('sudo chmod -R 0777 /etc/nginx/')
		os.system ('sudo chmod -R 0777 /etc/nginx/conf.d/')

		if not os.path.exists (Config.socketRoot):
			os.makedirs (Config.socketRoot)

		os.system ('sudo chmod -R 0777 {}'.format (Config.socketRoot))

		# print (os.access(r'/etc/nginx/conf.d/', os.W_OK))
		nginxConfDir = CreatePath (lib.nginx.config.Config.nginxDir, lib.nginx.config.Config.nginxConfDir)

		for file in os.listdir (nginxConfDir):
			os.remove (CreatePath (nginxConfDir, file))

		Php.configRemove (self)

		jsonData = self.getConfig ()

		lib.nginx.NginxMainConf ()
		lib.nginx.NginxTypesConf ()
		lib.nginx.NginxProxyConf ()
		lib.nginx.NginxFcgiConf ()

		for key, value in jsonData.items ():
			try:
				tech = value['techName']
				loadClass = LoadClass ('lib', 'tech', tech, tech, **value)
				loadClass.stop ()
			except:
				print ('Ошибка остановки сервера {} ({})'.format (value['serverName'], value['techName']))
		for key, value in jsonData.items ():
			try:
				lib.nginx.NginxCustomConf (value)
				tech = value['techName']
				loadClass = LoadClass ('lib', 'tech', tech, tech, **value)
				loadClass.configCreate ()
				loadClass.start ()
			except:
				print ('Ошибка сохранения файла конфигурации {} ({})'.format (value['serverName'], value['techName']))

		# TODO: заменить более правильным решением (Нужно для решения проблемы [emerg]: bind() to 0.0.0.0:80 failed (98: Address already in use))
		os.system ("sudo fuser -k 80/tcp")
		os.system ("sudo fuser -k 8080/tcp")
		# TODO: заменить более правильным решением
		os.system ('sudo service nginx restart')

	def start (self):
		jsonData = self.getConfig ()
		for key, value in jsonData.items ():
			tech = value['techName']
			loadClass = LoadClass ('lib', 'tech', tech, tech, **value)
			loadClass.start ()

		os.system ('sudo fuser -k 80/tcp')
		os.system ('sudo service nginx start')

	def restart (self):
		jsonData = self.getConfig ()
		for key, value in jsonData.items ():
			tech = value['techName']
			loadClass = LoadClass ('lib', 'tech', tech, tech, **value)
			loadClass.stop ()
		for key, value in jsonData.items ():
			tech = value['techName']
			loadClass = LoadClass ('lib', 'tech', tech, tech, **value)
			loadClass.start ()

		os.system ('sudo fuser -k 80/tcp')
		os.system ('sudo service nginx restart')

	def stop (self):
		jsonData = self.getConfig ()
		for key, value in jsonData.items ():
			tech = value['techName']
			loadClass = LoadClass ('lib', 'tech', tech, tech, **value)
			loadClass.stop ()

		os.system ('sudo service nginx stop')
