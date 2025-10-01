from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.wallets.models import Wallet
from .services import create_invoice, pay_invoice, check_invoice_status
from .serializers import LightningInvoiceSerializer, LightningPaymentSerializer
from .models import LightningInvoice

# --- Créer une invoice ---
class LightningInvoiceCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get('wallet_id')
        amount_sats = request.data.get('amount_sats')
        memo = request.data.get('memo', '')
        if not wallet_id or not amount_sats:
            return Response({"error": "wallet_id et amount_sats sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error":"Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        invoice = create_invoice(wallet, int(amount_sats), memo)
        return Response(LightningInvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)

# --- Payer une invoice ---
class LightningPayInvoice(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get('wallet_id')
        invoice_str = request.data.get('invoice')
        if not wallet_id or not invoice_str:
            return Response({"error":"wallet_id et invoice sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error":"Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        payment = pay_invoice(wallet, invoice_str)
        return Response(LightningPaymentSerializer(payment).data, status=status.HTTP_200_OK)

# --- Vérifier statut d'une invoice ---
class LightningInvoiceStatus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invoice_str = request.data.get('invoice')
        if not invoice_str:
            return Response({"error":"invoice est requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            invoice = LightningInvoice.objects.get(invoice=invoice_str, wallet__user=request.user)
        except LightningInvoice.DoesNotExist:
            return Response({"error":"Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
        invoice = check_invoice_status(invoice)
        return Response(LightningInvoiceSerializer(invoice).data, status=status.HTTP_200_OK)
