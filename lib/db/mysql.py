import configparser
import glob
import os
import pymysql.cursors
import time

from config import *
from lib.db import Db
from lib.helper import *


class Mysql (Db):
	dbDescription = 'MySQL Description'

	config = {
		'host'    : 'localhost',
		'user'    : 'root',
		'password': '1111',
		'dumpName': '',
		'commands': {
			'show_databases' : 'SHOW DATABASES',
			'check_database' : "SHOW DATABASES LIKE '{}'",
			'create_database': 'CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci',
			'drop_database'  : 'DROP DATABASE IF EXISTS {}',
			'dump'           : 'mysqldump -u {} -p{} {} > {}',
			'restore'        : 'mysql -u {} -p{} {} < {}',
		}
	}

	db = None

	cursor = None

	def __init__ (self, **kwargs):
		super (Mysql, self).__init__ (**kwargs)

		self.config['dumpName'] = self.dbName + '_' + time.strftime ('%Y-%m-%d_%H-%M-%S') + '.sql'

		self.connectDb ()

	def __del__ (self):
		self.db.close ()

	def connectDb (self):
		connect = {
			'host'       : self.config['host'],
			'user'       : self.config['user'],
			'password'   : self.config['password'],
			# 'charset':'utf8mb4',
			'cursorclass': pymysql.cursors.DictCursor
		}

		self.db = pymysql.connect (**connect)

		self.cursor = self.db.cursor ()

		if self.checkDb ():
			connect['db'] = self.dbName
			self.db = pymysql.connect (**connect)
			self.cursor = self.db.cursor ()

	def checkDb (self):
		try:
			sql = self.config['commands']['check_database'].format (self.dbName)
			if self.cursor.execute (sql):
				# print ('БД существует')
				return True
			else:
				# print ('БД НЕ существует')
				return False
		except:
			print ('Ошибка проверки базы данных')
			return False

	def createDb (self):
		try:
			sql = self.config['commands']['create_database'].format (self.dbName)
			self.cursor.execute (sql)
			print ('База данных "{}" успешно создана'.format (self.dbName))
			return True
		except:
			print ('Ошибка создания базы данных')
			return False

	def dropDb (self):
		try:
			sql = self.config['commands']['drop_database'].format (self.dbName)
			self.cursor.execute (sql)
			print ('База данных "{}" успешно удалена'.format (self.dbName))
			return True
		except:
			print ('Ошибка удаления базы данных')
			return False
		# finally:
		# 	self.db.close ()

	def dumpDb (self, dumpPath):
		try:
			dumpFile = CreatePath (dumpPath, self.config['dumpName'])
			dump = self.config['commands']['dump'].format (self.config['user'], self.config['password'], self.dbName, dumpFile)
			result = os.system (dump)
			if result == 0:
				print ('Дамп базы данных "{}" успешно создан'.format (self.dbName))
				return self.config['dumpName']
			else:
				print ('Дамп базы данных "{}" НЕ создан'.format (self.dbName))
				print (result)
				return False
		except:
			print ('Ошибка создания дампа базы данных')
			return False

	def restoreDb (self, dumpPath, dumpFile=False):
		try:
			if dumpFile == False:
				dumpFile = max (glob.iglob (CreatePath (dumpPath, '*.sql')), key=os.path.getctime)
			restore = self.config['commands']['restore'].format (self.config['user'], self.config['password'], self.dbName, dumpFile)
			self.createDb ()
			result = os.system (restore)
			if result == 0:
				print ('База данных "{}" успешно восстановлена из дампа {}'.format (self.dbName, dumpFile))
				return True
			else:
				print ('База данных "{}" НЕ восстановлена из дампа {}'.format (self.dbName, dumpFile))
				print (result)
				return False
		except:
			print ('Ошибка восстановления базы данных из дампа')
			return False
