
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=================
Modul Instruction
=================

En el simulador, cada instruccio del microcontrolador te associada una classe. Per exemple, la
instruccio ADD te associada la classe Add. Una instancia de la classe Add es capac de reconeixer
i simular qualsevol instruccio ADD.

La classe InstRunner es la super-classe (abstracta) de totes les classes lligades a instruccions.
Concentra els (pocs) serveis comuns que aquestes classes lligades a instruccio tenen.

"""

from bitvec import*
from memory import*
from state import*
from avrexcept import*

class BreakException(AVRException):
    """
    Es llensa cada cop que s'executa la instruccio BRK. S'usa per aturar la simulacio.
    """
    pass


class InstRunner(object):
    """
    Es la superclasse de totes les classes lligades a instruccions.
    """
    def __repr__(self):
        """
        Retorna una cadena que representa la instruccio.
        """
        tip=str(type(self))
        tip=tip.split('.')
        nom=tip[1][0:(tip[1].index("'"))]
  
class Add(InstRunner):
    """
    Suma normal, registre-registre.
    """
    def match(self,instr):
        """
        Mirar si va lligat amb trace
        """
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='000011':
            return True
        else:
            return False

    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        resultat=op1+op2
        state.data[rd]=resultat
        state.pc+=1
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0

class Adc(InstRunner):
    """
    Suma amb carry, registre-registre.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='000111':
            return True
        else:
            return False
    
    def execute(self,instr,state):
        """
       
        """
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        op1=str(0)+"{0:0b}".format(op1.getW())+str(state.flags['CARRY'])
        op2=str(0)+"{0:0b}".format(op2.getW())+str(1)
        resultat=bin(int(op1,2)+int(op2,2))#[2:]
        resultat=resultat[:-1]
        state.flags['CARRY']= (int(resultat,2)&256)>>8
        state.data[rd]=Byte(int(resultat,2))
        state.pc+=1
        if resultat==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0

class Sub(InstRunner):
    """
    Resta sense carry, registre-registre.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='000110':
            return True
        else:
            return False

    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        resultat=op1-op2
        state.data[rd]=resultat
        state.pc+=1
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0

class Subi(InstRunner):
    """
    Resta sense carry, registre-constant.
    Suposem que la constant esta en forma de nombre binari al ocupant el lloc del nom del segon registre.
    """
    
    def match(self,instr):
        opcode="{0:04b}".format(int(instr.extract_field_u(0b1111000000000000),2))
        if opcode=='0101':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000011110000),2)
        k=Byte(int(instr.extract_field_u(0b0000111100001111),2))
        op1=state.data[rd]
        resultat=op1-k.getW()
        state.data[rd]=resultat
        state.pc+=1
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0
    
class And(InstRunner):
    """
    And registre-registre.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='001000':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        resultat=op1&op2
        state.data[rd]=resultat
        state.pc+=1
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0

class Or(InstRunner):
    """
    Or registre-registre.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='001010':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        resultat=op1|op2
        state.data[rd]=resultat
        state.pc+=1
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0


class Eor(InstRunner):
    """
    Or exclusiva registre-registre.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='001001':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        resultat=op1^op2
        state.data[rd]=resultat
        state.pc+=1
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0


class Lsr(InstRunner):
    """
    Desplacament dreta registre.
    """
    def match(self,instr):
        opcode="{0:011b}".format(int(instr.extract_field_u(0b1111111000001111),2))
        if opcode=='10010100110':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        r=int(instr.extract_field_u(0b0000000111110000),2)
        op=state.data[r]
        resultat=op>>1
        state.data[r]=resultat
        state.pc+=1
        if op[0]:
            state.flags['CARRY']=1
        else:
            state.flags['CARRY']=0
        if resultat.getW()==Byte(0):
            state.flags['ZERO']=1
        else:
            state.flags['ZERO']=0


class Mov(InstRunner):
    """
    Copia registre-registre.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='001011':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        rd=int(instr.extract_field_u(0b0000000111110000),2)
        rr=int(instr.extract_field_u(0b0000001000001111),2)
        op1,op2=state.data[rd],state.data[rr]
        state.data[rd]=op2
        state.pc+=1


class Ldi(InstRunner):
    """
    Assigna valor a registre.
    """
    def match(self,instr):
        opcode="{0:04b}".format(int(instr.extract_field_u(0b1111000000000000),2))
        if opcode=='1110':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        r=int(instr.extract_field_u(0b0000000011110000),2)
        v=Byte(int(instr.extract_field_u(0b0000111100001111),2))
        state.data[r]=v
        state.pc+=1

class Sts(InstRunner):
    """        
    Copia registre a memoria.ACABAR
    """
    def match(self,instr):
        opcode="{0:011b}".format(int(instr.extract_field_u(0b1111111000001111),2))
        if opcode=='10010010000':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        """
        Falta acabar.
        Com s'ha d'escriure el contingut del registre al port extern??
        """
        r=int(instr.extract_field_u(0b0000000111110000),2)
        k=instr.getW()
        m=Byte(26)
        state.data[m]=state.data[r]
        state.pc+=2


class Lds(InstRunner):
    """
    Copia memoria a registre. ACABAR
    """
    def match(self,instr):
        opcode="{0:011b}".format(int(instr.extract_field_u(0b1111111000001111),2))
        if opcode=='10010000000':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        r=int(instr.extract_field_u(0b0000000111110000),2)
        k=instr.getW()
        m1=Byte(26)
        m1=state.data[m1]
        m2=Byte(27)
        m2=state.data[m2]
        m=m2.concat(m1)
        state.data[r]=m
        state.pc+=2

class Rjmp(InstRunner):
    """
    Salt relatiu a una nova instruccio.
    """
    def match(self,instr):
        opcode="{0:04b}".format(int(instr.extract_field_u(0b1111000000000000),2))
        if opcode=='1100':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        k=int(instr.extract_field_u(0b0000111111111111),2)+1
        state.pc+=k
        

class Brbs(InstRunner):
    """
    Salta a adreca de programa si cert bit de FLAGS es 1.
    Farem un BREQ, es a dir, suposarem s=001, i mirarem el flag Z.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='111100':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        k=int(instr.extract_field_u(0b0000001111111000),2)
        if state.flags['ZERO']==1:
            state.pc+=k
        state.pc+=1

class Brbc(InstRunner):
    """
    Salta a adreca de programa si cert bit de FLAGS es 0.
    Farem un BRNE, es a dir, suposarem s=001, i mirarem el flag Z.
    """
    def match(self,instr):
        opcode="{0:06b}".format(int(instr.extract_field_u(0b1111110000000000),2))
        if opcode=='111101':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        k=int(instr.extract_field_u(0b0000001111111000),2)
        if state.flags['ZERO']==0:
            state.pc+=k
        state.pc+=1

class Nop(InstRunner):
    """
    No fa res, instruccio nula.
    """
    def match(self,instr):
        if instr.getW()==0:
            return True
        else:
            return False
        
    def execute(self,instr,state):
        state.pc+=1

class In(InstRunner):
    """
    Quan s'aplica al port 0x0, llegeix un caracter del teclat.
    """
    def match(self,instr):
        opcode="{0:05b}".format(int(instr.extract_field_u(0b1111100000000000),2))
        if opcode=='10110':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        r=int(instr.extract_field_u(0b0000000111110000),2)
        a=int(instr.extract_field_u(0b0000011000001111),2)
        if a==0:
            c=raw_input("Escriu caracter: ")
            state.data[r]=Byte(c)
            state.pc+=1

class Out(InstRunner):
    """
    Escriura per pantalla:
    si el port es 0x0, el valor del registre corresponent en base 10
    si el port es 0x1, el valor del registre corresponent en base 16
    si el port es 0x2, el valor del registre assumint que correspon a la codificacio UTF d'un caracter
    """
    def match(self,instr):
        opcode="{0:05b}".format(int(instr.extract_field_u(0b1111100000000000),2))
        if opcode=='10111':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        """
        Falta acabar.
        """
        if self.match(instr):
            r=int(instr.extract_field_u(0b0000000111110000),2)
            op=state.data[r]
            a=int(instr.extract_field_u(0b0000011000001111),2)
            if a==0:
                print op.getW()
            if a==1:
                print op
            if a==2:
                pass

            state.pc+=1

class Break(InstRunner):
    """
    llenca l'excepcio
    """
    def match(self,instr):
        opcode="{0:016b}".format(int(instr.extract_field_u(0b1111111111111111),2))
        if opcode=='1001010110011000':
            return True
        else:
            return False
        
    def execute(self,instr,state):
        raise BreakException
    

if __name__ == '__main__':
    st=State(32,32)
    Ldi().execute(Word(0b1110111100001111),st) 
    Ldi().execute(Word(0b1110000000010001),st)
     
    print st.dump_reg()
  
    
    a=Word(0b0000111001110001)
    b=Brbc()
    print b.match(a)
    st=State(1,1)
    Nop().execute(Word(0b0000000000000000),st)
    Ldi().execute(Word(0b1110000000100101),st) #assignem el valor 5 al registre 2
    Ldi().execute(Word(0b1110000000110001),st) #assignem el valor 1 al registre 3
    print 1
    print st.dump_reg()
    Add().execute(Word(0b0000110000100011),st) #fem la suma normal i guardem el resultat al registre 2
    print 2
    print st.dump_reg()
    Sub().execute(Word(0b0001100000100011),st) #restem el valor del registre 2 menys el del registre 3, guardem al reg 3
    print 3
    print st.dump_reg()
    Subi().execute(Word(0b0101000000100010),st) #restem 2 al reg 2
    print 4
    print st.dump_reg()
    And().execute(Word(0b0010000000100011),st) #fem una and, guardem al reg 2
    print 5
    print st.dump_reg()
    Or().execute(Word(0b0010100000100011),st) #fem una or, guardem al reg 2
    print 6
    print st.dump_reg()
    Eor().execute(Word(0b0010010000100011),st) #fem una exor, guardem al reg 2
    print 7
    print st.dump_reg()
    Ldi().execute(Word(0b1110000001001011),st) #assignem el valor 11 al registre 4
    print 8
    print st.dump_reg()
    Lsr().execute(Word(0b1001010001000110),st) #desplacem el valor del registre 4 cap a dreta
    print 9
    print st.dump_reg()
    Mov().execute(Word(0b0010110001010100),st) #copiem el contingut del reg4 al reg5
    print 10
    print st.dump_reg()
    Lds().execute(Word(0b1001000001010000),st) #nose si acava de funcionar be...
    print 11
    print st.dump_reg()
    Rjmp().execute(Word(0b1100000000000011),st) #fa un salt augmentant el comptador +3(+1)
    print 12
    print st.dump_reg()
    Brbs().execute(Word(0b1111000000110001),st) #si el flag z es 1 fa un salt de +6(+1) sino nomes +1
    print 13
    print st.dump_reg()
    Brbc().execute(Word(0b1111010000100001),st) #si el flag z es 0 fa un salt de +4(+1) sino nomes +1
    print 14
    print st.dump_reg()
    #In().execute(Word(0b1011000001100000),st) #escriu el caracter que demana al registre 6
    print 15
    print st.dump_reg()
    Out().execute(Word(0b1011100001000000),st) #printa en base 10 el valor del registre 4
    Out().execute(Word(0b1011100001100001),st) #printa en base 16 el valor del registre 6
    Out().execute(Word(0b1011100001100010),st) #printa en codi utf el valor del registre 6
    Adc().execute(Word(0b0001110001000110),st) #suma amb carry del registre 4 i 6
    print 16
    print st.dump_reg()
    Sts().execute(Word(0b1001001001000000),st) #copia a la memoria externa X, el contingut de reg4
    print 17
    #print st.dump_reg()
    #Lds().execute(Word(0b1001000010000000),st) #copia al reg7, el continfut de la memoria externa X
    #print st.dump_reg()
    Break().execute(Word(0b1001010110011000),st) #atura
   
   
