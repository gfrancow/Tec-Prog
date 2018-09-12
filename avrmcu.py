# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
============
Modul AvrMcu
============

Conte una classe que implementa el control general del microcontrolador. Es en certa
manera la classe que aglutina la resta de components.

"""

from state import *
from repertoir import *
from instruction import *
from avrexcept import *
class AvrMcu(object):
	"""
	AvrMcu es una classe les instancies de la qual son simuladors de l MCU AVR. La seva funcio mes
	important es executar un programa escrit en assemblador de l AVR.

	>>> a=AvrMcu()
	>>> p=[Word(1),Word(2),Word(3)]
	>>> a.set_prog(p)
	>>> print a.dump_prog()
	0000: 0001
	0001: 0002
	0002: 0003
	>>> a.reset()
	>>> p=[]
	"""
	def __init__(self):
		'''
        Inicialitza el simulador. Particularment, fa un reset de l estat: esborra les memories,
        inicialitza el PC i les FLAGS a 0. Inicialitza el repertori d instruccions amb les
        instancies d InstRunner corresponents.
		'''
		self.__s=State()
		self.__rep=Repertoir([Add(),Adc(),Sub(),Subi(),And(),Or(),Eor(),Lsr(),Mov(),Ldi(),Sts(),Lds(),Rjmp(),Brbs(),Brbc(),Nop(),Break(),In(),Out()])

	def reset(self):
		'''
        Fa un reset de l estat deixant lo de la mateixa forma que el metode init.
        '''
		self.__s.data=DataMemory()
		self.__s.prog=ProgramMemory()
		self.__s.pc=Word(0)
		self.__s.flags['CARRY']=0
		self.__s.flags['ZERO']=0
		self.__s.flags['NEG']=0

	def set_prog(self,p):
		'''
        p es una llista d enters que representen un programa en llenguatge maquina de l AVR.
        El metode instal la el programa p en la memoria de programa del simulador a partir
        de l adreça 0000.
        '''
		l=[Word(i) for i in p]
		self.__s.prog.setList(l)

	def dump_reg(self):
		'''
        Retorna un string que correspon amb un bolcat dels registres del simulador.
        '''
		return self.__s.data.dump_reg()

	def dump_dat(self):
		'''
        Retorna un str que representa un bolcat de la memoria de dades del simulador.
        '''
		return self.__s.dump_dat()

	def dump_prog(self):
		'''
        Retorna un str que representa un bolcat de la memoria de programa del simulador.
        '''
		return self.__s.dump_prog()

	def run(self):
		'''
        Es el metode principal del simulador. Quan s invoca inicia una iteracio infinita que:
        a) Obte la instruccio indicada pel PC.
        b) Busca un InstRunner que pugui executar aquesta instruccio.
        c) Executa la instruccio.
        El metode te un catcher pel les excepcions UnknownCodeError i BreakException que
        actuen de forma consequent.
        '''
		w=True
		while w:
			try:
				inst=self.__s.prog[self.__s.pc]
				InRu=self.__rep.find(inst)
				InRu.execute(inst,self.__s)
			except BreakException:
				w=False
				print "Fi"


	def set_trace(self,t):
		'''
        Quan s invova amb t=True activa el mode trace de la memoria de dades. Si s activa
        amb t=False es desactiva el mode.
        '''
		if t: self.__s.data.trace_on()
		else: self.__s.data.trace_off()
