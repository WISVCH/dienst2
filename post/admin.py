from django.contrib import admin
from reversion.admin import VersionAdmin

from post.models import *


class CategoryAdmin(VersionAdmin):
    """CategoryAdmin"""
    search_fields = ('name',)
    list_display = ('name', 'grouping', 'counting')


class SourceAdmin(VersionAdmin):
    """SourceAdmin"""
    search_fields = ('name',)
    list_filter = ('location',)
    list_display = ('name', 'location')


class ItemAdmin(VersionAdmin):
    """ItemAdmin"""
    date_hierarchy = 'date'
    search_fields = ('description',)
    list_filter = ('sender', 'receiver', 'category')
    list_display = ('description', 'sender', 'receiver', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Item, ItemAdmin)
