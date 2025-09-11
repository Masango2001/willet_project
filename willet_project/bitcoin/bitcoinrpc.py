from bitcoinrpc.authproxy import AuthServiceProxy
from django.conf import settings


def get_rpc_connection():
    """
    Retourne une connexion RPC au daemon Bitcoin.
    """
    try:
        rpc_user = settings.BITCOIN_RPC_USER
        rpc_password = settings.BITCOIN_RPC_PASSWORD
        rpc_host = settings.BITCOIN_RPC_HOST
        rpc_port = settings.BITCOIN_RPC_PORT

        rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
        return AuthServiceProxy(rpc_url)
    except Exception as e:
        raise ConnectionError(f"Impossible de se connecter au daemon Bitcoin : {e}")
