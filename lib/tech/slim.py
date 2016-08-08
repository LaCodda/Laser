import os
import shutil
import sys
import tarfile
import urllib.request

from lib.helper import *
from lib.tech.php import Php


class Slim (Php):
	techDescription = 'Slim is a PHP micro framework that helps you quickly write simple yet powerful web applications and APIs'

	def __init__ (self, **kwargs):
		super (Slim, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'      :
				{
					'try_files': '$uri $uri/ /index.php$is_args$args'
				},
			'~ \.php':
				{
					'try_files'                    : '$uri =404',
					'fastcgi_index'                : 'index.php',
					'include'                      : 'fcgi.conf',
					'fastcgi_pass'                 : 'unix:' + self.socket,
					'fastcgi_param SCRIPT_FILENAME': '$document_root$fastcgi_script_name',
					'fastcgi_param SCRIPT_NAME'    : '$fastcgi_script_name',
					'fastcgi_split_path_info'      : '^(.+\.php)(/.+)$',
				},

		}

	def load (self):
		try:
			if self.checkComposer ():
				demoIndexPage = '''<?php
		use \Psr\Http\Message\ServerRequestInterface as Request;
		use \Psr\Http\Message\ResponseInterface as Response;

		require 'vendor/autoload.php';

		$app = new \Slim\App;
		$app->get('/hello/{name}', function (Request $request, Response $response) {
		    $name = $request->getAttribute('name');
		    $response->getBody()->write("Hello, $name");

		    return $response;
		});
		$app->run();'''
				destinationDir = CreatePath (self.nginxConf['server']['root'])
				destinationFile = CreatePath (destinationDir, 'index.php')
				os.chdir (destinationDir)
				os.system ('composer require slim/slim "^3.0"')
				fw = open (destinationFile, "wt")
				fw.write (demoIndexPage)
				fw.close ()
				print ('Новая версия Slim успешно загружена!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Slim по причине отсутствия Composer')
				return False
		except:
			print ('Ошибка загрузки Slim!')
			return False
