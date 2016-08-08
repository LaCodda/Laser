import importlib
import inspect
import json
import os


class Helper:
	def __init__ (self):
		pass


class Json:
	jsonDict = {}
	jsonOutput = ''

	def __init__ (self, dict, output):
		self.jsonDict = dict
		self.jsonOutput = output

	def save (self):
		try:
			fw = open (self.jsonOutput, "wt")
			fw.write (json.dumps (self.jsonDict, indent=4, sort_keys=True))
			fw.close ()
			return True
		except:
			print ('Ошибка сохранения json файла')
			return False

	def update (self):
		try:
			if os.path.exists (self.jsonOutput):
				with open (self.jsonOutput) as jsonFile:
					jsonData = json.load (jsonFile)
				self.jsonDict.update (jsonData)
			self.save ()
		except:
			print ('Ошибка обновления json файла')
			return False


class CreatePath:
	def __new__ (self, *args):
		resultList = []
		for path in args:
			resultList += path.split ('/')
		return '/' + '/'.join (filter (None, resultList))


class LoadClass:  # dynamically load a class from a string
	def __new__ (self, *args, **kwargs):
		try:
			resultList = []
			for arg in args:
				resultList += arg.split ('.')
			moduleName = ('.'.join (resultList[:-1])).lower ()
			className = resultList[-1].capitalize ()
			module = importlib.import_module (moduleName)
			if 'no_args' in kwargs and kwargs['no_args'] == True:
				return getattr (module, className) ()
			elif kwargs:
				return getattr (module, className) (**kwargs)
			else:
				return getattr (module, className)
		except:
			# print ('Ошибка загрузки модуля')
			return False


class Permissions:
	name = ''

	def __init__ (self, name):
		self.name = name

	def checkAndAddUser (self):
		import pwd

		try:
			pwd.getpwnam (self.name)
			return True
		except KeyError:
			print('User {} does not exist.'.format (self.name))
			return False

	def checkAndAddGroup (self):
		import grp

		try:
			grp.getgrnam (self.name)
			return True
		except KeyError:

			print('Group {} does not exist, but it will be add now.'.format (self.name))
			if self.addGroup ():
				print('Group {} was added.'.format (self.name))
				return True
			else:
				print('Error! Group {} was not added.'.format (self.name))
				return False

	def addGroup (self):
		try:
			os.system ("sudo groupadd {}".format (self.name))
			return True
		except:
			return False


class ClassAttr:
	def __new__ (self, Class):
		boring = dir (type ('Foo', (object,), {}))
		members = [item for item in inspect.getmembers (Class) if item[0] not in boring and not inspect.ismethod (item[1]) and not hasattr (item[1], '__dict__') and item[0] != 'config']
		return {member[0]: member[1] for member in members}
