from bitcoinrpc.authproxy import AuthServiceProxy
from django.conf import settings
from bitcoinrpc.authproxy import JSONRPCException

def get_rpc_connection(wallet_name: str = None):
    """
    Retourne une connexion RPC au daemon Bitcoin.
    Si wallet_name est fourni, on charge le wallet correspondant.
    """
    try:
        rpc_user = settings.BITCOIN_RPC_USER
        rpc_password = settings.BITCOIN_RPC_PASSWORD
        rpc_host = settings.BITCOIN_RPC_HOST
        rpc_port = settings.BITCOIN_RPC_PORT

        rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
        rpc = AuthServiceProxy(rpc_url)

        # Crée et/ou charge le wallet spécifique
        if wallet_name:
            try:
                rpc.createwallet(wallet_name)
            except JSONRPCException:
                # Wallet existe déjà, on ignore l'erreur
                pass
            rpc.loadwallet(wallet_name)

        return rpc

    except Exception as e:
        raise ConnectionError(f"Impossible de se connecter au daemon Bitcoin : {e}")
