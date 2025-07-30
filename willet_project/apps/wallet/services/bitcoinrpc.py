from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.conf import settings


class BitcoinRPC:
    def __init__(self):
        try:
            rpc_user = settings.BITCOIN_RPC_USER
            rpc_password = settings.BITCOIN_RPC_PASSWORD
            rpc_host = settings.BITCOIN_RPC_HOST
            rpc_port = settings.BITCOIN_RPC_PORT

            rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
            self.rpc = AuthServiceProxy(rpc_url)
        except Exception as e:
            raise ConnectionError(f"Erreur de connexion au daemon Bitcoin : {e}")

    def get_balance(self, address: str) -> float:
        """
        Retourne le montant total reçu par une adresse Bitcoin.
        """
        try:
            return self.rpc.getreceivedbyaddress(address)
        except JSONRPCException as e:
            raise ValueError(f"Erreur RPC lors de la récupération du solde : {e}")
        except Exception as e:
            raise RuntimeError(f"Erreur inattendue : {e}")

    def send_bitcoin(self, to_address: str, amount: float) -> str:
        """
        Envoie des bitcoins à l'adresse spécifiée.
        """
        try:
            return self.rpc.sendtoaddress(to_address, amount)
        except JSONRPCException as e:
            raise ValueError(f"Erreur RPC lors de l’envoi : {e}")
        except Exception as e:
            raise RuntimeError(f"Erreur inattendue : {e}")
