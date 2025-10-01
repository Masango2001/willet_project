# import grpc
# import os
# from django.conf import settings
# from apps.lightning import lightning_pb2 as ln
# from apps.lightning import lightning_pb2_grpc as lnrpc

# def _load_tls_cert(path):
#     with open(path, 'rb') as f:
#         return f.read()

# def _load_macaroon(path):
#     with open(path, 'rb') as f:
#         return f.read().hex()

# def get_lnd_stub():
#     host = settings.LND_GRPC_HOST
#     port = int(settings.LND_GRPC_PORT)
#     tls_path = settings.LND_TLS_CERT_PATH
#     macaroon_path = settings.LND_MACAROON_PATH

#     cert = _load_tls_cert(tls_path)
#     creds = grpc.ssl_channel_credentials(cert)

#     # attach macaroon to metadata via interceptor
#     def metadata_callback(context, callback):
#         macaroon = _load_macaroon(macaroon_path)
#         callback([('macaroon', macaroon)], None)

#     auth_creds = grpc.metadata_call_credentials(
#         lambda context, callback: callback([('macaroon', _load_macaroon(macaroon_path))], None)
#     )
#     composite_creds = grpc.composite_channel_credentials(creds, auth_creds)

#     channel = grpc.secure_channel(f"{host}:{port}", composite_creds)
#     stub = lnrpc.LightningStub(channel)
#     return stub
