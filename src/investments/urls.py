from django.urls import path, include
from .views import (
    InvestmentsViewSet,
    ExchangeViewSet,
    CurrencyViewSet,
    BalanceViewSet,
    OrderTypeViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"investments", InvestmentsViewSet)
router.register(r"currency", CurrencyViewSet)
router.register(r"exchange", ExchangeViewSet)
router.register(r"order_type", OrderTypeViewSet)

app_name = "investments"

urlpatterns = [
    path("", include(router.urls)),
    path("balance", BalanceViewSet.as_view()),
]
