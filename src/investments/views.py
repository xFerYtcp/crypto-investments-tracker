from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Investments, Exchange, Currency, OrderType
from rest_framework.generics import ListAPIView
from .serializers import (
    InvestmentsSerializer,
    ExchangeSerializer,
    CurrencySerializer,
    BalanceSerializer,
    OrderTypeSerializer,
)
from django.db.models import Q, Sum, Count, Avg

# Create your views here.


class InvestmentsViewSet(viewsets.ModelViewSet):
    queryset = Investments.objects.all()
    serializer_class = InvestmentsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class OrderTypeViewSet(viewsets.ModelViewSet):
    queryset = OrderType.objects.all().order_by("name")
    serializer_class = OrderTypeSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by("code")
    serializer_class = CurrencySerializer
    permission_classes = [
        IsAuthenticated,
    ]


class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all().order_by("name")
    serializer_class = ExchangeSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class BalanceViewSet(ListAPIView):
    queryset = Investments.objects.all().order_by("-date")
    pagination_class = None
    filter_fields = ["currency"]
    serializer_class = BalanceSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    # filter_fields = ["area_type", "places__sessions__sightings__codesp"]

    def get_queryset(self):
        qs = super(BalanceViewSet, self).get_queryset()
        qs = (
            qs.values("currency__code", "currency__id", "currency__name")
            .annotate(buy_cost=Sum("cost", filter=Q(order_type__category="buy")))
            .annotate(buy_quantity=Sum("quantity", filter=Q(order_type__category="buy")))
            .annotate(sell_cost=Sum("cost", filter=Q(order_type__category="sell")))
            .annotate(sell_quantity=Sum("quantity", filter=Q(order_type__category="sell")))
            .filter(user=self.request.user)
            .order_by("currency__code")
        )
        return qs
