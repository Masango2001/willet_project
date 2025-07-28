 
from bitcoinrpc.authproxy import AuthServiceProxy
from django.conf import settings

class BitcoinRPC:
    def __init__(self):
        self.rpc = AuthServiceProxy(
            f"http://{settings.BITCOIN_RPC_USER}:{settings.BITCOIN_RPC_PASSWORD}@{settings.BITCOIN_RPC_URL}"
        )

    def get_balance(self, address):
        return self.rpc.getreceivedbyaddress(address)

    def send_bitcoin(self, from_address, to_address, amount):
        return self.rpc.sendtoaddress(to_address, amount)