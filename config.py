import sys
import time


class Config:
	progAuthor = 'LaCodda'

	progName = 'Laser'

	progVersion = '0.0.8'

	dateForFile = time.strftime ('%Y-%m-%d_%H-%M-%S')

	dateTime = time.strftime ('%Y.%m.%d %H:%M:%S')

	serverRoot = '/srv/'

	socketRoot = '/home/vagrant/socket/'

	serverDirs = {
		'backup'       : 'backups',
		'config'       : 'config',
		'document_root': 'public_html',
		'log'          : 'logs',
	}

	configFile = 'config.json'

	backupsDir = serverRoot + '/backups/'

	# groupBySite = True
	#
	# save_db_only_if_site_exist = False
	#
	# delete_files_after_uploading = False

	phpVersion = '5.4.45'

	# phpVersion = '5.6.24'

	phpBrew = {
		'confDir' : '/home/vagrant/.phpbrew/php/php-{}/etc/php-fpm.d'.format (phpVersion),
		'fpm'     : 'sudo /home/vagrant/.phpbrew/php/php-{}/sbin/php-fpm -R'.format (phpVersion),
		'confName': 'php-fpm.conf',
	}

	mongodbConfig = {
		'host'       : 'localhost',
		'port'       : 27017,
		'database'   : 'lalibase',
		'backup_name': backupsDir + 'lalibase_' + dateForFile + '.gz',
		'commands'   : {
			'restore': 'mongorestore --db {} --archive={} --gzip',
			'dump'   : 'mongodump --db {} --archive={} --gzip',
		}
	}
