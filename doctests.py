    def __add__(self,o):
        """       
        >>> Byte(2)+Byte(12)
        0E
        >>> Byte(12)+2
        0E
        """
     

    def __sub__(self,o):
        """    
        >>> Byte(12)-Byte(2)
        0A
        >>> Byte(12)-2
        0A
        """
     

    def __and__(self,o):
        """    
        >>> Byte(8)&Byte(8)
        08
        >>> Byte(7)&Byte(0b0010)
        02
        >>> Byte(0xff)&Byte(0b1011)
        0B
        """
     

    def __or__(self,o):
        """    
        >>> Byte(24)|Byte(8)
        18
        >>> Byte(7)|Byte(0b0010)
        07
        >>> Byte(3)|Byte(4)
        07
        """
      

    def __xor__(self,o):
        """      
        >>> Byte(24)^Byte(8)
        10
        >>> Byte(0xff)^Byte(0b1011)
        F4
        """
    
    def __invert__(self):
        """
        >>> ~Byte(24)
        E7
        >>> ~Byte(0xf0)
        0F
        >>> print ~Byte(0b101010)
        D5
        """
    

    def __lshift__(self,i):
        """
        >>> Byte(1)<<4
        10
        >>> Byte(0xfe)<<3
        F0
        """
     

    def __rshift__(self,i):
        """
        >>> Byte(0xff)>>4
        0F
        """
    

   
    def __eq__(self,o):
        """
        >>> Byte(2)==2
        True
        >>> Byte(8)==Byte(8)
        True
        >>> Byte(12)==-12
        False
        """
  

    def __ne__(self,o):
       """
        >>> Byte(2)!=2
        False
        >>> Byte(8)!=Byte(8)
        False
        >>> Byte(12)!=-12
        True
        """
     

    def __getitem__(self,i):
        """
        >>> Byte(2)[0]
        False
        >>> Byte(2)[1]
        True
        >>> Byte(10)[7]
        False
        """

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

     
    
class Byte(BitVector):

    def __init__(self,w):
    """
    Constructor
    """
  
    def __len__(self):
    """
    >>> print len(Byte(4))
    8
        """
     

    def concat(self,b):
        """
        retorna el Word resultant de concatenar self amb el Byte b. self es MSB i b el LSB
        >>> b=Byte(255)
        >>> c=Byte(0)
        >>> d=b.concat(c)
        >>> print d
        F0
        """

   
class Word(BitVector):
    def __init__(self,w):
        """
        Constructor
        """
    

    def __len__(self):
        """
        >>> print len(Word(24))
        16
        """
 

    def lsb(self):
        """
        >>> Word(255).lsb()
        FF
        >>> Word(65535).lsb()
        FF
        """
       

    def msb(self):
        """
        >>> Word(255).msb()
        00
        >>> Word(65535).msb()
        FF
        """
       
