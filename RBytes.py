def int_byte(number:int):   
    return bytes((number,))


class RBytes:
    '''Fixed length of bytes'''
    def __init__(self,array:bytes):
        self._bytes = array

    def __getitem__(self,item):
        return self._bytes[item]

    def __invert__(self):
        to_return = b''
        for i in range(len(self._bytes)):
            to_return += int_byte(self._bytes[i] ^ 0b11111111)
        return RBytes(to_return)

    def __bool__(self):
        to_return = False
        for i in range(len(self._bytes)):
            if self._bytes[i] != 0:
                to_return = True
                break
        return to_return

    def __len__(self):
        return len(self._bytes)

    def __rshift__(self,shift):
        if shift<0:
            raise ValueError('negative shift count')
        if shift == 0:
            return self

        to_return = b''
        buf = 0
        if shift>8:
            orig_shift = shift
            shift = 8
            to_return = RBytes(self._bytes)
            for n in range(orig_shift//shift):
                to_return = to_return>>8
            
            if orig_shift > (orig_shift//shift)*8:
                shift = orig_shift - (orig_shift//shift)*8
                to_return = to_return>>shift
            return to_return
        else:
            buf = 0
            for i in range(len(self._bytes)):
                to_return += int_byte((self._bytes[i]>>shift)+buf)
                buf = (self._bytes[i]&((0b11111111>>(8-shift))))<<(8-shift)
        
        return RBytes(to_return)

    def __lshift__(self,shift):
        if shift<0:
            raise ValueError('negative shift count')
        if shift == 0:
            return self

        to_return = b''
        buf = 0

        if shift>8:
            orig_shift = shift
            shift = 8
            to_return = RBytes(self._bytes)
            for n in range(orig_shift//shift):
                to_return = to_return<<8
            
            if orig_shift > (orig_shift//shift)*8:
                shift = orig_shift - (orig_shift//shift)*8
                to_return = to_return<<shift
            return to_return
        else:
            buf = 0
            for i in range(len(self._bytes)-1,-1,-1):
                to_return = int_byte(((self[i]&(0b11111111>>shift))<<shift)+buf) + to_return            
                buf = (self[i]&((0b11111111>>(8-shift))<<(8-shift)))>>(8-shift)               

        return RBytes(to_return)

    def unsized_lshift(self,shift):
        if shift<0:
            raise ValueError('negative shift count')
        if shift == 0:
            return self
        to_return = b''
        if shift>8:
            orig_shift = shift
            shift = 8
            to_return = RBytes(self._bytes)
            for n in range(orig_shift//shift):
                to_return = to_return.unsized_lshift(8)               
            
            if orig_shift > (orig_shift//shift)*8:
                shift = orig_shift - (orig_shift//shift)*8
                to_return = to_return.unsized_lshift(shift)
            return to_return
        else:
            buf = 0
            for i in range(len(self._bytes)-1,-1,-1):
                to_return = int_byte(((self._bytes[i]&(0b11111111>>shift))<<shift)+buf) + to_return            
                buf = (self._bytes[i]&((0b11111111>>(8-shift))<<(8-shift)))>>(8-shift) 
               
            if buf != 0:
                to_return = int_byte(buf) + to_return

        return RBytes(to_return)


    def __add__(a,b):
        if type(a) != RBytes or type(b)!= RBytes:
            raise TypeError('Unsupported types of operands')
        to_return = b''
        
        if len(b)>len(a):
            buf = a
            a = b
            b = buf
        
        buf = b'\x00'*(len(a)-len(b)) + b._bytes
        
        b = RBytes(buf)

        buf = 0

        for i in range(len(a)-1,-1,-1):
            to_return = int_byte((a[i]+b[i]+buf)&0b11111111) + to_return
            buf = (a[i]+b[i]+buf)>>8

        return RBytes(to_return)

    def __and__(a,b):
        if type(a) != RBytes or type(b)!= RBytes:
            raise TypeError('Unsupported types of operands')
        to_return = b''
        
        if len(b)>len(a):
            buf = a
            a = b
            b = buf

        buf = b'\x00'*(len(a)-len(b)) + b._bytes
        b = RBytes(buf)

        for i in range(len(a)-1,-1,-1):
            to_return = int_byte(a[i] & b[i]) + to_return

        return RBytes(to_return)


    def __or__(a,b):
        if type(a) != RBytes or type(b)!= RBytes:
            raise TypeError('Unsupported types of operands')
        to_return = b''
        
        if len(b)>len(a):
            buf = a
            a = b
            b = buf

        buf = b'\x00'*(len(a)-len(b)) + b._bytes
        b = RBytes(buf)

        for i in range(len(a)-1,-1,-1):
            to_return = int_byte(a[i] | b[i]) + to_return

        return RBytes(to_return)

    def __xor__(a,b):
        
        if type(a) != RBytes or type(b)!= RBytes:
            raise TypeError('Unsupported types of operands')
        to_return = b''
        
        if len(b)>len(a):
            buf = a
            a = b
            b = buf

        buf = b'\x00'*(len(a)-len(b)) + b._bytes
        b = RBytes(buf)

        for i in range(len(a)-1,-1,-1):
            to_return = int_byte(a[i] ^ b[i]) + to_return

        return RBytes(to_return)

    def __eq__(a,b):
        if type(a) != RBytes or type(b)!= RBytes:
            raise TypeError('Unsupported types of operands')
        
        
        if len(b)>len(a):
            buf = a
            a = b
            b = buf

        buf = b'\x00'*(len(a)-len(b)) + b._bytes
        b = RBytes(buf)

        eq = True

        for i in range(len(a)-1,-1,-1):
            if a[i] != b[i]:
                eq = False
                break


        return eq

    def __bytes__(self):
        return self._bytes



    
#import time

if __name__ == '__main__':
    
    

    bts = RBytes(b'\x40\x69\xe4\xf2\x01\x11\xff\x52')
    data = bts >> 32
    
    print(bytes(bts))
    #beg = time.time()
    check = bts<<40
    u = bts == bts1
    #delta = time.time()-beg
    bts1 = RBytes(b'\x01')
    new = bts + bts1
    
    print(bool(bts))
    data = ~bts
    print(data)
    data = data >> 1
    data = data.unsized_lshift(2)
    #data = data << 2

    if data:
        print(bool(data))
    
