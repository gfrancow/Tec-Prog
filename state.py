#!/usr/bin/env python
# -+- coding: utf-8 -+-

from memory import*
from bitvec import*

"""
===========
Modul State
===========

Representa l'estat de la MCU. L'estat d'un computador esta format pel conjunt de tots els registres i memories. Cada vegada qye s'executa una instruccio diferent, l'estat ha de canviar.

"""

class State(object):
	"""
	Aquesta classe representa lestat de la MCU. Lestat dun computador esta format pel conjunt
	de tots els registres i memories. Cada vegada que sexecuta una instruccio, lestat acostuma a
	canviar.

	"""
	def __init__(self, data=128, prog=128):
		"""
		Inicialitza lestat de la MCU. data es el nombre de cel.les de la memoria de dades i
		prog el nombre de cel.les de la memoria de programa.	
		"""
		self.data = DataMemory(data)
		self.prog = ProgramMemory(prog)
		self.pc = Word(0)
		self.flags = {'CARRY':0,'ZERO':0,'NEG':0} # ho he volgut gestionar amb un diccionari per fer-ho més fàcil de tractar

	def dump_dat(self):
		"""
		Retorna un str que representa el bolcat de la memòria de dades.

		>>> print State(data=32).dump_dat()
		0000: 00
		0001: 00
		0002: 00
		0003: 00
		0004: 00
		0005: 00
		0006: 00
		0007: 00
		0008: 00
		0009: 00
		0010: 00
		0011: 00
		0012: 00
		0013: 00
		0014: 00
		0015: 00
		0016: 00
		0017: 00
		0018: 00
		0019: 00
		0020: 00
		0021: 00
		0022: 00
		0023: 00
		0024: 00
		0025: 00
		0026: 00
		0027: 00
		0028: 00
		0029: 00
		0030: 00
		0031: 00
		"""
		return self.data.dump(t=len(self.data))

	def dump_prog(self):
		"""
		Retorna un str que representa el bolcat de la memòria de programa.

		>>> print State(prog=6).dump_prog()
		0000: 0000
		0001: 0000
		0002: 0000
		0003: 0000
		0004: 0000
		0005: 0000
		"""
		return self.prog.dump(t=len(self.prog))

	def dump_reg(self):
		"""
		Retorna un str que representa els registres continguts en l’estat.

		>>> print State(32,32).dump_reg()
		R00: 00
		R01: 00
		R02: 00
		R03: 00
		R04: 00
		R05: 00
		R06: 00
		R07: 00
		R08: 00
		R09: 00
		R10: 00
		R11: 00
		R12: 00
		R13: 00
		R14: 00
		R15: 00
		R16: 00
		R17: 00
		R18: 00
		R19: 00
		R20: 00
		R21: 00
		R22: 00
		R23: 00
		R24: 00
		R25: 00
		R26: 00
		R27: 00
		R28: 00
		R29: 00
		R30: 00
		R31: 00
		X(R27:R26): 0000
		Y(R29:R28): 0000
		Z(R31:R30): 0000
		PC: 0000
		{'CARRY': 0, 'NEG': 0, 'ZERO': 0}
		"""
		a=self.data.dump_reg()
		b='\n'+'PC: '+("{:0>4d}".format(int(self.pc)))+'\n'+str(self.flags)
		return a+b 


if __name__ == '__main__':
	m=State(6,6)
	print len(m.data.getList())
	"""
	[Byte(10),Byte(4),Byte(3),Byte(1),Byte(5)]
	0000: 10
	0001: 04
	0002: 03
	0003: 01
	0004: 05
	"""
	for i in m.data:
		print i
