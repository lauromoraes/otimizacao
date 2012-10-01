class Transaction(object):

	''' Attributes. '''
	_id = None
	_route = None
	_calendar = None
	_product = None

	''' Constructor method. '''
	def __init__(self, route, departure_date, product_type = None, product_amount = 0):
		try:
			from Calendar import Calendar
			#from Product import Product
			self._route = route
			self._calendar = Calendar(departure_date, self._route)
			print(self._calendar)
			#self._product = Product(product_type, product_amount)
			#self.set_id(source, destiny, departure_date)
			#print ('Transaction object', '"'+self.get_id()+'"', 'created at', str(self)+'.\n')
			#print ('Transaction object', 'created at', str(self)+'.\n')
		except ValueError as e:
			print(type(e))
			print(e)
		except:
			print('ERROR: Unexpected error at init method!')

	''' Define id attribute as a concatenation of source and destiny names. '''
	def set_id(self):
		from Unit import Unit
		try:
			source = self._route.get_route_source()
			destiny = self._route.get_route_destiny()
			if isinstance(source, Unit) and isinstance(destiny, Unit):
				source_name = source.get_name()
				destiny_name = destiny.get_name()
				self._id = source_name + '|' + destiny_name
			else:
				raise TypeError('ERROR: source and destiny must be a valid Unit instance!')
		except TypeError as e:
			print(type(e))
			print(e)