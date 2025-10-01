from decouple import config
from Crypto.Cipher import AES
import base64

KEY = config('WALLET_SECRET_KEY')[:32].encode() 

def encrypt_private_key(plain_text: str) -> str:
    cipher = AES.new(KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()

def decrypt_private_key(cipher_text: str) -> str:
    data = base64.b64decode(cipher_text)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
