from django.contrib import admin
from .models import Investments, Currency, Exchange, OrderType

# Register your models here.


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    fields = ("name", "url")


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "desc")


class InvestmentsAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "currency",
        "order_type",
        "price",
        "quantity",
        "cost",
        "exchange",
    )


admin.site.register(OrderType, OrderTypeAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Investments, InvestmentsAdmin)
