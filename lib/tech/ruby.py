import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech import Tech


class Ruby (Tech):
	techDescription = 'Ruby Description'

	def __init__ (self, **kwargs):
		super (Ruby, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/':
				{
					'proxy_pass'      : 'http://unix:' + self.socket,
					'proxy_set_header': [
						'Host $http_host',
						'X-Real-IP $remote_addr',
						'X-Forwarded-Proto $scheme',
						'X-Forwarded-For $proxy_add_x_forwarded_for'
					]
				}
		}

		self.techConf = [
			"bind 'unix:/home/vagrant/socket/ruby-dev-laser-0.sock'",
			"daemonize",
			"preload_app!",
			"workers 4"
		]

		self.confFile = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['config'], 'puma_config.rb')

		self.serverStart = 'puma -C {} {}'.format (self.confFile, 'index:app')

	def load (self):
		try:
			if self.checkPuma ():
				demoIndexPage = '''app do |env|
	puts env
	body = 'Hello, World!'
	[200, { 'Content-Type' => 'text/plain', 'Content-Length' => body.length.to_s }, [body]]
end'''
				destinationDir = CreatePath (self.nginxConf['server']['root'])
				destinationFile = CreatePath (destinationDir, 'index.py')
				os.chdir (destinationDir)
				fw = open (destinationFile, "wt")
				fw.write (demoIndexPage)
				fw.close ()
				print ('Демонстрационный файл успешно создан!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Ruby по причине отсутствия Gunicorn')
				return False
		except:
			print ('Ошибка загрузки Ruby!')
			return False

	def configCreate (self):
		config = ''
		for value in self.kwargs['techConf']:
			config += "{}\n".format (value)
		fw = open (self.kwargs['confFile'], "wt")
		fw.write (config)
		fw.close ()

	def start (self):
		# TODO: заменить более правильным решением
		os.system (self.kwargs['serverStart'])

	def stop (self):
		# TODO: заменить более правильным решением
		os.system ("kill -9 `ps aux | grep puma | awk '{print $2}'`")

	def checkPuma (self):
		try:
			path = shutil.which ("puma")
			if path:
				return True
			else:
				return self.installPuma ()
		except:
			print ('Ошибка выполнения проверки установки Puma!')
			return False

	def installPuma (self):
		try:
			os.system ('gem install puma')
			print ('Новая версия Puma успешно установлена!')
			return True
		except:
			print ('Ошибка установки Puma!')
			return False

		# Ruby
		# cd ~/
		# rails new railsapp --skip-bundle
		# cd ~/railsapp
		# echo "gem 'therubyracer',  platforms: :ruby" >> Gemfile
		# bundle install
		# #kill -9 `ps aux | grep rails | awk '{print $2}'`
		# #rails s -d #server
		# kill -9 `ps aux | grep puma | awk '{print $2}'`
		# puma -d -b unix:/var/run/puma_rails-test_dev.sock
		# sudo cp -avr ~/Backups/srv/sites-available /etc/nginx
		# sudo ln -s /etc/nginx/sites-available/rails-test.dev /etc/nginx/sites-enabled/rails-test.dev
		# sudo service nginx restart
