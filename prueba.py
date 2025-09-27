from pwn import *

# Script para resolver múltiples operaciones aritméticas hasta obtener la flag.
# Ajusta context.log_level = 'debug' si querés ver el tráfico completo.
context.log_level = 'info'

HOST = "163.10.20.26"
PORT = 10002


def es_expr(line: str) -> bool:
    try:
        parts = line.strip().split()
        if len(parts) < 3:
            return False
        int(parts[0]); int(parts[2])
        return parts[1] in ['+','-','*']
    except Exception:
        return False


def resolver(parts):
    a = int(parts[0]); op = parts[1]; b = int(parts[2])
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    raise ValueError(f"Operador no soportado: {op}")


def main():
    r = remote(HOST, PORT)
    operaciones = 0
    while True:
        try:
            line = r.recvline(timeout=3)
        except EOFError:
            print("[!] El servidor cerró la conexión (EOF).")
            break
        if not line:
            print("[!] Fin de datos (línea vacía).")
            break
        txt = line.decode(errors='ignore').strip()
        print(f"[SERVIDOR] {txt}")
        low = txt.lower()
        if 'flag' in low and ('{' in txt or 'ctf' in low):
            print("[FLAG]", txt)
            break
        if es_expr(txt):
            parts = txt.split()
            try:
                res = resolver(parts)
            except Exception as e:
                print(f"[!] Error resolviendo expresión: {e}")
                break
            operaciones += 1
            print(f"[ENVÍO #{operaciones}] {res}")
            r.sendline(str(res).encode())
    r.close()
    print(f"[+] Total operaciones resueltas: {operaciones}")


if __name__ == '__main__':
    main()

# Notas:
# - Se eliminó recvall() para no consumir líneas futuras.
# - Se procesa cada línea en orden; si es expresión se responde.
# - Cuando aparece algo que parece la flag se corta el loop.
# - Aumenta context.log_level a 'debug' si necesitás más traza.