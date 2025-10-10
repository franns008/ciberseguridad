#ejercicio 9
import base64
from Crypto.Cipher import AES
import codecs

mensaje = b"dV5t6M4m2AcjYWsxC9iO+YXlc0r0ClfwyTGtpuWdPh9fvH+8cejJWOHYq1qH7qA+Kj7Lci133Awj3rnoq42p532+fvbN64oZ8R/TlMkhw47nmIM5gPN+rt45985jeiIDbdpCu1ig09Rzepl4/kawM1AzFtoMzTvadmx11qSFp+UD81yiRz6HjaFLIIIIQnbzFrmcOIOGEQ6LBEYz2cTW6JPBs7MHpqDrcrzZoLcb7Ah2jQSIId+YZ90JmRt83yTe66a60kqL5SoW7/463Suyyp9xDhrgFu6YS3ScNDgOamADIcKmLUTxrvYooZIjL7s+thek3aBPrv/yB84YNUhX7MOxjiTiP02nBJ1E1dOA0ew75BeARB4cHKVfLMnPMkjSYyiQ2eTWqYd4cZ+14Z9joNVA1Uei8Pg4KITPfJYy3Mc="
clave = "CLAVE RE SECRETA".encode('utf8')
cipher = AES.new(clave, AES.MODE_ECB)
mensaje_bytes = base64.b64decode(mensaje)
plain_text = cipher.decrypt(mensaje_bytes)
print(plain_text.decode('utf8'))

#ejercicio 10
#cifrado XOR
import codecs

import codecs

def XOR(key: bytes, data: bytes) -> bytes:
    return bytes([b ^ key[0] for b in data])  # XOR con un solo byte de clave

cipher_hex = b"08296632232822342f27356637332366252f2034273466252928661e09146a66252e236866162334296624332328296a662a2766202a272166222366233532236634233229662335660f053d092c7619257628193e7634676767737e7f737f73737f192527352f192e27252d232334343b"
cipher_bytes = codecs.decode(cipher_hex, "hex")

for i in range(256):
    resultado = XOR(bytes([i]), cipher_bytes)
    try:
        texto = resultado.decode("utf-8")
        if "IC{" in texto:   # mostrar solo posibles flags
            print(f"Clave {i}: {texto}")
    except UnicodeDecodeError:
        continue

