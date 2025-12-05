from pwn import *
host = "lottery.ctf.cert.unlp.edu.ar"
port = 35001
con = remote(host, port)
print(con.recvuntil