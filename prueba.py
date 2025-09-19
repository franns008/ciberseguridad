from pwn import *
# Para debug del socket utilizamos:
# context.log_level = 'debug'
# Analice las diferencias entre usar o no el debug
# Nos conectamos utilizando remote
con = remote("163.10.20.26", 10002)
# para quitar el texto que no nos interesa (banner),
# leemos hasta justo antes de la cuenta, es decir, hasta ":\n"

con.recvuntil(b"flag!:\n") 

# Leemos hasta el salto de línea, la cuenta deseada
cuenta = con.recvline(timeout=0.2)
print(type(cuenta))
print(cuenta)
# Pasamos los bytes a string, para poder realizar la cuenta
cuenta = cuenta.decode().split()

# Convierto a entero los operandos
op1 = int(cuenta[0])
op2 = int(cuenta[2])

# El operador es el segundo elemento de la lista
operador = cuenta[1]
# Sumo multiplico o resto según el operador
if operador == '-':
 resultado = op1 - op2
elif operador == '*':
 resultado = op1 * op2
else:
    resultado = op1 + op2
# Enviamos la respuesta de la cuenta, como bytes:
con.sendline((str(resultado) + "\n").encode())
# Imprimimos toda la respuesta del servidor
print(con.recv(timeout=0.3))

#CONSULTAR, PORQUE AHORA ESTO ANDA RAPIDO? A DIFERENCIA DEL DE ANTES