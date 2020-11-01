# RBytes
"Real" bytes in python, because standart bytes() doesn't work properly

I wrote that because bytes() in python doesn't allow to do bit shiftings and other bitwise operations

# Installation
pip install RBytes

# Some Examples

```python
from RBytes import RBytes

byte_array = RBytes(b'\x01\x01\x01\x01')

result = byte_array << 5 #bitwise left shift

```

```python
from RBytes import RBytes
import struct

converted_int = struct.pack('i',69) #get 4 bytes

byte_array = RBytes(converted_int) #get 'real' bytes

result = byte_array << 5 #bitwise left shift

```
