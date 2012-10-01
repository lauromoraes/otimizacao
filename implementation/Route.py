class Route(object):

	_source = None
	_destiny = None
	_transit_time = None
	_transactions = None

	''' Contructor method. '''
	def __init__(self, source, destiny, transit_time = None):
		self.change_route(source, destiny)
		self.set_transit_time(transit_time)
		self.set_transactions_programming()
		print ('Route object', '"'+self._source.get_name()+"-->"+self._destiny.get_name()+'"', 'created at', str(self)+'.\n')

	''' Insert a Unit instance as a source. '''
	def set_source(self, source):
		from Unit import Unit
		try:
			if isinstance(source, Unit):
				self._source = source
			else:
				raise TypeError('TypeError: source parameter must be a Unit instance.')
		except TypeError as e:
			print(type(e))
			print(e)
		except:
			print('ERROR: Unexpected error at set_source method!')

	''' Insert a Unit instance as a destiny. '''
	def set_destiny(self, destiny):
		from Unit import Unit
		try:
			if isinstance(destiny, Unit):
				self._destiny = destiny
			else:
				raise TypeError('TypeError: destiny parameter must be a Unit instance.')
		except TypeError as e:
			print(type(e))
			print(e)
		except:
			print('ERROR: Unexpected error at set_destiny method!')

	''' Realiza a troca da origem e do destino da rota. '''
	def change_route(self, source, destiny):
		self.set_source(source)
		self.set_destiny(destiny)

	''' Retorna a origem de uma rota. '''
	def get_route_source(self):
		return(self._source)

	''' Retorna o nome da origem de uma rota. '''
	def get_route_source_name(self):
		return(self._source.get_name())

	''' Retorna o destino de uma rota. '''
	def get_route_destiny(self):
		return(self._destiny)

	''' Retorna o nome do destino de uma rota. '''
	def get_route_destiny_name(self):
		return(self._destiny.get_name())

	''' Armazena o valor do transit-time entre origem e destino. '''
	def set_transit_time(self, transit_time):
		self._transit_time = transit_time

	''' Retorna o valor do transit-time entre origem e destino. '''
	def get_transit_time(self):
		return(self._transit_time)

	''' Retorna o identificador da rota. '''
	def get_id(self):
		return(self.get_route_source_name()+'|'+self.get_route_destiny_name())

	def set_transactions_programming(self):
		self._transactions = list()
		from Transaction import Transaction
		source = self.get_route_source()
		destiny = self.get_route_destiny()
		for i in range(30):
			self._transactions.append( Transaction( self, (i+1) ) )