class Calendar(object):

	_departure_date = None
	_arrival_date = None

	def __init__(self, departure_date, route):
		self.set_departure_date(departure_date)
		self.set_arrival_date(route)

	def __str__(self):
		return('Calendar object "'+str(self.get_departure_date())+'-->'+str(self.get_arrival_date())+'"')

	''' Define the departure date of the Calendar. '''
	def set_departure_date(self, departure_date):
		try:
			if isinstance(departure_date, int) and departure_date > 0 and departure_date < 32:
				self._departure_date = departure_date
			else:
				raise TypeError('ERROR: departure_date must be a valid int number!')
		except TypeError as e:
			print(type(e))
			print(e)

	''' Define the arrival date of the Calendar. '''
	def set_arrival_date(self, route):
		from Unit import Unit
		from Route import Route
		try:
			source = route.get_route_source()
			destiny = route.get_route_destiny()
			if isinstance(source, Unit) and isinstance(destiny, Unit):
				transit = route.get_transit_time()
				if transit != None:
					self._arrival_date = self._departure_date + transit
					#print('departure_date = ', self.get_departure_date(), '| arrival_date = ', self.get_arrival_date())
				else:
					print('ERROR: nao ha rota entre estes dois pontos')
			else:
				raise TypeError('ERROR: source and destiny must be a valid Unit instance!')
		except TypeError as e:
			print(type(e))
			print(e)

	def get_departure_date(self):
		return(self._departure_date)

	def get_arrival_date(self):
		return(self._arrival_date)