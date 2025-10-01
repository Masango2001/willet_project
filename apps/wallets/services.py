# from decimal import Decimal
# from django.conf import settings
# from .models import Wallet, UTXO
# from .lightning_client import get_lnd_stub
# from apps.lightning import lightning_pb2 as ln
# from apps.lightning import lightning_pb2_grpc as lnrpc
# from bitcoinrpc.authproxy import JSONRPCException
# from bitcoin.bitcoinrpc import get_rpc_connection
# import grpc

# # -------------------------
# # Basic user wallet management
# # -------------------------
# def create_wallet_for_user(user, wallet_name: str):
#     w, created = Wallet.objects.get_or_create(user=user, name=wallet_name)
#     rpc = get_rpc_connection()

#     try:
#         # Essaie de créer le wallet
#         rpc.createwallet(wallet_name, False, True, "", True, True)
#     except JSONRPCException as e:
#         msg = str(e)
#         if "-4: Wallet file" in msg or "-4: Wallet already exists" in msg:
#             # Wallet existe → on vérifie s'il est déjà chargé
#             try:
#                 rpc.loadwallet(wallet_name)
#             except JSONRPCException as e2:
#                 if "-35: Wallet" in str(e2) and "is already loaded" in str(e2):
#                     # Wallet déjà chargé → on continue sans erreur
#                     pass
#                 else:
#                     raise
#         else:
#             raise

#     # Connexion RPC spécifique au wallet
#     rpc_wallet = get_rpc_connection(wallet_name=wallet_name)

#     # Génère une nouvelle adresse
#     address = rpc_wallet.getnewaddress()
#     w.current_address = address
#     w.save()
#     return w

# def get_wallet_balance(wallet: Wallet):
#     # On-chain balance
#     try:
#         rpc = get_rpc_connection(wallet_name=wallet.name)
#         utxos = rpc.listunspent(0, 999999, [wallet.current_address])
#         total_sats = sum(int(u['amount'] * 1e8) for u in utxos)
#         wallet.onchain_balance = Decimal(total_sats) / Decimal(1e8)
#     except Exception:
#         wallet.onchain_balance = Decimal('0.0')

#     # Lightning balance
#     try:
#         stub = get_lnd_stub()
#         resp = stub.WalletBalance(ln.WalletBalanceRequest())
#         wallet.lightning_balance = Decimal(resp.total_balance) / Decimal(1e8)
#     except grpc.RpcError:
#         wallet.lightning_balance = Decimal('0.0')

#     wallet.save()
#     return wallet.total_balance()


# # -------------------------
# # On-chain operations
# # -------------------------
# def generate_new_address(wallet: Wallet):
#     rpc = get_rpc_connection(wallet_name=wallet.name)
#     address = rpc.getnewaddress()
#     wallet.current_address = address
#     wallet.save()
#     return address


# def get_onchain_balance(wallet: Wallet):
#     rpc = get_rpc_connection(wallet_name=wallet.name)
#     utxos = rpc.listunspent(0, 999999, [wallet.current_address])
#     total_sats = sum(int(u['amount'] * 1e8) for u in utxos)
#     return Decimal(total_sats) / Decimal(1e8)


# def send_onchain_payment(wallet: Wallet, to_address: str, amount_btc: Decimal, fee_rate=None):
#     rpc = get_rpc_connection(wallet_name=wallet.name)
#     try:
#         txid = rpc.sendtoaddress(to_address, float(amount_btc))
#         return txid
#     except JSONRPCException as e:
#         raise


# def list_transactions(wallet: Wallet):
#     rpc = get_rpc_connection(wallet_name=wallet.name)
#     return rpc.listtransactions("*", 100)


# # -------------------------
# # Lightning operations (LND)
# # -------------------------
# def get_ln_balance():
#     stub = get_lnd_stub()
#     try:
#         resp = stub.WalletBalance(ln.WalletBalanceRequest())
#         return {
#             'total_sats': resp.total_balance,
#             'confirmed_sats': resp.confirmed_balance,
#             'unconfirmed_sats': resp.unconfirmed_balance
#         }
#     except grpc.RpcError:
#         return {'total_sats': 0, 'confirmed_sats': 0, 'unconfirmed_sats': 0}


# def create_invoice(amount_sats: int, memo: str = "", expiry: int = 3600):
#     stub = get_lnd_stub()
#     req = ln.Invoice(value=amount_sats, memo=memo, expiry=expiry)
#     resp = stub.AddInvoice(req)
#     return {'payment_request': resp.payment_request, 'r_hash': resp.r_hash.hex()}


# def pay_invoice(payment_request: str, timeout_seconds: int = 30):
#     stub = get_lnd_stub()
#     req = ln.SendRequest(payment_request=payment_request)
#     resp = stub.SendPaymentSync(req)
#     return {
#         'payment_error': resp.payment_error,
#         'payment_preimage': resp.payment_preimage.hex() if resp.payment_preimage else None
#     }


# def list_invoices():
#     stub = get_lnd_stub()
#     resp = stub.ListInvoices(ln.ListInvoiceRequest(pending_only=False))
#     return resp.invoices


# def list_payments():
#     stub = get_lnd_stub()
#     resp = stub.ListPayments(ln.ListPaymentsRequest())
#     return resp.payments


# # -------------------------
# # Channels
# # -------------------------
# def connect_peer(pubkey: str, host: str, port: int = 9735):
#     stub = get_lnd_stub()
#     req = ln.ConnectPeerRequest(addr=ln.LightningAddress(pubkey=pubkey, host=f"{host}:{port}"))
#     return stub.ConnectPeer(req)


# def open_channel(pubkey: str, local_funding_sats: int):
#     stub = get_lnd_stub()
#     req = ln.OpenChannelRequest(node_pubkey=bytes.fromhex(pubkey), local_funding_sat=local_funding_sats)
#     resp = stub.OpenChannelSync(req)
#     return resp


# def close_channel(channel_point: str, force=False):
#     stub = get_lnd_stub()
#     txid, index = channel_point.split(':')
#     req = ln.CloseChannelRequest(channel_point=ln.ChannelPoint(funding_txid_str=txid, output_index=int(index)), force=force)
#     stream = stub.CloseChannel(req)
#     updates = [update for update in stream]
#     return updates


# def list_channels():
#     stub = get_lnd_stub()
#     resp = stub.ListChannels(ln.ListChannelsRequest())
#     return resp.channels
