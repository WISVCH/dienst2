from django.contrib import admin
from reversion.admin import VersionAdmin

from post.models import *


class CategoryAdmin(VersionAdmin):
    """CategoryAdmin"""


admin.site.register(Category, CategoryAdmin)


class SourceAdmin(VersionAdmin):
    """SourceAdmin"""


admin.site.register(Source, SourceAdmin)


class ItemAdmin(VersionAdmin):
    """ItemAdmin"""


admin.site.register(Item, ItemAdmin)
