#!/usr/bin/env python
# -+- coding: utf-8 -+-
from bitvec import*
from instruction import*
from avrexcept import*


"""
===============
Modul Repertoir
===============

Repertoir es una classe les instancies de la qual son conjunt de InstRunners. Representen el
conjunt dinstruccions dun MCU. La seva funcionalitat mes caracteristica es la que, donada una
instruccio, retorna lobjecte InstRunner que es capac dexecutar-la.

"""

class UnknownCodeError(AVRException):
	"""
	Es una excepcio que saixeca quan cal executar una instruccio de llenguatge maquina i aquesta
	no és coneguda.
	"""
	pass
class Repertoir(object):
	"""
	Repertoir es una classe les instancies de la qual son conjunt de InstRunners. Representen el
	conjunt dinstruccions dun MCU. La seva funcionalitat mes caracteristica es la que, donada 		una instruccio, retorna lobjecte InstRunner que es capac dexecutar-la.
	"""
	def __init__(self,li):
		self.__li=li

	def find(self,instr):
		t=False
		for i in self.__li:
			if i.match(instr):
				t=True
				return i
		if t==False:
			raise UnknownCodeError
		
if __name__ == '__main__':
	a=Repertoir([Nop()])
	a.find(Word(0b0000000000000000))
	
