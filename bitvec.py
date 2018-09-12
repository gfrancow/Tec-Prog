#!/usr/bin/env python
# -+- coding: utf-8 -+-

"""
=================
MODUL BitVector
=================


Principal perque funcionin la resta de classes

"""

class BitVector(object):
	"""
	Inicialitza un int al BitVector, mentre que self.__w contindra el valor en format unsigned, 		es a dir que el valor que contindran sera de 0 a 255, pero s'ha de saber que compleix el CA2 		per tant s'ha de saber que entre els valors (128-->255) es un numero negatiu i entre (0->127) 		es un numero positiu, no obstant per Words farem que sigui unsigned ( 0 --> 65536).
		
	"""
	
	def __init__(self,w=0):
		self.__w=w
		if self.__class__ is Byte:
			self.__w=int(w)&255
		else:
			self.__w=int(w)&65535

	def getW(self):
		return self.__w
     
	
	def extract_field_u(self,mask):
		"""
		Mask es un enter que sinterpreta om a una mascara binaria. Retorna semppre un enter 			positiu.

		>>> a=BitVector(166)
		>>> print a.extract_field_u(51)
		1010
		>>> a=BitVector(0b0000111001110001)
		>>> print a.extract_field_u(0b1111110000000000)
		11
		"""
		num=self.getW()
		mask=format(mask,'016b')
		num=format(num,'016b')
		newv=""
		for i,v in enumerate(mask):
			if v=='1':
				newv+=num[i]
		newv=int(newv,2)
		return "{0:0b}".format(newv)

	def extract_field_s(self,mask):
		"""
		Fa exactament el mateix que el metode anterior pero interpreta el resultat com un
		enter amb signe. Pot retornar doncs en un enter positiu o negatiu. Sassumeix que la
		codificacio es complement a dos.
		"""
		newn=format(self.__w,'#010b')
		if newn[0]==0:
			return self.extract_field_u(mask)
		else:
			c=2**(len(str(newn)))+self.__w
			return BitVector(c).extract_field_u(mask)

	def __int__(self):
		"""
		Torna el valor enter corresponent a self interpretat sempre com a un valor sense 			signe.
		>>> int(Byte(7))
		7
		>>> int(Byte(0b1011))
		11
		>>> int(Word(403))
		403
		"""
		return self.__w


	def __index__(self):
		"""
		Torna el mateix que en el metode anterior. Consulteu el manual de Python per
		entendre quin paper juga aquest metode.
		"""
		return self.__w

	def __repr__(self):
		"""
		Torna la representacio en hexadecimal del valor del BitVector. Cal tenir en compte
		la llargada de la paraula i escriure sempre el nombre de digits corresponents. Per
		exemple, si la llargada de la paraula es dun byte i el valor es 10, repr hauria
		descriure 0A i no pas A.

		>>> print Byte(10)
		0a
		>>> print Word(10)
		000a
		>>> print Byte(1)
		01
		>>> print Byte(15)
		0f
		>>> print Byte(-1)
		ff
		>>> print Byte(403)
		93
		"""
		if isinstance(self,Byte):
			return format(self.__w,'02x')
		else:
			return format(self.__w,'04x')

	def __add__(self,o):
		"""       
		>>> print Byte(2)+Byte(12)
		0e
		>>> print Byte(12)+2
		0e
		"""
		if isinstance(self,Byte):
			if isinstance(o,Byte):
				return Byte(self.__w + o.__w)
			else:
				return Byte(self.__w + o)
		else:
			if isinstance(o,Byte):
				return Word(self.__w + o.__w)
			else:
				return Word(self.__w + o)

	def __sub__(self,o):
		"""    
		>>> print Byte(12)-Byte(2)
		0a
		>>> print Byte(12)-2
		0a
		"""
		if isinstance(self,Byte):
			if isinstance(o,Byte):
				return Byte(self.__w - o.__w)
			else:
				return Byte(self.__w - o)
		else:
			if isinstance(o,Byte):
				return Word(self.__w - o.__w)
			else:
				return Word(self.__w - o)
	
	def __and__(self,o):
		"""    
		>>> print Byte(8)&Byte(8)
		08
		>>> print Byte(7)&Byte(0b0010)
		02
		>>> print Byte(0xff)&Byte(0b1011)
		0b
		"""
		if isinstance(self,Byte):
			return Byte(self.__w & o.__w)
		else:
			return Word(self.__w & o)

	def __or__(self,o):
		"""    
		>>> print Byte(24)|Byte(8)
		18
		>>> print Byte(7)|Byte(0b0010)
		07
		>>> print Byte(3)|Byte(4)
		07
		"""
		if isinstance(self,Byte):
			return Byte(self.__w | o.__w)
		else:
			return Word(self.__w | o)

		
	def __xor__(self,o):
		"""      
		>>> print Byte(24)^Byte(8)
		10
		>>> print Byte(0xff)^Byte(0b1011)
		f4
		"""
		if isinstance(self,Byte):
			return Byte(self.__w ^ o.__w)
		else:
			return Word(self.__w ^ o)
    
	def __invert__(self):
		"""
		>>> print ~Byte(24)
		e7
		>>> print ~Byte(0xf0)
		0f
		>>> print ~Byte(0b101010)
		d5
		"""
		if isinstance(self,Byte):
			return Byte(~self.__w)
		else:
			return Word(~self.__w)
    

	def __lshift__(self,i):
		"""
		>>> print Byte(1)<<4
		10
		>>> print Byte(0xfe)<<3
		f0
		"""
		try:
			if isinstance(self,Byte):
				return Byte(self.__w<<i)
			else:
				return Word(self.__w<<i)
		except IndexError:
			print "Index out of range"




	def __rshift__(self,i):
		"""
		>>> print Byte(0xff)>>4
		0f
		"""
		try:
			if isinstance(self,Byte):
				return Byte(self.__w>>i)
			elif isinstance(self,Word):
				return Word(self.__w>>i)
			else:
				return self>>i
		except IndexError:
			print "Index out of range"

	def __eq__(self,o):
		"""
		>>> Byte(2)==2
		True
		>>> Byte(8)==Byte(8)
		True
		>>> Byte(12)==-12
		False
		"""
		if isinstance(o,BitVector):
			return self.getW()==o.getW()
		else:
			return self.getW()==o

  

	def __ne__(self,o):
		"""
		>>> Byte(2)!=2
		False
		>>> Byte(8)!=Byte(8)
		False
		>>> Byte(12)!=-12
		True
		"""
		if isinstance(o,BitVector):
			return self.getW()!=o.getW()
		else:
			return self.getW()!=o

	def __getitem__(self,i):
		"""
		>>> Byte(2)[0]
		False
		>>> Byte(2)[1]
		True
		>>> Byte(10)[7]
		False
		>>> Byte(10)[3]
		True
		"""
		try:
			a="{0:0b}".format(self.getW())
			a=a[::-1]
			if i < len(str(a)):
				if a[i]=='1':
					return True
				else: 
					return False
			else:
				return False
		except KeyError:
			print "Index out of range"

	def __setitem__(self,i,v):
		"""
		>>> a=Byte(2)
		>>> a[1]=0
		>>> print a
		00
		>>> b=Byte(4)
		>>> b[0]=1
		>>> print b
		05
		"""
		try:
			b="{0:0b}".format(self.__w)
			b=b[::-1]
			b=list(b)
			b[i]=str(v)
			b=''.join(b)
			b=b[::-1]
			b=int(b,2)
			if isinstance(self,Byte):
				self.__w = b
			else:
				self.__w = b
		except KeyError:
			print "Index out of range"

     
class Byte(BitVector):

	def __init__(self,w):
		"""
		Constructor
		"""
		super(Byte,self).__init__(w)
  
	def __len__(self):
		"""
		>>> print len(Byte(4))
		8
		"""
		return 8

	def concat(self,b):
		"""
		retorna el Word resultant de concatenar self amb el Byte b. self es MSB i b el LSB
		>>> b=Byte(255)
		>>> c=Byte(0)
		>>> d=b.concat(c)
		>>> print d
		ff00
		"""
		a="%s%s" % (format(self.getW(),'02x'),format(b.getW(),'02x'))
		a=int(a,16)
		return Word(int(a))

   
class Word(BitVector):
	def __init__(self,w):
		"""
		Constructor
		"""
		super(Word,self).__init__(w)

	def __len__(self):
		"""
		>>> print len(Word(24))
		16
		"""
		return 16

	def lsb(self):
		"""
        >>> Word(255).lsb()
        ff
        >>> Word(65535).lsb()
        ff
        """
		return Byte(self.getW())

	def msb(self):
		"""
		>>> Word(3697).msb()
		0e
		>>> Word(255).msb()
		00
		>>> Word(65535).msb()
		ff
		""" 
		a= self.getW() & 65280
		a= format(a,'016b')
		a=str(a)[:8]
		a=int(a,2)
		return Byte(a)

		
		#a= a>>8
		#print a


if __name__ == '__main__':
	print Word(3697).msb()
	
	
