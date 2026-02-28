from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions

from .models import FinanceSetting, FinanceRecord
from .serializers import FinanceSettingSerializer, FinanceRecordSerializer

class FinanceSettingViewSet(viewsets.ModelViewSet):
    serializer_class = FinanceSettingSerializer
    lookup_field = 'key'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinanceSetting.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception:
            return Response({"key": kwargs.get('key'), "value": None}, status=status.HTTP_200_OK)

class FinanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FinanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinanceRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def get_record(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if not month or not year:
            return Response({"error": "month and year are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            record = FinanceRecord.objects.get(user=request.user, month=month, year=year)
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        except FinanceRecord.DoesNotExist:
            return Response({"month": month, "year": year, "value": None}, status=status.HTTP_200_OK)
