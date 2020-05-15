from __future__ import unicode_literals

from django.contrib import admin

from post.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """CategoryAdmin"""

    search_fields = ("name",)
    list_display = ("name", "grouping", "counting")


@admin.register(Contact)
class SourceAdmin(admin.ModelAdmin):
    """SourceAdmin"""

    search_fields = ("name",)
    list_filter = ("location",)
    list_display = ("name", "location")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """ItemAdmin"""

    date_hierarchy = "date"
    search_fields = ("description",)
    list_filter = ("sender", "recipient", "category")
    list_display = ("description", "date", "sender", "recipient", "category")
