from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from post.querysets import ItemQuerySet


@python_2_unicode_compatible
class Category(models.Model):
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ['name']

    name = models.CharField(_('name'), max_length=128, blank=False)
    grouping = models.BooleanField(_('grouping'), default=False)
    counting = models.BooleanField(_('counting'), default=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Contact(models.Model):
    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    INTERNAL = 'I'
    EXTERNAL = 'E'
    LOCATIONS = (
        (INTERNAL, _('internal')),
        (EXTERNAL, _('external'))
    )

    name = models.CharField(_('name'), max_length=128, blank=False)
    location = models.CharField(_('location'), max_length=1, choices=LOCATIONS)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Item(models.Model):
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ('date',)

    date = models.DateTimeField(_('date'), auto_now_add=True)
    description = models.CharField(_('description'), max_length=128, blank=False)
    sender = models.ForeignKey(Contact, verbose_name=_('sender'), related_name='sent_items', on_delete=models.PROTECT)
    recipient = models.ForeignKey(Contact, verbose_name=_('recipient'), related_name='received_items',
                                  on_delete=models.PROTECT)
    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='items', on_delete=models.PROTECT)

    objects = ItemQuerySet.as_manager()

    def __str__(self):
        return self.description
