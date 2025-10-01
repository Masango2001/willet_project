from django.test import TestCase
from bitcoin.bitcoinrpc import get_rpc_connection

class BitcoinConnectionTest(TestCase):
    def test_rpc_connection(self):
        rpc = get_rpc_connection()
        try:
            info = rpc.getblockchaininfo()
            print("Connexion RPC OK:", info["chain"])
        except Exception as e:
            self.fail(f"Erreur de connexion RPC : {e}")
