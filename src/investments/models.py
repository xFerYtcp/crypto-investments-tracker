from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext as _


# Create your models here.
ORDER_TYPE_CATEGORY = (
    ("buy", _("Buy")),
    ("sell", _("Sell")),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de modification"), auto_now=True)

    class Meta:
        abstract = True


class OrderType(BaseModel):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    category = models.CharField(
        _("Order type category"), max_length=50, choices=ORDER_TYPE_CATEGORY
    )

    class Meta:
        verbose_name = _("Order type")
        verbose_name_plural = _(f"Order types")

    def __str__(self):
        return f"{self.name}"


class Exchange(BaseModel):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    url = models.URLField(_("Url"), max_length=200)

    class Meta:
        verbose_name = _("Exchange")
        verbose_name_plural = _(f"Exchanges")

    def __str__(self):
        return f"{self.name}"


class Currency(BaseModel):
    code = models.CharField(_("Code"), max_length=50, unique=True)
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _(f"Currencies")

    def __str__(self):
        return f"{self.code} - {self.name}"


class Investments(BaseModel):
    date = models.DateTimeField(_("DateTime"), auto_now=False, auto_now_add=False)
    currency = models.ForeignKey(
        "investments.Currency", verbose_name=_("Currency"), on_delete=models.CASCADE
    )
    order_type = models.ForeignKey(
        "investments.OrderType", verbose_name=_("Order type"), on_delete=models.CASCADE
    )
    price = models.FloatField(_("Price"))
    quantity = models.FloatField(_("Quantity"))
    cost = models.FloatField(_("Cost"), blank=True)
    exchange = models.ForeignKey(
        "investments.Exchange",
        verbose_name=_("Exchange"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reference = models.CharField(_("reference"), max_length=250, blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("User"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Investment")
        verbose_name_plural = _("Investments")

    def save(self, *args, **kwargs):
        self.cost = self.quantity * self.price
        super(Investments, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {self.currency} {self.order_type} {self.quantity}"

    def get_absolute_url(self):
        return reverse("Invests _detail", kwargs={"pk": self.pk})
