import sys
from Unit import Unit
from Transaction import Transaction
from ExcelModel import ExcelModel
from RoutesTable import RoutesTable
from Map import Map

''' Globals '''
ROOT = 'D:\\Pesquisa\\projeto_metaheuristicas\\mineradora\\v0.4\\'
EXCEL_VISIBILITY = False
TEST_UNIT = True
TEST_TRANSACTION = False
TEST_MODEL = True

''' Main '''
if __name__ == '__main__':

	''' Testes do modelo. '''
	if TEST_MODEL:
		print('Testing ExcelModel...')
		model = ExcelModel(ROOT + 'entrada_mineradora.xlsx', EXCEL_VISIBILITY)
		transit_time_table = model.get_transit_time_table('lt-up-routes')
		#print(transit_time_table)

	''' Testes das unidades. '''
	if TEST_UNIT:
		print('Testing Unit...\n')

		# Generate load terminals pool
		#load_terminals = model.get_load_terminals('lt-up-routes')
		#print(load_terminals)

		# Generate unloading points pool
		#unloading_points = model.get_unloading_points('lt-up-routes')
		#print(unloading_points)


		''' Cria um objeto do tipo Map. '''
		map = Map(model)

		''' Adiciona ao objeto uma tabela de rotas entre terminais de carga e pontos de descarga. '''
		map.add_route_table('lt-up-routes')

		''' Cria uma lista com os nomes das origens (terminais de carga) de cada rota da tabela. '''
		sources_names = map.get_routes_table('lt-up-routes').get_table_sources_names()

		''' Cria uma lista com os nomes dos destinos (pontos de descarga) de cada rota da tabela. '''
		destinies_names = map.get_routes_table('lt-up-routes').get_table_destinies_names()

		''' Gera uma nova pool no objeto map, usando a lista de nomes dos terminais de carga. '''
		map.add_unit_pool('LoadTerminal', sources_names)

		''' Gera uma nova pool no objeto map, usando a lista de nomes dos pontos de descarga. '''
		map.add_unit_pool('UnloadingPoint', destinies_names)

		''' Retorna a pool de terminais de carga criada. '''
		lt_pool = map.get_unit_pool('LoadTerminal')

		''' Retorna a pool de pontos de descarga criada. '''
		up_pool = map.get_unit_pool('UnloadingPoint')

		''' Percorre todos os elementos da pool de terminais de carga. '''
		for index, unit in lt_pool.items():
			''' Imprime os nomes dos objetos do tipo Unit presentes na pool e seus indices na pool. '''
			print(unit.get_name(), '=', index)

		''' Percorre todos os elementos da pool de pontos de descarga. '''
		for index, unit in up_pool.items():
			''' Imprime os nomes dos objetos do tipo Unit presentes na pool e seus indices na pool. '''
			print(unit.get_name(), '=', index)

		''' Retona o transit-time entre duas unidades, caso nao exista retorna None. '''
		#print( 'Transit-time( tc-01 | pd-03 ) =', map.get_transit_time('tc-01', 'pd-03') )

		''' Cria as rotas entre os terminais de carga e os pontos de descarga. '''
		# Todas as seguintes chamadas sao (devem ser) validas
		#map.make_routes(lt_pool, up_pool)
		#map.make_routes('LoadTerminal', up_pool)
		#map.make_routes(lt_pool, 'UnloadingPoint')
		map.make_routes('LoadTerminal', 'UnloadingPoint')

	''' Testes das transacoes. '''
	if TEST_TRANSACTION:
		print('Testing Transaction...')
		# Cria um novo objeto do tipo Transaction
		t1 = Transaction(u1, u2, 10)

	print('END')