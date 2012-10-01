class Map(object):

	_model = None
	_routes_tables = None
	_units_pools = None

	''' Metodo construtor da classe. '''
	def __init__(self, model):
		self.set_model(model)

	''' Agrega um modelo contendo o objeto de interface para os dados provenientes do banco de dados. '''
	def set_model(self, model):
		self._model = model

	''' Adiciona um dicionario que representa uma tabela bidimensional contendo as possiveis rotas e seus respectivos transit times. '''
	def add_route_table(self, sheet_name):
		if self._routes_tables == None:
			self._routes_tables = dict()
		from RoutesTable import RoutesTable
		self._routes_tables[sheet_name] = RoutesTable(self._model, sheet_name)

	''' Retorna o dicionario que armazena as possiveis rotas e seus respectivos transit times. '''
	def get_routes_table(self, sheet_name):
		return(self._routes_tables[sheet_name])

	''' Fabrica de objetos derivados de Unit. '''
	def units_factory(self, unit_type, unit_name):
		if unit_type == 'LoadTerminal':
			from LoadTerminal import LoadTerminal
			unit = LoadTerminal(unit_name)
			return(unit)
		elif unit_type == 'UnloadingPoint':
			from UnloadingPoint import UnloadingPoint
			unit = UnloadingPoint(unit_name)
			return(unit)
		elif unit_type == 'Unit':
			from Unit import Unit
			unit = Unit(unit_name)
			return(unit)
		else:
			print('ERROR: invalid unit_type!!!')
			return(None)

	''' As pools sao criadas a partir das tabelas de rotas. '''
	def add_unit_pool(self, pool_type, units_names):
		if self._units_pools == None:
			self._units_pools = dict()
		self._units_pools[pool_type] = dict()
		pool = self._units_pools[pool_type]
		for unit_name in units_names:
			unit = self.units_factory(pool_type, unit_name)
			pool[unit_name] = unit

	''' Retorna uma referencia para o dicionario da pool de objetos. '''
	def get_unit_pool(self, pool_type):
		return(self._units_pools[pool_type])

	''' Retorna o transit-time entre duas unidades. '''
	def get_transit_time(self, source_name, destiny_name):
		cell = None
		for table in self._routes_tables.values():
			value = table.get_cell_value(source_name, destiny_name)
			if value != None:
				cell = value
		return(cell)

	''' Realiza o roteamento entre duas pools de objetos. '''
	def make_routes(self, source_pool, destiny_pool):
		if isinstance(source_pool, str):
			sources = self.get_unit_pool(source_pool).values()
		elif isinstance(source_pool, dict):
			sources = source_pool.values()
		else:
			print('ERROR: source_pool parameter is not of a valid type!')
			return
		if isinstance(destiny_pool, str):
			destinies = self.get_unit_pool(destiny_pool).values()
		elif isinstance(destiny_pool, dict):
			destinies = destiny_pool.values()
		else:
			print('ERROR: destiny_pool parameter is not of a valid type!')
			return
		for source in sources:
			for destiny in destinies:
				source_name = source.get_name()
				destiny_name = destiny.get_name()
				transit_time = self.get_transit_time(source_name, destiny_name)
				if transit_time != None:
					print(source_name, ' -> ', destiny_name, '('+str(transit_time)+')')
					from Route import Route
					route = Route(source, destiny, int(transit_time))
				else:
					print(">> There's no route between", source_name, 'and', destiny_name+'.\n')
