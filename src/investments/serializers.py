from rest_framework import routers, serializers, viewsets
from .models import OrderType, Currency, Investments, Exchange


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ("id", "name", "desc", "category")


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ("id", "name", "url")


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class InvestmentsSerializer(serializers.ModelSerializer):
    # currency = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrencySerializer())
    # exchange = serializers.PrimaryKeyRelatedField(read_only=True, default=ExchangeSerializer())
    currency = CurrencySerializer(read_only=True)
    exchange = ExchangeSerializer(read_only=True)
    order_type = OrderTypeSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Investments
        fields = (
            "id",
            "date",
            "exchange",
            "exchange_id",
            "currency",
            "currency_id",
            "order_type",
            "order_type_id",
            "price",
            "quantity",
            "cost",
            "reference",
            "comment",
            "user",
        )
        extra_kwargs = {
            "currency_id": {"source": "currency", "write_only": True},
            "exchange_id": {"source": "exchange", "write_only": True},
            "order_type_id": {"source": "order_type", "write_only": True},
        }


class BalanceSerializer(serializers.Serializer):
    currency__code = serializers.CharField()
    currency__id = serializers.IntegerField()
    currency__name = serializers.CharField()
    buy_cost = serializers.FloatField()
    buy_quantity = serializers.FloatField()
    sell_cost = serializers.FloatField()
    sell_quantity = serializers.FloatField()
