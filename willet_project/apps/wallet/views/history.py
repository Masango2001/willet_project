from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.wallet.models import TransactionHistory
from apps.wallet.serializers import TransactionSerializer

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            transactions = TransactionHistory.objects.filter(user=request.user).order_by('-date')
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Une erreur s’est produite lors de la récupération de l’historique : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
