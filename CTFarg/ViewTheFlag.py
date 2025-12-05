from pwn import *
host = "lottery.ctf.cert.unlp.edu.a"
port = 35001

con = remote(host, port)
print(con.recvuntil(b"Welcome to the Blackjack table!\n"))

