from win32com.client import Dispatch
import traceback

#from inspect import *
#from functools import *
#import os
#import pprint
#pp = pprint.PrettyPrinter(indent=4)

class ExcelModel(object):

	''' Cria um objeto e abre uma conexao com um arquivo xls ou xlsx. '''
	def __init__(self, file_name, visibility = False):
		try:
			self.file_name = file_name
			self.excel = Dispatch('Excel.Application')
			self.workbook = self.excel.Workbooks.Open(file_name)
			# Define a visiblidade do documento
			self.excel.Visible = visibility
			# Imprime o nome de todas a planilhas da pasta
			print(' | '.join([sheet.Name for sheet in self.workbook.Sheets]))
			self.objects = []
		except:
			print("ERRO: Nome invalido para o workbook!")
			return
		finally:
			print("Modelo carregado com sucesso.")

	''' Imprime uma planilha especificada por seu nome como parametro. '''
	def print_sheet(self, sheet_name):
		if self.workbook is None:
			print("ERRO: nao existe um workbook!")
		else:
			try:
				sheet = self.workbook.Worksheets(sheet_name)
				sheet.Activate()
			except:
				print("ERRO: Nome invalido para o worksheet!")
				return
			for row in range(1,self.get_rows_number(sheet)):
				print(' | '.join([str(sheet.Cells(row,col)) for col in range(self.get_cols_number(sheet))]))

	''' Retorna o numero de linhas utilizadas em uma planilha. '''
	def get_rows_number(self, sheet):
		return sheet.UsedRange.Rows.Count

	''' Retorna o numero de colunas utilizadas em uma planilha. '''
	def get_cols_number(self, sheet):
		return sheet.UsedRange.Columns.Count

	''' Limpa a planilha removendo linhas nulas. '''
	def clean_blank_rows(self, sheet_name):
		if self.workbook is None:
			print("ERRO: nao existe um workbook!")
		else:
			try:
				sheet = self.workbook.Worksheets(sheet_name)
				sheet.Activate()
			except:
				print("ERRO: Nome invalido para o worksheet!")
				return
			blanks_rows = []
			nrows = self.get_rows_number(sheet)+1
			ncols = self.get_cols_number(sheet)+1
			for row in range(1,nrows):
				sheet.Rows(row).EntireRow.Select()
				is_blank_row = True
				for col in range(1,ncols):
					if sheet.Cells(row,col).Value != None:
						is_blank_row = False
						break
				if is_blank_row == True:
					blanks_rows.append(row)
			if len(blanks_rows) == 0:
				print("This sheet has no blank rows!")
			else:
				print("Blanks rows(",len(blanks_rows),"): ",blanks_rows)
				for row in blanks_rows:
					# DESCOBRIR PORQUE DELETA A ULTIMA LINHA DESTE EXEMPLO!!!
					print('rw',row)
					sheet.Rows(row).EntireRow.Delete()
					pass

	'''
		Este metodo extrai valores da tabela e monta um dicionario bidimensional que representa o transit-time entre as possiveis rotas.
		A tabela deve estar sempre configurada corretamente, segundo as seguintes regras:
		> O dicionario caracteriza-se como: dicionario[origem][destino] = Valor
		> A celula(1,1) e sempre ignorada.
		> A primeira linha contem os nomes dos destinos.
		> A primeira celula de cada linha, a partir da segunda linha, contem o nome da origem.
		> A celulas intermediarias contem os valores, sendo que uma celula VAZIA representa a ausencia de rota entre origem e destino.
	'''
	def get_transit_time_table(self, sheet_name):
		# Verifica disponibilidade de um workbook
		if self.workbook is None:
			print("ERRO: nao existe um workbook!")
		else:
			try:
				# Seleciona a worksheet parametrizada
				sheet = self.workbook.Worksheets(sheet_name)
				# Ativa a worksheet para visualizacao
				sheet.Activate()
			except:
				print("ERRO: Nome invalido para o worksheet!")
				return
			# Define a variavel que contera o dicionario bidimensional
			transit_times = dict()
			# Percorre as linhas a partir da segunda ate o final
			for row in range(2, self.get_rows_number(sheet)+1):
				# Gera a primeira chave do dicionario
				key1 = str(sheet.Cells(row, 1))
				# Cria o campo no dicionario como um novo dicionario
				transit_times[key1] = dict()
				# Percorre as colunas a partir da segunda ate o final
				for col in range(2, self.get_cols_number(sheet)+1):
					# Gera a segunda chave do dicionario
					key2 = str(sheet.Cells(1, col))
					# Grava o valor do transit-time
					transit_times[key1][key2] = sheet.Cells(row, col).Value
			# Retorna o dicionario
			return(transit_times)

	''' Metodo fabrica de objetos do tipo Order. '''
	def extract_orders(self, sheet_name):
		# Associa o numero da coluna ao campo
		order_name = 1
		due_date = 2
		penalty = 3
		# Verifica disponibilidade de um workbook
		if self.workbook is None:
			print("ERRO: nao existe um workbook!")
		else:
			try:
				# Seleciona a worksheet parametrizada
				sheet = self.workbook.Worksheets(sheet_name)
				# Ativa a worksheet para visualizacao
				sheet.Activate()
			except:
				print("ERRO: Nome invalido para o worksheet!")
				return
			# Percorre as linhas, cria os objetos do tipo Order e os insere na pool
			for row in range(2,self.get_rows_number(sheet)):
				# Encontra o inicio do registro de um pedido
				if sheet.Cells(row,order_name).Value is not None:
					order = Order(sheet.Cells(row,order_name).Value)
					order.set_sup_row(row)
					self.orders_pool.append(order)
					# Encontra a linha final do registro da order na planilha
					while(sheet.Cells(row+1,order_name).Value is None and row+1 <= self.get_rows_number(sheet)):
						row += 1
					self.orders_pool[-1].set_inf_row(row)
				else:
					pass
			# Para cada objeto da pool, percorre a planilha configurando-os
			for order in self.orders_pool:
				order.set_due_date(sheet.Cells(order.get_sup_row(),due_date).Value)
				order.set_penalty(sheet.Cells(order.get_sup_row(),penalty).Value)
				print(order.name,' - ',order.due_date,' - ',order.penalty)

	def get_load_terminals(self, sheet_name):
		# Verifica disponibilidade de um workbook
		if self.workbook is None:
			print("ERRO: nao existe um workbook!")
		else:
			try:
				# Seleciona a worksheet parametrizada
				sheet = self.workbook.Worksheets(sheet_name)
				# Ativa a worksheet para visualizacao
				sheet.Activate()
			except:
				print("ERRO: Nome invalido para o worksheet!")
				return
			from Unit import Unit
			load_terminals = dict()
			for row in range(2, self.get_rows_number(sheet)+1):
				key1 = str(sheet.Cells(row, 1))
				load_terminals[key1] = Unit(key1)
			return(load_terminals)

	def get_unloading_points(self, sheet_name):
		# Verifica disponibilidade de um workbook
		if self.workbook is None:
			print("ERRO: nao existe um workbook!")
		else:
			try:
				# Seleciona a worksheet parametrizada
				sheet = self.workbook.Worksheets(sheet_name)
				# Ativa a worksheet para visualizacao
				sheet.Activate()
			except:
				print("ERRO: Nome invalido para o worksheet!")
				return
			from Unit import Unit
			unloading_points = dict()
			for col in range(2, self.get_cols_number(sheet)+1):
				key1 = str(sheet.Cells(1, col))
				unloading_points[key1] = Unit(key1)
			return(unloading_points)

	def __del__(self):
		print('Fim do programa.')
		i = input('Deseja salvar alteracoes: S | N\n')
		save = True if (i=='S' or i=='s') else False
		try:
			# Fecha a visualizacao do Excel
			self.excel.Visible = False
			# Fecha o workbook e salva as alteracoes caso seja requisitado
			self.workbook.Close(SaveChanges=save)
			# Fecha a aplicacao Excel
			self.excel.Quit()
			# Destroi o objeto workbook
			del self.workbook
			# Destroi o objeto aplicacao Excel
			del self.excel
		except:
			print('Ocorreu algum erro ao fechar a aplicacao.')
			print(traceback.format_exec())
			pass
		print("Modelo destruido com sucesso.")