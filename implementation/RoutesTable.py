class RoutesTable(object):

	_id = None
	_table = None

	def __init__(self, model, sheet_name):
		self.set_table(model, sheet_name)
		self.set_id(sheet_name)

	''' Agrega uma tabela bidimensional a partir do modelo associado. '''
	def set_table(self, model, sheet_name):
		self._table = model.get_transit_time_table(sheet_name)

	''' Define o identificador unico da tabela. Que e o proprio nome da planilha. '''
	def set_id(self, sheet_name):
		self._id = sheet_name

	''' Retorna o identificador unico da tabela. '''
	def get_id(self):
		return(self._id)

	''' Retorna uma referencia para a tabela agregada. '''
	def get_table(self):
		return(self._table)

	''' Considerendo que a tabela bidimensional contem como coluna primaria os nomes das origens das rotas, retorna estes. '''
	def get_table_sources_names(self):
		return(list(self._table.keys()))

	''' Considerendo que a tabela bidimensional contem como linha primaria os nomes dos destinos das rotas, retorna estes. '''
	def get_table_destinies_names(self):
		keys = list(self._table.keys())
		return(list(self._table[keys[0]].keys()))

	''' Retorna o valor da celula requisitada atraves dos indices da linha e coluna informados por parametros. '''
	def get_cell_value(self, row_index, col_index):
		return(self._table[row_index][col_index])
