import glob
import os
import re
import tarfile
import time
from ftplib import FTP
from zipfile import *

from config import *
from lib.helper import *
from lib.host import *


class Backup:
	hostName = ''

	hostDir = ''

	backupDir = ''

	backupFile = ''

	type = ''

	backupFileArc = None

	def __init__ (self, hostName, type):
		self.hostName = hostName
		self.type = type
		self.hostDir = CreatePath (Config.serverRoot, hostName)
		self.documentRootDir = CreatePath (self.hostDir, Config.serverDirs['document_root'])
		self.backupDir = CreatePath (self.hostDir, Config.serverDirs['backup'])
		self.backupFile = CreatePath (self.backupDir, hostName + '_' + time.strftime ('%Y-%m-%d_%H-%M-%S') + '.zip')

	# f.write(content)
	# f.close()

	# if hostName == 'all':
	#
	# hostDir = CreatePath (Config.serverRoot, name)

	def host (self):
		self.backupFileArc = ZipFile (self.backupFile, 'w')
		if self.type == 'all':
			self.files ()
			self.db ()
		elif self.type == 'files':
			self.files ()
		elif self.type == 'db':
			self.db ()
		self.backupFileArc.close ()

	def db (self):
		try:
			host = Host ()
			jsonData = host.getConfig (self.hostName)
			if jsonData:
				if 'dbTechName' in jsonData:
					loadDbClass = LoadClass ('lib', 'db', jsonData['dbTechName'], jsonData['dbTechName'], dbname=jsonData['dbName'])
					if loadDbClass:
						dumpName = loadDbClass.dumpDb (self.backupDir)
						if dumpName:
							os.chdir (self.backupDir)
							self.backupFileArc.write (dumpName)
							os.remove (dumpName)
							print ('В архив {} добавлен дамп базы данных {}'.format (self.backupFile, dumpName))
							return True
		except:
			print ('Ошибка')

	def files (self):
		try:
			host = Host ()
			jsonData = host.getConfig (self.hostName)
			if jsonData:
				os.chdir (self.hostDir)
				for root, dirs, files in os.walk (Config.serverDirs['document_root']):  # Список всех файлов и папок в директории folder
					for file in files:
						self.backupFileArc.write (os.path.join (root, file))
				print ('В архив {} добавлены файлы проекта'.format (self.backupFile))
				return True
		except:
			print ('Ошибка')


class Restore:
	hostName = ''

	hostDir = ''

	backupDir = ''

	backupFile = ''

	type = ''

	backupFileArc = None

	def __init__ (self, **kwargs):
		self.hostName = kwargs['hostName']
		self.type = kwargs['type']
		self.hostDir = CreatePath (Config.serverRoot, kwargs['hostName'])
		self.backupDir = CreatePath (self.hostDir, Config.serverDirs['backup'])
		if 'backupFile' in kwargs:
			self.backupFile = kwargs['backupFile']
		else:
			self.backupFile = max (glob.iglob (CreatePath (self.backupDir, '*.zip')), key=os.path.getctime)

	def host (self):
		tempDbDump = ''
		self.backupFileArc = ZipFile (self.backupFile, 'r')
		searchDb = [x for i, x in enumerate (self.backupFileArc.namelist ()) if re.search (r'^(?!.+/).*\.sql$', x)]
		if len (searchDb) > 0:
			tempDbDump = CreatePath (self.backupDir, searchDb[0])
			self.backupFileArc.extract (searchDb[0], self.backupDir)
		else:
			print ('В выбранном архиве отсутствует дамп базы данных')
		if self.type == 'all':
			# self.files ()
			self.db ()
		elif self.type == 'files':
			self.files ()
		elif self.type == 'db':
			self.db ()
		self.backupFileArc.close ()
		if os.path.exists (tempDbDump):
			os.remove (tempDbDump)

	def db (self):
		try:
			host = Host ()
			jsonData = host.getConfig (self.hostName)
			if jsonData:
				if 'dbTechName' in jsonData:
					loadDbClass = LoadClass ('lib', 'db', jsonData['dbTechName'], jsonData['dbTechName'], dbname=jsonData['dbName'])
					if loadDbClass:
						loadDbClass.restoreDb (self.backupDir)
		except:
			print ('Ошибка')

	def files (self):
		try:
			host = Host ()
			jsonData = host.getConfig (self.hostName)
			if jsonData:
				os.chdir (self.hostDir)
				for root, dirs, files in os.walk (Config.serverDirs['document_root']):  # Список всех файлов и папок в директории folder
					for file in files:
						self.backupFileArc.write (os.path.join (root, file))
				print ('В архив {} добавлены файлы проекта'.format (self.backupFile))
				return True
		except:
			print ('Ошибка')


class Compile:
	installDir = 'bitrix/modules/lacodda.biztrip/install'

	installDirs = {
		'admin'     : {
			'source'     : 'bitrix/modules/lacodda.biztrip/admin',
			'destination': 'admin',
		},
		'biztrip'   : {
			'source'     : 'biztrip',
			'destination': 'biztrip',
		},
		'components': {
			'source'     : 'bitrix/components/lacodda',
			'destination': 'components/lacodda',
		},
		'upload'    : {
			'source'     : 'upload/biztrip',
			'destination': 'upload/biztrip',
		},
	}

	mySqlConfig = {
		'host'    : 'localhost',
		'user'    : 'root',
		'password': '1111',
		'dumpName': '',
		'commands': {
			'show_databases' : 'SHOW DATABASES',
			'create_database': 'CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci',
			'drop_database'  : 'DROP DATABASE IF EXISTS {}',
			'dump'           : 'mysqldump -u {} -p{} {} > {}',
			'restore'        : 'mysql -u {} -p{} {} < {}',
		}
	}

	def __init__ (self):
		for child in self.installDirs.keys ():
			if os.path.exists (self.installDir + os.sep + child):
				shutil.rmtree (self.installDir + os.sep + child)
			if os.path.exists (self.installDirs[child]['source']):
				shutil.copytree (self.installDirs[child]['source'], self.installDir + os.sep + self.installDirs[child]['destination'])

		print ('Копирование завершено!')


# try:
#     from config import main_config
# except ImportError:
#     print('File "config.py" not found.')
#     exit()
# DATE = time.strftime('%Y-%m-%d_%H-%M-%S')
# UPLOADS_FILES = []
# SITES = []
# DBS = {}
# FILES = {}


def get_database_list (config):
	""" Getting a list of databases to create a dump """
	if config['backups_targets']['databases'] == '__ALL__':
		databases = []
		database_list_command = config['mysql']['commands']['show_databases'].format (
				config['mysql']['user'],
				config['mysql']['password'],
				config['mysql']['host']
		)
		for database in os.popen (database_list_command).readlines ():
			database = database.strip ()
			if database not in config['backups_targets']['databases_excluded']:
				databases.append (database)
		return databases
	else:
		return config['backups_targets']['databases']


def database_backup (config):
	""" Creating a database dump """
	databases = get_database_list (config)

	sql_backup_dir = os.path.abspath (config['backups_dir'] + DATE + os.sep + 'mysql')

	if not os.path.exists (sql_backup_dir):
		print('Create folder ' + sql_backup_dir)
		os.makedirs (sql_backup_dir)

	for database in databases:
		print('MySQL Dump: ' + database)
		sql_backup_name = database + '_' + DATE + '.sql'
		sql_backup_path = sql_backup_dir + os.sep + sql_backup_name

		code = os.system (
				config['mysql']['commands']['dump'].format (
						config['mysql']['user'],
						config['mysql']['password'],
						database,
						sql_backup_path
				)
		)
		if code != 0:
			os.unlink (sql_backup_path)
		else:
			gz_sql_backup_path = sql_backup_path + '.gz'
			sql_file = open (sql_backup_path, 'rb')
			gz_sql_file = gzip.open (gz_sql_backup_path, 'wb')
			gz_sql_file.writelines (sql_file)
			sql_file.close ()
			gz_sql_file.close ()
			os.unlink (sql_backup_path)
			UPLOADS_FILES.append (gz_sql_backup_path)
			DBS[database] = gz_sql_backup_path


def get_dirs_list (config):
	dirs_list = {}
	for (path, type) in config['backups_targets']['dirs'].items ():
		if type == 'composite':
			list = os.listdir (path)
			for dir in list:
				path_dir = os.path.abspath (path + os.sep + dir)
				if path_dir not in config['backups_targets']['dirs_excluded']:
					dirs_list[dir] = path_dir
					SITES.append (dir)
				# print('Backup directory: ' + path_dir)
		else:
			dir = os.path.basename (path)
			path_dir = os.path.abspath (path)
			if os.path.exists (path_dir) == True:
				dirs_list[dir] = path_dir
				SITES.append (os.path.basename (path_dir))
			# print('Backup directory: ' + path_dir)
			# else:
			#     print('Directory "' + path_dir + '" not exist')
	return dirs_list


def backup_files (config):
	""" Create an archive folder """
	files_backup_dir = os.path.abspath (config['backups_dir'] + DATE + os.sep + 'public_html')

	if not os.path.exists (files_backup_dir):
		print('Create folder ' + files_backup_dir)
		os.makedirs (files_backup_dir)
	dirs_list = get_dirs_list (config)
	for (site, path) in dirs_list.items ():
		print('Backup directory: ' + path)
		backup_name = files_backup_dir + os.sep + os.path.basename (os.path.abspath (path)) + \
		              '_' + DATE + '.tar.bz2'

		with tarfile.open (backup_name, "w:gz") as tar:
			tar.add (
					name=path,
					arcname=os.path.abspath (path),
					exclude=lambda file: file in config['backups_targets']['dirs_excluded']
			)
		UPLOADS_FILES.append (backup_name)
		FILES[site] = backup_name


def upload_backups (upload_files, config):
	""" Uploading files on the FTP server """
	print('Connect to FTP')
	try:
		ftp = FTP ()
		ftp.connect (config['ftp']['host'], 21)
		ftp.login (config['ftp']['user'], config['ftp']['password'])
		ftp.cwd (config['ftp']['dir_destination'])

	except Exception as e:
		print(type (e))
		print(e.args)
		print(e)
		if config['delete_files_after_uploading']:
			delete_files_after_uploading (upload_files)

	else:
		for file in upload_files:
			print('Upload file: ' + file)

			try:
				ftp.storbinary ('STOR ' + os.path.basename (os.path.abspath (file)), open (file, 'rb'))

			except Exception as e:
				if config['delete_files_after_uploading']:
					delete_files_after_uploading ([file])

				print(type (e))
				print(e.args)
				print(e)
				break

			else:
				ftp.storbinary ('STOR ' + os.path.basename (os.path.abspath (file)), open (file, 'rb'))
				if config['delete_files_after_uploading']:
					delete_files_after_uploading ([file])
	ftp.quit ()


def delete_files_after_uploading (files):
	""" Delete files """
	for file in files:
		print('Delete file: ' + file)
		os.unlink (file)


def main (config):
	config['backups_dir'] = os.path.abspath (config['backups_dir']) + os.sep

	if not os.path.exists (config['backups_dir']):
		print('Create folder ' + config['backups_dir'])
		os.mkdir (config['backups_dir'])

	database_backup (config)
	backup_files (config)

	if config['group_by_site'] == True:
		for site in SITES:
			site_path = config['backups_dir'] + DATE + os.sep + site
			if not os.path.exists (site_path):
				print('Create folder ' + site_path)
				os.mkdir (site_path)
			os.rename (FILES[site], os.path.abspath (site_path + os.sep + os.path.basename (FILES[site])))

			if site in DBS.keys ():
				os.rename (DBS[site], os.path.abspath (site_path + os.sep + os.path.basename (DBS[site])))

		mysql_dir = os.path.abspath (config['backups_dir'] + DATE + os.sep + 'mysql')
		public_html_dir = os.path.abspath (config['backups_dir'] + DATE + os.sep + 'public_html')

		if not os.listdir (public_html_dir):
			os.rmdir (public_html_dir)

		if config['save_db_only_if_site_exist'] == True:
			for path in DBS.values ():
				if os.path.exists (path):
					os.unlink (path)
					print('Delete DB dump ' + path)

		if not os.listdir (mysql_dir):
			os.rmdir (mysql_dir)
