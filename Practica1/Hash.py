import hashlib

# Ejercicio 5
# inciso a
resumen_hash = "21232f297a57a5a743894a0e4a801fc3"
longitud = len(resumen_hash)
hash_md5 = hashlib.md5(b"admin").hexdigest()
if hash_md5 == resumen_hash:
    print("La cadena 'admin' coincide con el hash dado.")
    print("Longitud del hash:", longitud)
print("Hash MD5:", hash_md5)

# inciso b
resumen_hash = "e731a7b612ab389fcb7f973c452f33df3eb69c99"
print("Longitud del hash:", len(resumen_hash))
hash_sha1 = hashlib.sha1(b"p4ssw0rd").hexdigest()
if hash_sha1 == resumen_hash:
    print("La cadena 'p4ssw0rd' coincide con el hash dado.")
    print("Longitud del hash:", len(resumen_hash))
print("Hash SHA-1:", hash_sha1)

# inciso c
resumen_hash = "796DD619207C4E357FD432FDF962C958BA1DF4CD6785246937223BC8DC4FBF01794EBFF0" \
"159A175D9BE65B8EA4E7F46B80CCFFA4ED2A21773D358C523DDDD382"
print("Longitud del hash:", len(resumen_hash))
hash_sha512 = hashlib.sha512(b"!!!gotosleep!!!").hexdigest().upper()
if hash_sha512 == resumen_hash:
    print("La cadena '!!!gotosleep!!!' coincide con el hash dado.")
    print("Longitud del hash:", len(resumen_hash))
print("Hash SHA-512:", hash_sha512)

#ejercicio 6
from pwn import *
HOST = "ic.catedras.linti.unlp.edu.ar"
PORT = 11006
con = remote(HOST, PORT)
con.recvuntil(b"siguiente palabra:\n")
palabra = con.recvline().strip().decode()
print("Palabra recibida:", palabra)
hash = hashlib.md5(palabra.encode()).hexdigest()
con.sendline(hash.encode())
print("Respuesta ",con.recvall().decode())

#ejercicio 7

from pwn import *
import os 
archivo_path = os.path.join(os.getcwd(), "Practica1/rockyou.txt")

archivo = open(archivo_path, "r", encoding="utf-8")

    
HOST = "ic.catedras.linti.unlp.edu.ar"
PORT = 11007
con = remote(HOST, PORT)
con.recvuntil(b"rockyou.txt):\n")
palabra_hash = con.recvline().strip().decode()
print("Hash recibido:", palabra_hash)
cant =0
for linea in archivo:
    palabra = linea.strip()
    hash = hashlib.sha256(palabra.encode()).hexdigest()
    cant +=1
    print("Intentando con:",palabra)
    if hash == palabra_hash:
        con.sendline(palabra.encode())
        print("Palabra encontrada:", palabra)
        
        break
    if cant == 100:
        print("No se encontró la palabra en las primeras 100 líneas.")
        break
print("Respuesta ",con.recvall().decode())
archivo.close()


