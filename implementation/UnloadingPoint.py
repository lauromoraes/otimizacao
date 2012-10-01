from Unit import Unit

class UnloadingPoint(Unit):
	def __init__(self, name):
		Unit.__init__(self, name)
		# Imprime alguns dados para debug, linha opcional.
		print ('UnloadingPoint object', '"'+self.get_name()+'"', 'created at', str(self)+'.\n')