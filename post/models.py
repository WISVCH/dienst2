from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from post.querysets import ItemQuerySet


class Category(models.Model):
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ['name']

    name = models.CharField(_('name'), max_length=128, blank=False)
    grouping = models.BooleanField(_('grouping'), default=False)
    counting = models.BooleanField(_('counting'), default=False)

    def __unicode__(self):
        return self.name


class Source(models.Model):
    class Meta:
        verbose_name = _("source")
        verbose_name_plural = _("sources")

    INTERNAL = 'I'
    EXTERNAL = 'E'
    LOCATIONS = (
        (INTERNAL, _('internal')),
        (EXTERNAL, _('external'))
    )

    name = models.CharField(_('name'), max_length=128, blank=False)
    location = models.CharField(_('location'), max_length=1, choices=LOCATIONS)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ['-date']

    date = models.DateTimeField(_('date'), auto_now_add=True)
    description = models.CharField(_('description'), max_length=128, blank=False)
    sender = models.ForeignKey(Source, related_name='sent_items')
    receiver = models.ForeignKey(Source, related_name='received_items')
    category = models.ForeignKey(Category, related_name='items')

    objects = ItemQuerySet.as_manager()

    def __unicode__(self):
        return self.description
