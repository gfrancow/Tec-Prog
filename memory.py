# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""

.. image:: image.jpeg
   :width: 300pt

============
Modul Memory
============

Conte diverses classes que tenen com a objectiu representar les paraules de diferent longitud
que intervenen en la simulacio.

"""

from avrexcept import *
from bitvec import *

class Memory(object):
	 """
	 Representa un banc de memoria. Es abstracta i, per tant, no poden haver hi objectes instanciats de la classe sino que sempre ho son de les seves subclasses DataMemory i ProgramaMemory.
	 """
	 def __init__(self,m=[],trace=False):
		 """
		 Assigna False a _trace_.
		 """
		 self.__m = m   #Banc de memoria (llista de Word o Byte)
		 self.__trace = trace 	#Bool: indica funcionalitat de traçada

	 def __len__(self):
		"""
		Retorna la llista de word o bytes.

        >>> print len(Memory([Word(3)]))
		1
		"""
		return len(self.__m)

	 def __repr__(self):
		"""
		Retorna un string que conte un bolcat del banc de memoria en un format exactament com el que segueix (en el cas que les cel.les siguin Byte):
        0000: 00
        0001: 01

		>>> print Memory([Byte(1)])
		0000: 01
		>>> print Memory([Word(3)])
		0000: 0003
		"""
		for i,v in enumerate(self.__m):
			if isinstance(v,Byte):
				return ("{:0>4d}".format(int(i)))+': '+("{:0>2d}".format(int(v)))
			elif isinstance(v,Word):
				return ("{:0>4d}".format(int(i)))+': '+("{:0>4d}".format(int(v)))
			else:
				return "It's neither a Byte nor a Word!"

	 def __getitem__(self,addr):
		"""
		>>> m=Memory([Byte(1),Word(3)])
		>>> print m[1]
		0003
		>>> m.trace_on()
		>>> print m[1]
		Read 03 from 0001
		0003
		"""
		try:
			if not self.__trace:
				return self.__m[addr]
			else:
				print 'Read {:0>2x} from {:0>4x}'.format(int(self.__m[addr]),addr)
				return self.__m[addr]
		except IndexError:
				raise OutOfMemError('Readfrom{0:x}outofrange'.format(addr))

	 def __setitem__(self,addr,val):
		"""
		>>> m=Memory([Byte(1),Word(3)])
		>>> m[1]=Word(4)
		>>> m.trace_on()
		>>> m[1]=Word(10)
		Write 0a to 0001
		"""
		try:
			if not self.__trace:
				self.__m[addr]=val
			else:
				self.__m[addr]=val
				print 'Write {:0>2x} to {:0>4x}'.format(int(val),addr)
		except IndexError:
				raise OutOfMemError('Writeto{0:x}outofrange'.format(addr))

	 def getList(self):
		"""
		>>> print Memory([Byte(1),Word(3)]).getList()
		[01, 0003]
		"""
		return self.__m

	 def setList(self,l):
		self.__m=l

	 def trace_on(self):
		self.__trace=True

	 def trace_off(self):
		self.__trace=False

	 def dump(self,f=0,t=5):
		"""
		Retorna un string el qual conte un bolcat del banc de memoria exactament com en el cas de __repr__. No obstant, nomes de les cel.les que estan en l interval d adreces [f,t).

		>>> print Memory([Byte(10),Byte(4),Byte(3),Byte(1),Byte(5)]).dump(1,3)
		0001: 04
		0002: 03
		>>> print Memory([Word(3),Byte(3)]).dump(0,2)
		0000: 0003
		0001: 03
		"""
		s=''
		if isinstance(self,ProgramMemory) or isinstance(self,DataMemory):
			for i,v in enumerate(self.getList()[f:t]):
				if isinstance(v,Byte):
					s+=("{:0>4d}".format(int(f+i)))+': '+("{:0>2d}".format(int(v)))+'\n'
				elif isinstance(v,Word):
					s+=("{:0>4d}".format(int(f+i)))+': '+("{:0>4d}".format(int(v)))+'\n'
				else:
					return "It's neither a Byte nor a Word!"
		else:
			for i,v in enumerate(self.getList()[f:t]):
				if isinstance(v,Byte):
					s+=("{:0>4d}".format(int(f+i)))+': '+("{:0>2d}".format(int(v)))+'\n'
				elif isinstance(v,Word):
					s+=("{:0>4d}".format(int(f+i)))+': '+("{:0>4d}".format(int(v)))+'\n'
				else:
					return "It's neither a Byte nor a Word!"
		return s[:-1]

"""
Els seguents dos metodes implementes les operacions d acces a la memoria. addr es un int, o qualsevol altre objecte que implementi el metode «index» (en particular word). Correspon amb l adreca de memoria a la qual es vol axcedir. Val es un bitvector de la mateix amida que la cel la de la memoria, ja sigui Byte o Word.
	Getitem torna una paraula de la mida de la cela de la memoria. Si _trace == True (esta activada), cada vegada que es fa un acces a la memoria printa un missatge com el seguent:
a. Quina operacio s ha fet (read o write)
b. A quina addreca de memoria s ha accedit.
c. Quin valor s ha llegit i/o escrit.
"""

class ProgramMemory(Memory):
	"""
	Representa un banc de memoria per guardar programaes. Les dades guardades son de mida Word.

	>>> print ProgramMemory(2).dump(0,2)
	0000: 0000
	0001: 0000
	"""
	def __init__(self,ncells=1024):
		"""
        Inicialitza un banc de memoria d amplada Word i ncells cel.les.
        """
		super(ProgramMemory,self).__init__()
		l=[]
		for i in range(ncells):
			l.append(Word(0))
		self.setList(l)

class DataMemory(Memory):
	"""
    Representa un banc de memoria per guardar dades. Per tant, les dades guardades son de mida Byte
    """
	def __init__(self,ncells=1024):
		super(DataMemory,self).__init__()
		if ncells<32:
			ncells=32
		l=[]
		for i in range(ncells):
			l.append(Byte(0))
		self.setList(l)

	def dump_reg(self):
		"""
		Retorna un string el qual representa els registres continguts en el banc de memoria en un format com el que segueix:
		R00: 00
		R01: 00
		...
		R31: 00
		x(R27: R26): 0000
		Y(R29: R28): 0000
		Z(R31: R30): 0000

		>>> print DataMemory(32).dump_reg()
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
		"""
		s=''
		for i,v in enumerate(self.getList()):
			s+='R{:0>2d}: {:0>2x}\n'.format(i,int(v))
			if i==31:
				break
		s+='X(R27:R26): {:0>4x}\n'.format(int(("{:0>2x}".format(int(self.getList()[27]))+"{:0>2x}".format(int(self.getList()[26])))))
		s+='Y(R29:R28): {:0>4x}\n'.format(int(("{:0>2x}".format(int(self.getList()[29]))+"{:0>2x}".format(int(self.getList()[28])))))
		s+='Z(R31:R30): {:0>4x}'.format(int(("{:0>2x}".format(int(self.getList()[31]))+"{:0>2x}".format(int(self.getList()[30])))))
		return s


class OutOfMemError(AVRException):
	"""
    Es una excpecio que denota un acces a un banc de memoria amb una adreca inexistent.
    """
	pass




if __name__ == '__main__':
	print 'Test passed.'
	#m=['00' for q in range(32)]
	#s=''
	#for i,v in enumerate(m):
	#	s+='R{:0>2d}: {:0>2x}\n'.format(i,int(v))
	#s+='X(R27:R26): {:0>4x}\n'.format(int(("{:0>2x}".format(int(m[27]))+"{:0>2x}".format(int(m[26])))))
	#s+='Y(R29:R28): {:0>4x}\n'.format(int(("{:0>2x}".format(int(m[29]))+"{:0>2x}".format(int(m[28])))))
	#s+='Z(R31:R30): {:0>4x}'.format(int(("{:0>2x}".format(int(m[31]))+"{:0>2x}".format(int(m[30])))))
	#print s
	pm=ProgramMemory(2)
	print pm.dump(0,2)
	#for i in pm.getList():
	#	print isinstance(i,Word)
	#h=Memory()
	#h.setList(['petnis'])
	#for i in pm.getm():
	#	print i
	#print 'aaaaaaaaaaaaa'
	#for i in h.getList():
	#	print i
