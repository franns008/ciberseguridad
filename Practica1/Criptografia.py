import re

#Ejercicio 03 
#incisio a
mensaje_cifrado = "}ratnelac_a_odnazepmE{CI"
mensaje_descifrado = mensaje_cifrado[::-1]
print("Mensaje descifrado inciso a:", mensaje_descifrado)
#se uso cifrado de tansposicion. Se invierte el mensaje.
#inciso b
mensaje_cifrado = "LF{HVWr VH hpSlhcd d FrpsolfdU}"
mensaje_descifrado = ""
for letra in mensaje_cifrado:
    if letra not in ("{", "}", " "):
        mensaje_descifrado += chr(ord(letra)-3) if ord(letra)-3 >= ord('A') else chr(ord(letra)-3+26)
    else:
        mensaje_descifrado += letra
print("Mensaje descifrado inciso b:", mensaje_descifrado)
#se uso cifrado cesar con corrimiento de 3, es de transposicion
#inciso c
mensaje_cifrado = "QK{IPWZI CV XWKW UIA}"
cantidad_corrimiento =  ord('Q') - ord('I')
mensaje_descifrado = ""
for letra in mensaje_cifrado:   
    if letra not in ("{", "}", " "):
        mensaje_descifrado += chr(ord(letra)-cantidad_corrimiento) if ord(letra)-cantidad_corrimiento >= ord('A') else chr(ord(letra)-cantidad_corrimiento+26)
    else:
        mensaje_descifrado += letra
print("Mensaje descifrado inciso c:", mensaje_descifrado)
#se uso cifrado cesar con corrimiento de 2, es de transposicion

#inciso d
from itertools import cycle

cipher = "pp epnwfus dvjipèym jx ln dtjcefv jfxrhw rq hkmmwjetfd wpvkla ij teznfxgymx t ceuced hgs knkielb féwcy ntwdaoos pwvva hfiekghvgz csf kacwe, wpctiif kejyd hg cqljeèrf, byp wg baf hfqw poexl. mq hzfslhz hg cqljeèvm rv yp jqkwrdp oi dyuaqyztmóv flqrsm utcibwjlfévpkt. rlc jvhr! nh nqfx et tg{g1k3plz3_wzc3w} . arjyí czí!"
clave = "le chiffre indechiffrable".lower()

abc = "abcdefghijklmnopqrstuvwxyz"
def vigenere_decrypt(text, key):
    out = []
    key_iter = cycle(key)
    for c in text:
        if c.lower() in abc:
            k = next(key_iter)
            while k not in abc:  # saltar espacios u otros caracteres de la clave
                k = next(key_iter)
            p = (abc.index(c.lower()) - abc.index(k)) % 26
            out.append(abc[p] if c.islower() else abc[p].upper())
        else:
            out.append(c)
    return "".join(out)

print(vigenere_decrypt(cipher, clave))

#Se uso cifrado vigenere con clave "le chiffre indechiffrable", es de tipo polialfabetico

#inciso e

mensaje_cifrado = "CROITSFRIRACANIPSOOPN"
cols, rows = 7, 3
mensaje_descifrado = ""
# cortar el cifrado en columnas (cada columna tiene 'rows' letras)

columns = [mensaje_cifrado[i*rows:(i+1)*rows] for i in range(cols)]

# reconstruir filas tomando el r-ésimo char de cada columna
rows_str = [''.join(col[r] for col in columns) for r in range(rows)]

plaintext = ''.join(rows_str)
print("Mensaje descifrado inciso e:", plaintext)
#transposicion, se usa cifrado por transposicion de columnas


#inciso f
mensaje_cifrado = "TSaeile nh umrnrwl ev tnoebi laao"
mensaje_descifrado = " "
mensaje_cifrado = mensaje_cifrado.split()
def rail_fence_decrypt(ciphertext, rails):
    n = len(ciphertext)

    # patrón zigzag: a qué riel va cada carácter
    pattern = []
    rail, direction = 0, 1
    for _ in range(n):
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # contar cuántos caracteres tocan en cada riel
    counts = [pattern.count(r) for r in range(rails)]

    # cortar ciphertext en pedazos según esos counts
    rails_content = []
    idx = 0
    for c in counts:
        rails_content.append(list(ciphertext[idx:idx+c]))
        idx += c

    # reconstruir siguiendo el zigzag
    pos = [0]*rails
    result = []
    for r in pattern:
        result.append(rails_content[r][pos[r]])
        pos[r] += 1

    return ''.join(result)


# --- Uso ---
mensaje_cifrado = "TSaeile nh umrnrwl ev tnoebi laao"
print("Mensaje descifrado inciso f:", rail_fence_decrypt(mensaje_cifrado, 3))
#se usa rail fence con 3 rieles, es de transposicion

#Ejercicio 04
from pwn import *
HOST = "ic.catedras.linti.unlp.edu.ar"
PORT = 11004

con = connect(HOST, PORT)


desplazamiento = con.recvuntil(b"de esta").strip()
desplazamiento = int(re.search(rb'ROT (\d+)',desplazamiento).group(1))
con.recvuntil(b"frase:\n")
mensaje_cifrado = con.recvline()
mensaje_cifrado = mensaje_cifrado.decode().strip()
print("mensaje cifrado:", mensaje_cifrado)
mensaje_descifrado = ""
for letra in mensaje_cifrado:
    if letra.isalpha():  # solo letras
        base = ord('A') if letra.isupper() else ord('a')
        # desplazamiento circular con módulo
        mensaje_descifrado += chr((ord(letra) - base - desplazamiento) % 26 + base)
    else:
        mensaje_descifrado += letra
con.sendline(mensaje_descifrado)
print("respuesta enviada:",con.recvall().decode())
