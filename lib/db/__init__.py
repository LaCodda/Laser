import string


class Db ():
	dbTechName = ''

	dbName = ''

	dbDescription = 'Description'

	def __init__ (self, **kwargs):
		self.setDbTechName ()

		if 'dbname' in kwargs and kwargs['dbname'] != 'default':
			self.dbName = kwargs['dbname']
		elif 'serverName' in kwargs:
			self.setDbName (kwargs['serverName'])

	def setDbTechName (self):
		self.dbTechName = self.__class__.__name__

	def setDbName (self, serverName):
		self.dbName = serverName.translate (str.maketrans ('.- ', '___'))
