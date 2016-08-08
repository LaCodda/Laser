import os
import shutil
import sys
import tarfile
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import *
from lib.helper import *
from lib.db.mysql import Mysql
from lib.tech.bitrix import Bitrix
from lib.host import Host


class Bitrix ():
	mysqlCommands = {
		'select': "SELECT VALUE FROM b_option WHERE `NAME`='admin_passwordh'",
		'update': "UPDATE b_option SET `VALUE` = '{}' WHERE `NAME`='admin_passwordh'",
	}
	dbPass = ''
	cacheFile = '/bitrix/modules/main/admin/define.php'
	managedCache = '/bitrix/managed_cache/'
	sourceHost = ''
	sourceCacheFile = ''
	destinationHost = ''
	destinationCacheFile = ''

	def __init__ (self, **kwargs):
		self.destinationHost = kwargs['destinationHost']
		self.destinationCacheFile = CreatePath (Config.serverRoot, self.destinationHost, Config.serverDirs['document_root'], self.cacheFile)
		if 'sourceHost' in kwargs:
			self.sourceHost = kwargs['sourceHost']
			self.sourceCacheFile = CreatePath (Config.serverRoot, self.sourceHost, Config.serverDirs['document_root'], self.cacheFile)
		else:
			self.sourceHost = 'bitrix_demo_'
			self.sourceCacheFile = CreatePath (Config.serverRoot, self.sourceHost, Config.serverDirs['document_root'], self.cacheFile)
			# host = Host ()
			# host.new (serverName=self.sourceHost, tech='bitrix', db='mysql')
			# host.up ()

	def install (self):
		bitrixSetupUrl = '{}/bitrixsetup.php'.format (self.sourceHost)
		print (bitrixSetupUrl)
		# try:
		# 	webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'ru-RU'
		# 	browser = webdriver.PhantomJS ()
		# 	browser.get (bitrixSetupUrl)
		# 	# assert "Python" in driver.title
		# 	# elem = browser.find_element_by_name ("q")
		# 	# elem.send_keys ("pycon")
		# 	# elem.send_keys (Keys.RETURN)
		# 	# assert "No results found." not in browser.page_source
		# 	print (browser.page_source)
		# 	browser.close ()
		# 	# os.system("kill -9 `ps aux | grep phantomjs | awk '{print $2}'`")
		# 	files = 'bitrixsetup.php'
		# 	files = 'bitrixsetup.php?action=LOAD&edition=1&url=intranet_business&lang=ru'
		# 	print ('Новая версия файла bitrixsetup.php успешно загружена!')
		# 	return True
		# except:
		# 	print ('Ошибка загрузки WordPress!')
		# 	return False

	def snichPass (self):
		connectSource = Mysql (serverName=self.sourceHost)
		connectDestination = Mysql (serverName=self.destinationHost)
		if not connectSource.checkDb ():
			print ('Ошибка! БД {} отсутствует'.format (connectSource.dbName))
			return False
		if not connectDestination.checkDb ():
			print ('Ошибка! БД {} отсутствует'.format (connectDestination.dbName))
			return False
		if not os.path.exists (self.sourceCacheFile):
			print ('Ошибка! Файл {} отсутствует'.format (self.sourceCacheFile))
			return False
		if not os.path.exists (self.destinationCacheFile):
			print ('Ошибка! Файл {} отсутствует'.format (self.destinationCacheFile))
			return False
		self.copyPass ()
		self.pastePass ()
		self.copyCache ()
		self.clearCacheDir ()

	def copyPass (self):
		try:
			connect = Mysql (serverName=self.sourceHost)
			connect.cursor.execute (self.mysqlCommands['select'])
			result = connect.cursor.fetchone ()
			self.dbPass = result['VALUE']
			print(self.dbPass)

		except:
			print ('Ошибка соединения с базой данных')
			return False

	def pastePass (self):
		try:
			connect = Mysql (serverName=self.destinationHost)
			connect.cursor.execute (self.mysqlCommands['update'].format (self.dbPass))
			connect.db.commit ()

		except:
			print ('Ошибка соединения с базой данных')
			return False

	def copyCache (self):
		try:
			shutil.copyfile (self.sourceCacheFile, self.destinationCacheFile)
			print ('Файл кэша успешно скопирован')
			return True
		except:
			print ('Ошибка копирования')
			return False

	def clearCacheDir (self):
		cacheDir = CreatePath (Config.serverRoot, self.destinationHost, Config.serverDirs['document_root'], self.managedCache)
		for file in os.listdir (cacheDir):
			shutil.rmtree (CreatePath (cacheDir, file))

# if dbClass:
# 	dbClass.createDb ()
# 	json = Json (ClassAttr (dbClass), CreatePath (Config.serverRoot, kwargs['serverName'], Config.serverDirs['config'], Config.configFile))
# 	json.update ()
# else:
# 	print ('Шаблонa баз данных "{}" не существует! Укажите правильный шаблон. (к примеру: --db=mysql)'.format (kwargs['tech']))
