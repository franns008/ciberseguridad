# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: script.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2025-11-12 11:14:50 UTC (1762946090)

import time
import binascii
from Crypto.Cipher import AES
y = 's4Pd'
z = '0w5' + y + 'r'
def get_passwd():
    return input('Password: ')

def check(s):
    z = '0w5' + y + 'r'
    x = (s[6:8] + s[0:3] + s[3:6])[::-1]
    return x == z

def get_secret(k):
    secret = binascii.unhexlify('f92d0786425761806008f985a2fcc4a1f04e142b6b7dadd0998083c35135dc21')
    key = (k * 2).encode('utf-8')
    iv = b'thisIsNotTheFlag'
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(secret)
s = get_passwd()
if check(s):
    print(get_secret(s))
else:
    time.sleep(5)
    print('Invalid password!')