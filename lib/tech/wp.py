import os
import shutil
import sys
import tarfile
import urllib.request

from lib.helper import *
from lib.tech.php import Php


class Wp (Php):
	techDescription = 'WordPress Description'

	def __init__ (self, **kwargs):
		super (Wp, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'                                                                                                                                         :
				{
					'try_files': '$uri $uri/ /index.php?$args'
				},
			'~ [^/]\.php(/|$)'                                                                                                                          :
				{
					'fastcgi_index'       : 'index.php',
					'include'             : 'fcgi.conf',
					'fastcgi_pass'        : 'unix:' + self.socket,
					'fastcgi_param'       : 'SCRIPT_FILENAME $document_root$fastcgi_script_name',
					'fastcgi_read_timeout': '300',
				},
			'/favicon.ico'                                                                                                                              :
				{
					'log_not_found': 'off',
					'access_log'   : 'off',
				},

			'/robots.txt'                                                                                                                               :
				{
					'allow'        : 'all',
					'log_not_found': 'off',
					'access_log'   : 'off',
				},
			'~* ^.+\.(ogg|ogv|svg|svgz|eot|otf|woff|mp4|ttf|rss|atom|jpg|jpeg|gif|png|ico|zip|tgz|gz|rar|bz2|doc|xls|exe|ppt|tar|mid|midi|wav|bmp|rtf)$':
				{
					'access_log'   : 'off',
					'log_not_found': 'off',
					'expires'      : 'max',
				}
		}

		self.nginxConf['server']['rewrite'] = '/wp-admin$ $scheme://$host$uri/ permanent'

	def load (self):
		try:
			destinationDir = CreatePath (self.nginxConf['server']['root'])
			sourceDir = CreatePath (destinationDir, 'wordpress')
			arcSourceName = 'latest.tar.gz'
			arcSourcePath = CreatePath (destinationDir, arcSourceName)
			urllib.request.urlretrieve ('http://wordpress.org/' + arcSourceName, arcSourcePath)
			tar = tarfile.open (arcSourcePath)
			tar.extractall (destinationDir)
			tar.close ()
			sourceList = os.listdir (sourceDir)
			for files in sourceList:
				shutil.move (CreatePath (sourceDir, files), destinationDir)
			os.rmdir (sourceDir)
			os.remove (arcSourcePath)
			print ('Новая версия WordPress успешно загружена!')
			return True
		except:
			print ('Ошибка загрузки WordPress!')
			return False
