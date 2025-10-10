from pwn import *
import codecs

print ("ejercicio 11")
con = remote("ic.catedras.linti.unlp.edu.ar", 11015)
con.recvuntil(b"es:\n")
pista = con.recvline().strip()          # b'reptil' por ejemplo

# leer la línea con el hexstring (no usar recvall antes de leerla)
mensaje_hex = con.recvline().decode().strip()

# convertir hex a bytes
mensaje_ct = bytes.fromhex(mensaje_hex)

key_bytes = bytearray(4)
for i in range(len(pista)):
    key_bytes[i % 4]= mensaje_ct[i] ^ pista[i]
# descifrar todo
plaintext_bytes = bytes(mensaje_ct[i] ^ key_bytes[i % 4] for i in range(len(mensaje_ct)))
plaintext = plaintext_bytes.decode('latin1')  

con.sendline(plaintext.encode())
print(con.recvall().decode())


print(" ")
#RSA
print("RSA")
print("ejercicio 12")
#ejercicio 12
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

p = "1411681044962247700471424630708374925648758544093881877"
q = "1025477764739116170232001755962926569489838949121232767"
e = 65537
C = "24480032935390633635038225308868097264670696263978384433594823408502234840" \
"0763256559770095538177770365047075"
n = int(p) * int(q)
phi = (int(p)-1)*(int(q)-1)
d = pow(e, -1, phi) # inverso modular
C = int(C)
m = pow(C, d, n) #m se calcula como C^d mod n, siendo m el mensaje encriptado
print("m:", m)
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
print("m_bytes:", m_bytes)

#Creamos la clave privada RSA

#ejercicio 13
from pwn import *
print("ejercicio 13")
con = remote("ic.catedras.linti.unlp.edu.ar", 11012)
print(con.recvuntil(b"siguiente texto:\n").decode())
p = con.recvline().strip()
q = con.recvline().strip()
e = con.recvline().strip()
p = p.partition(b'=')[2].strip()    
q = q.partition(b'=')[2].strip()
e = e.partition(b'=')[2].strip()
n = int(p) * int(q)
phi = (int(p)-1)*(int(q)-1)
d = pow(int(e), -1, phi) # inverso modular
c = con.recvline().strip()
c = c.partition(b'=')[2].strip()
c = int(c)
m = pow(c, d, n) #m se calcula como C^d mod n, siendo m el mensaje encriptado
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big') # Convertir m a bytes
#Calcula cuántos bytes hacen falta para guardar m.
#Luego crea esos bytes en orden big-endian.
con.sendline(m_bytes)
print(con.recvall().decode())

print(" ")
#ejercicio 14 Saque el facto de factordb
print("ejercicio 14")
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

n = "1452449184624535635757449085988204487494222248509493899299759"
e = 65537
c = "1280743944712857143060627969938538851911171950125979945026152"
n = int(n)
p = "1153324775179431312178120797679"
q = n // int(p)
phi = (int(p)-1)*(int(q)-1)
d = pow(e, -1, phi) # inverso modular
c = int(c)
m = pow(c, d, n) #m se calcula como C^d mod n, siendo m el mensaje encriptado
m_bytes = m.to_bytes((m.bit_length() + 7) // 8,
                        'big') # Convertir m a bytes    
print(m_bytes.decode())

#ejercicio 15


from pwn import *
from factordb.factordb import FactorDB
import requests
import requests
print("ejercicio 15")

def get_factors_from_factordb(n):
    # usar http (la API pública documentada) y forzar User-Agent
    url = f"http://factordb.com/api?query={n}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
    r.raise_for_status()
    j = r.json()
    while j.get('status') != 'FF':
        # si está en cola, esperar y volver a consultar
        time.sleep(2)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        r.raise_for_status()
        j = r.json()

    print("Factordb response:", j)
    if 'factors' in j and j['factors']:
        factors = [int(pair[0]) for pair in j['factors']]
        # si la API sólo devuelve [n] -> no hay factorización directa
        if len(factors) == 1 and factors[0] == int(n):
            return None
        return factors
    return None


HOST = 'ic.catedras.linti.unlp.edu.ar'
PORT = 11017
con = remote(HOST, PORT)
con.recvuntil(b"n= ")
n = con.recvline().decode().strip() 
con.recvuntil(b"e= ")
e = con.recvline().decode().strip()
con.recvuntil(b"c= ")
c = con.recvline().decode().strip()
print("n:", n)
print("e:", e)
print("c:", c)
factors = get_factors_from_factordb(n)

p = factors[0]
q = factors[1]
phi = (p-1)*(q-1)
d = pow(int(e), -1, phi) # inverso modular
c = int(c)
m = pow(c, d, int(n)) #m se calcula como C^d mod
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big') # Convertir m a bytes
print("m_bytes:", m_bytes)
con.sendline(m_bytes)
print(con.recvall().decode())



#ejercicio 16
print("ejercicio 16")
from pwn import *
HOST = 'ic.catedras.linti.unlp.edu.ar'
PORT = 11018
con = remote(HOST, PORT)

con.recvuntil(b"p= ")
p = con.recvline().strip()
con.recvuntil(b"g=")
g = con.recvline().strip()
con.recvuntil(b"public_alice= ")
public_alice = con.recvline().strip()
con.recvuntil(b"private_bob= ")
private_bob = con.recvline().strip()
secret_bob = pow(int(public_alice), int(private_bob), int(p))
con.sendline(str(secret_bob).encode())
print(con.recvall().decode())

print("p:", p)
print("g:", g)
print("public_alice:", public_alice)
print("private_bob:", private_bob)