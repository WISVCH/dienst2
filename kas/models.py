from __future__ import unicode_literals

from functools import reduce

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        ordering = ["-date"]

    user = models.CharField(_("user"), max_length=32, blank=False)
    date = models.DateTimeField(_("date"), auto_now_add=True)

    amount = models.FloatField(_("amount"), blank=False)
    description = models.TextField(_("description"), blank=False)

    valid = models.BooleanField(_("valid"), default=True)

    PIN = "P"
    CASH = "C"
    METHODS = ((PIN, _("PIN")), (CASH, _("Cash")))

    method = models.CharField(_("method"), max_length=1, choices=METHODS, default=CASH)

    @property
    def closure(self):
        closure = getattr(self, "_closure", None)
        if not closure:
            try:
                if self.date:
                    # Existing transaction, try to get the first closure after this transaction
                    closure = Closure.objects.filter(date__gte=self.date).order_by(
                        "id"
                    )[0]
                else:
                    # New transaction, try to get a non-finished closure
                    closure = Closure.objects.filter(finished=False)[0]
                setattr(self, "_closure", closure)
            except IndexError:
                pass
        return closure

    @property
    def editable(self):
        return not (self.closure and self.closure.finished)

    def clean(self):
        super(Transaction, self).clean()

        if not self.editable:
            raise ValidationError(_("Transaction not editable."))

    def __str__(self):
        return (
            capfirst(_("transaction"))
            + " "
            + timezone.localtime(self.date).strftime("%Y-%m-%d %H:%M")
        )


class Closure(models.Model):
    class Meta:
        verbose_name = _("closure")
        verbose_name_plural = _("closures")
        ordering = ["-date"]

    user = models.CharField(_("user"), max_length=32, blank=False)

    date = models.DateTimeField(_("date"), auto_now=True)

    num_e500 = models.IntegerField(_("500 euro"), default=0)
    num_e200 = models.IntegerField(_("200 euro"), default=0)
    num_e100 = models.IntegerField(_("100 euro"), default=0)
    num_e50 = models.IntegerField(_("50 euro"), default=0)
    num_e20 = models.IntegerField(_("20 euro"), default=0)
    num_e10 = models.IntegerField(_("10 euro"), default=0)
    num_e5 = models.IntegerField(_("5 euro"), default=0)
    num_e2 = models.IntegerField(_("2 euro"), default=0)
    num_e1 = models.IntegerField(_("1 euro"), default=0)
    num_e050 = models.IntegerField(_("50 eurocent"), default=0)
    num_e020 = models.IntegerField(_("20 eurocent"), default=0)
    num_e010 = models.IntegerField(_("10 eurocent"), default=0)
    num_e005 = models.IntegerField(_("5 eurocent"), default=0)

    total = models.FloatField(
        _("total register content"), blank=True, default=0, editable=False
    )

    pin = models.FloatField(_("pin receipt"), default=0)

    transactions_pin = models.FloatField(
        _("pin transactions"), blank=True, editable=False, default=0
    )
    transactions_cash = models.FloatField(
        _("cash transactions"), blank=True, editable=False, default=0
    )

    notes = models.TextField(_("notes"), blank=True)

    finished = models.BooleanField(_("finished"), default=False)

    ###################################################

    @property
    def transactions(self):
        transactions = Transaction.objects.all()

        if self.previous:
            transactions = transactions.filter(date__gt=self.previous.date)

        if self.finished:
            transactions = transactions.filter(date__lte=self.date)

        return transactions

    @property
    def previous(self):
        previous = None
        try:
            if self.pk:
                previous = Closure.objects.filter(date__lt=self.date)[0:1].get()
            else:
                previous = Closure.objects.latest("pk")
        except Closure.DoesNotExist:
            pass
        return previous

    @property
    def cashdifference(self):
        return round(
            self.total - getattr(self.previous, "total", 0) - self.transactions_cash, 2
        )

    @property
    def pindifference(self):
        return round(self.pin - self.transactions_pin)

    def clean(self):
        super(Closure, self).clean()

        if self.pk and Closure.objects.get(pk=self.pk).finished:
            raise ValidationError(_("Closure already finished."))

        if self.previous and not self.previous.finished:
            raise ValidationError(_("Previous closure not finished yet"))

        # Calculate the total register contents
        self.total = (
            500 * self.num_e500
            + 200 * self.num_e200
            + 100 * self.num_e100
            + 50 * self.num_e50
            + 20 * self.num_e20
            + 10 * self.num_e10
            + 5 * self.num_e5
            + 2 * self.num_e2
            + 1 * self.num_e1
            + 0.5 * self.num_e050
            + 0.2 * self.num_e020
            + 0.1 * self.num_e010
            + 0.05 * self.num_e005
        )

        # Calculate the total cash transactions
        transactions_cash = self.transactions.filter(
            valid=True, method=Transaction.CASH
        )
        amounts = map(lambda transaction: transaction.amount, transactions_cash)
        self.transactions_cash = reduce(lambda x, y: x + y, amounts, 0)

        # Calculate the total cash transactions
        transactions_pin = self.transactions.filter(valid=True, method=Transaction.PIN)
        amounts = map(lambda transaction: transaction.amount, transactions_pin)
        self.transactions_pin = reduce(lambda x, y: x + y, amounts, 0)

    def __str__(self):
        return (
            capfirst(_("closure"))
            + " "
            + timezone.localtime(self.date).strftime("%Y-%m-%d %H:%M")
        )
