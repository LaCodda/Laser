import os
import shutil
import sys
import tarfile
import urllib.request

from lib.helper import *
from lib.tech.php import Php


class Adminer (Php):
	techDescription = 'Adminer (formerly phpMinAdmin) is a full-featured database management tool written in PHP'

	def __init__ (self, **kwargs):
		super (Adminer, self).__init__ (**kwargs)

	def load (self):
		try:
			if 'destinationFile' in self.kwargs:
				destinationFile = CreatePath (self.nginxConf['server']['root'], self.kwargs['destinationFile'])
			else:
				destinationFile = CreatePath (self.nginxConf['server']['root'], 'index.php')
			url = 'http://www.adminer.org/latest.php'
			urllib.request.urlretrieve (url, destinationFile)
			print ('Новая версия Adminer успешно загружена!')
			return True
		except:
			print ('Ошибка загрузки Adminer!')
			return False
