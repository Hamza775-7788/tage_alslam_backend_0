from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from .models import Drug, DrugCategory, DrugUnits, Order,Offer,OrderItem
from .serializers import (
    DrugSerializer,
    DrugCategorySerializer,
    DrugUnitsSerializer,
    OrderSerializer,
    OfferSerializer,
    DrugMostOrderingSerializer,
)
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.decorators import api_view 
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all().filter(is_active=True).order_by("id")
    serializer_class = DrugSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends =[SearchFilter]
    search_fields = ['=id','^name_ar','^name_en']

class DrugCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrugCategory.objects.all()
    serializer_class = DrugCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by("-id")
    serializer_class = OfferSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DrugUnitsViewSet(viewsets.ModelViewSet):
    queryset = DrugUnits.objects.all()
    serializer_class = DrugUnitsSerializer
    # permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     # إظهار فقط الطلبات الخاصة بالمستخدم الحالي
    #     return self.queryset.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
class DrugMostOrderedViewSet(viewsets.ViewSet):

    def list(self, request):
        grouped = (
            OrderItem.objects
            .values('drug_id')
            .annotate(
                total_quantity=Sum('quantity'),
                # total_price=Sum('total_price')
            )
            .order_by('-total_quantity')[:10]
        )

        results = []
        for item in grouped:
            try:
                drug = Drug.objects.get(id=item['drug_id'])
                results.append({
                    'drug': drug,
                    'total_quantity': item['total_quantity'],
                    # 'total_price': item['total_price'],
                })
            except Drug.DoesNotExist:
                continue

        serializer = DrugMostOrderingSerializer(results, many=True)
        return Response(serializer.data)
    


@api_view(["GET"])
def get_un_active_drugs(request):
    last_sync = request.GET.get("last_sync")  # مثل: 2025-06-25T00:00:00Z أو null

    drugs_qs = Drug.objects.filter(is_active=False)

    if last_sync and last_sync.lower() != "null":
        parsed_date = parse_datetime(last_sync)
        if parsed_date:
            drugs_qs = drugs_qs.filter(updated_at__gte=parsed_date)
        else:
            return Response({"error": "Invalid datetime format."}, status=400)

    drugs = drugs_qs.values("id", "updated_at")
    current_sync_time = now()
    return Response({"data": list(drugs),"last_sync":f"{current_sync_time}"})