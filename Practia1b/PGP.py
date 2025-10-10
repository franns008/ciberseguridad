# crack_with_subprocess.py
#ejercicio 19
print("ejercicio 19")

import subprocess
from pathlib import Path
import os
''' --- IGNORE ---
GPG_PATH = r"C:\Program Files (x86)\GnuPG\bin\gpg.exe"  # ajustá si es necesario
DICT_PATH = os.path.join(os.getcwd(), "Practia1b", "diccionario")  # ajustá si es necesario
ENC_PATH  = os.path.join(os.getcwd(), "Practia1b", "flag.txt.gpg")

with open(DICT_PATH, "r", encoding="utf-8", errors="ignore") as dic:
    for i, line in enumerate(dic, 1):
        p = line.strip()
        if not p:
            continue
        if i % 500 == 0:
            print(f"Probadas {i} passphrases... ultima: {p}")
        try:
            proc = subprocess.run(
                [GPG_PATH, "--batch", "--yes", "--passphrase", p, "-d", str(ENC_PATH)],
                capture_output=True, text=True, timeout=5
            )
        except Exception as e:
            print("Error ejecutando gpg:", e)
            continue
        if proc.returncode == 0 and proc.stdout:
            print("✅ Passphrase encontrada:", p)
            print("----- contenido -----")
            print(proc.stdout)
            break
    else:
        print("No se encontró la passphrase en el diccionario.")
'''

#ejercicio 20
# ejercicio 20 con subprocess
import subprocess
import os
from pwn import *

print("Ejercicio 20 — cifrado con subprocess")

# Ejercicio 20 - versión final con confianza y subprocess
print("Ejercicio 20 — cifrado con subprocess (versión final)")

import subprocess
import os
from pwn import *

# === RUTAS ===
BASE_DIR = os.path.join(os.getcwd(), "Practia1b")
GPG_PATH = r"C:\Program Files (x86)\GnuPG\bin\gpg.exe"
PUBLIC_KEY = os.path.join(BASE_DIR, "public.gpg")
INPUT_FILE = os.path.join(BASE_DIR, "encriptar.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "encriptar.txt.asc")

# === IMPORTAR LA CLAVE PÚBLICA ===
print("[*] Importando clave pública...")
subprocess.run(
    [GPG_PATH, "--batch", "--yes", "--import", PUBLIC_KEY],
    capture_output=True, text=True
)

# === OBTENER EL FINGERPRINT ===
result = subprocess.run(
    [GPG_PATH, "--list-keys", "--with-colons"],
    capture_output=True, text=True
)
fingerprint = None
for line in result.stdout.splitlines():
    if line.startswith("fpr:"):
        fingerprint = line.split(":")[9]
        break

if not fingerprint:
    print("❌ No se encontró fingerprint de la clave.")
    exit(1)

print(f"[+] Fingerprint detectado: {fingerprint}")

# === ESTABLECER CONFIANZA TOTAL EN LA CLAVE ===
print("[*] Marcando la clave como confiable...")
trust_input = f"{fingerprint}:6:\n"  # 6 = ultimate trust
subprocess.run(
    [GPG_PATH, "--import-ownertrust"],
    input=trust_input,
    text=True,
    capture_output=True
)

# === CIFRAR EL ARCHIVO ===
print("[*] Cifrando archivo...")
encrypt_cmd = [
    GPG_PATH,
    "--batch", "--yes",
    "--output", OUTPUT_FILE,
    "--armor", "--encrypt",
    "--recipient", fingerprint,
    INPUT_FILE
]
encrypt_result = subprocess.run(encrypt_cmd, capture_output=True, text=True)

if encrypt_result.returncode != 0:
    print("❌ Error al cifrar el archivo:")
    print(encrypt_result.stderr)
    exit(1)

print(f"[+] Archivo cifrado correctamente -> {OUTPUT_FILE}")

# === MOSTRAR LAS PRIMERAS LÍNEAS DEL ARCHIVO CIFRADO ===
print("\nContenido cifrado (primeras líneas):")
with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for _ in range(5):
        print(f.readline().strip())

HOST = "ic.catedras.linti.unlp.edu.ar"
PORT = 12003
print("\n[*] Conectando al servidor...")

con = remote(HOST, PORT)
print(con.recv(timeout=0.7).decode(errors="ignore"))

with open(OUTPUT_FILE, "rb") as f:
    con.send(f.read())

con.shutdown("send")
print("[*] Respuesta del servidor:")
print(con.recvall(timeout=5).decode(errors="ignore"))

