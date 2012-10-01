class Unit(object):

	_name = None
	_inputs = dict()
	_outputs = dict()
	_programming_inputs = dict()
	_programming_outputs = dict()
	_total_accumulated_products = dict()
	_transit_time = dict()

	def __init__(self, name):
		self._name = name

	def get_name(self):
		return(self._name)

	def add_input(self, input):
		import Transaction
		try:
			if isinstance(input, Unit):
				input_name = input.get_name()
				self._inputs[input_name] = input
				self._programming_inputs[input_name] = []
				transaction = Transaction(self, self._inputs[input_name])
				[self._programming_inputs[input_name].insert(transaction, (day+1)) for day in range(30)]
			else:
				raise TypeError('TypeError: input parameter must be a Unit instance.')
		except TypeError as e:
			print(type(e))
			print(e)
		except:
			print('ERROR: Unexpected error at add_input method!')

	def add_output(self, output):
		try:
			if isinstance(output, Unit):
				output_name = output.get_name()
				self._outputs[output_name] = output
				self._programming_outputs[input_name] = []
				transaction = Transaction(self, self._inputs[input_name])
				[self._programming_inputs[input_name].insert(transaction, (day+1)) for day in range(30)]
			else:
				raise TypeError('TypeError: input parameter must be a Unit instance.')
		except TypeError as e:
			print(type(e))
			print(e)
		except:
			print('ERROR: Unexpected error at add_input method!')

	def set_transit_times(self, transit_table):
		self._transit_time = transit_table[self.get_name()]

	def get_transit_times(self, output):
		return(self._transit_time[output.get_name()])
