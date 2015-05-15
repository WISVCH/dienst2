from django.contrib import admin

from kas.models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'amount', 'method', 'description', 'valid']
    fields = ['amount', 'description', 'valid', 'method']

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        obj.save()

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.closure is not None and obj.closure.finished:
            return False
        else:
            return True


class ClosureAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'total', 'cashdifference', 'pindifference', 'notes', 'finished']
    fields = ['num_e500', 'num_e200', 'num_e100', 'num_e50', 'num_e20', 'num_e10', 'num_e5', 'num_e2', 'num_e1',
              'num_e050', 'num_e020', 'num_e010', 'num_e005', 'pin', 'notes', 'finished']

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.username
        obj.save()

    def has_delete_permission(self, request, obj=None):
        if obj and obj.finished:
            return False
        else:
            return True


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Closure, ClosureAdmin)
