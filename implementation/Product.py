class Product(object):

	_product_type = None
	_product_amount = None

	def __init__(self, product_type, product_amount):
		self.set_product_type(product_type)
		self.set_product_amount(product_amount)

	''' Define the product amount of the Product. '''
	def set_product_type(self, product_type):
		try:
			if product_type != None:
				self._product_type = product_type
			else:
				raise TypeError('ERROR: product_amount must be a valid int number!')
		except TypeError as e:
			print(type(e))
			print(e)

	''' Define the product amount of the Product. '''
	def set_product_amount(self, product_amount):
		try:
			if isinstance(product_amount, int) and product_amount >= 0:
				self._product_amount = product_amount
			else:
				raise TypeError('ERROR: product_amount must be a valid int number!')
		except TypeError as e:
			print(type(e))
			print(e)

	def get_product_type(self):
		return(self._product_type)

	def get_product_amount(self):
		return(self._product_amount)