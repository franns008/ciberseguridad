from pwn import *
import codecs

con = remote("ic.catedras.linti.unlp.edu.ar", 11015)
print(con.recvuntil(b"palabra es:\n"))
primer_palabra = con.recvline().decode().strip()

#mensaje en hexadecimal
mensaje_encriptado = con.recvline().decode().strip()
cipher_bytes = codecs.decode(mensaje_encriptado, "hex")

primer_palabra = operator.xor(primer_palabra)


print(mensaje_encriptado)
print(primer_palabra)