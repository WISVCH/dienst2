from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import CreateView, WeekArchiveView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from post.filters import ItemFilterSet, AVFilterSet
from post.forms import ItemForm
from post.models import Item, Category


class ItemListView(FormMixin, FilterView):
    form_class = ItemForm
    model = Item
    paginate_by = 50
    filterset_class = ItemFilterSet

    def get_queryset(self):
        return super(ItemListView, self).get_queryset()\
            .order_by('-date')\
            .select_related('sender', 'recipient', 'category')

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context.update({
            'form': self.get_form()
        })
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super(ItemListView, self).get_filterset_kwargs(filterset_class)
        kwargs.update({
            'prefix': 'filter',
        })

        return kwargs


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('post_index')


class ItemWeekArchiveView(WeekArchiveView):
    model = Item
    ordering = 'date'

    allow_empty = True
    date_field = "date"
    week_format = "%W"

    def get_queryset(self):
        return super(ItemWeekArchiveView, self).get_queryset().select_related('sender', 'recipient', 'category')


class AVListView(FilterView):
    template_name = 'post/av.html'
    model = Category
    filterset_class = AVFilterSet

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        self.object_list = self.filterset.qs.prefetch_related('items__sender', 'items__recipient')
        context = self.get_context_data(filter=self.filterset,
                                        object_list=self.object_list)
        return self.render_to_response(context)
