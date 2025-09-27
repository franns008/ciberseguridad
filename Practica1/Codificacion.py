import base64
import unicodedata
from pwn import *
from PIL import PngImagePlugin, Image
import os
from pyzbar.pyzbar import decode

#ejercicio a
def desencriptar(mensaje):
    mensaje_desencriptado = mensaje.replace("73", "C").replace("67", "o")

mensaje_encriptado = "73 67 123 98 97 115 105 99 95 97 115 99 105 105 95 101 110 99 111 100 105 110 103 125"
print("Mensaje encriptado:", mensaje_encriptado)
mensaje_encriptado = mensaje_encriptado.split()
for i in range(len(mensaje_encriptado)):
    mensaje_encriptado[i] = chr(int(mensaje_encriptado[i]))
mensaje_desencriptado = ''.join(mensaje_encriptado)
print("Mensaje desencriptado:", mensaje_desencriptado)

#ejercicio b
mensaje_encriptado = "SUN7RW5jMGRlNHJfbjBfM3NfZW5DcjFwdDRyfQ=="

mensaje_desencriptado = base64.b64decode(mensaje_encriptado).decode('ascii')
print("Mensaje desencriptado: sin normalizar", mensaje_desencriptado)
print("Mensaje desencriptado: normalizado", mensaje_desencriptado.translate(str.maketrans({'0':'o', '3':'e', '4':'a'})))

#ejercicio c
mensaje = "9-14-20-18-15-4-21-3-3-9-15-14 1 12-1 3-9-2-5-18-19-5-7-21-18-9-4-1-4"

resultado = []
# separo por espacios (palabras)
for palabra in mensaje.split(" "):
    # separo cada palabra en números por el "-"
    letras = palabra.split("-")
    # convierto cada número a letra
    palabra_descifrada = "".join(chr(int(num) + 96) for num in letras if num.isdigit())
    resultado.append(palabra_descifrada)

mensaje_desencriptado = " ".join(resultado)

print("Mensaje desencriptado:", mensaje_desencriptado)

#EJERCICIO d

mensaje_encriptado = "05110006_08130308020418_001115070001041908021418"
palabras = []
for bloque in mensaje_encriptado.split('_'):  # separa por palabras
    letras = []
    for i in range(0, len(bloque), 2):        # pares de 2 dígitos
        num = bloque[i:i+2]
        if not num.isdigit():
            continue
        n = int(num)
        if 0 <= n <= 26:
            letters_char = chr(n + 97)       # fuera de rango, marca
        letras.append(letters_char)
    palabras.append(''.join(letras))

mensaje_desencriptado = '_'.join(palabras)
print("Mensaje desencriptado:", mensaje_desencriptado)

#ejercicio e
mensaje_encriptado = "49 43 7b 68 65 78 5f 65 6e 63 30 64 31 6e 47 5f 73 74 49 6c 4c 5f 65 34 7a 79 7d"
mensaje_encriptado = mensaje_encriptado.split()
for i in range(len(mensaje_encriptado)):
    mensaje_encriptado[i] = chr(int(mensaje_encriptado[i], 16))
mensaje_desencriptado = ''.join(mensaje_encriptado)

print("Mensaje desencriptado:", mensaje_desencriptado)

#ejercicio f
def braille_to_text(s: str) -> str:
    map_mask_to_char = {
        0: ' ',   
        1: 'a', 3: 'b', 9: 'c', 25: 'd', 17: 'e', 11: 'f', 27: 'g', 19: 'h', 10: 'i', 26: 'j',
        5: 'k', 7: 'l', 13: 'm', 29: 'n', 21: 'o', 15: 'p', 31: 'q', 23: 'r', 14: 's', 30: 't',
        37: 'u', 39: 'v', 58: 'w', 45: 'x', 61: 'y', 53: 'z',
    
    }
    out = []
    for ch in s:
        if '\u2800' <= ch <= '\u28ff':
            mask = ord(ch) - 0x2800
            out.append(map_mask_to_char.get(mask, '?'))
        else:
            out.append(ch)
    return ''.join(out)


mensaje_encriptado  = "⠁⠧⠁⠙⠁⠀⠅⠑⠙⠁⠧⠗⠁"
print("Texto en Braille:", mensaje_encriptado)
print("Texto desencriptado:", braille_to_text(mensaje_encriptado))

#ejercicio g

import re

image_path = os.path.join(os.getcwd(), "Practica1/merged_image.jpg")

with open(image_path, "rb") as f:
    data = f.read()

m = re.search(rb'IC\{[^}\r\n]{1,200}\}', data)
if m:
    flag = m.group(0).decode("utf-8", errors="ignore")
    print(flag)
#ejercicio 2

conect = remote("ic.catedras.linti.unlp.edu.ar", 11002)
conect.recvuntil(b'esta palabra:\n')
palabra = conect.recvline()
palabra = palabra.replace(b'\n', b'')
print(palabra)
palabraBase64 = base64.b64encode(palabra).decode()

conect.sendline(palabraBase64.encode())
print(conect.recvall().decode())