from decouple import config
from Crypto.Cipher import AES
import base64

from django.shortcuts import get_object_or_404

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


from django.shortcuts import get_object_or_404

def get_user_wallet(user, wallet_id=None):
    """
    Retourne le wallet pour l'utilisateur :
    - Si wallet_id fourni, récupère ce wallet
    - Sinon, récupère le wallet par défaut
    """
    # import local pour éviter circular import
    from apps.wallets.models import Wallet  

    if wallet_id:
        wallet = get_object_or_404(Wallet, id=wallet_id, user=user)
    else:
        wallet = get_object_or_404(Wallet, user=user, is_default=True)
    return wallet
