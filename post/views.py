from django.core.urlresolvers import reverse_lazy
from django.db.models import Prefetch
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, CreateView, WeekArchiveView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from post.filters import ItemFilterSet, AVFilterSet
from post.forms import ItemForm
from post.models import Item, Category

post_data = {
    'title': 'Post',
    'ng_app': 'post',
    'navbar': {
        'title': 'Post',
        'items': [
            ('#/dashboard', 'Dashboard'),
            ('#/week', 'Weekoverzicht'),
            ('#/av', 'AV-Overzicht'),
        ]
    }
}


def index(request):
    return render_to_response('post/dashboard.html', post_data, context_instance=RequestContext(request))


class ItemListView(FormMixin, FilterView):
    form_class = ItemForm
    model = Item
    paginate_by = 50
    filterset_class = ItemFilterSet

    def get_queryset(self):
        return super(ItemListView, self).get_queryset().select_related('sender', 'receiver', 'category')

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
    allow_empty = True
    queryset = Item.objects.all()
    date_field = "date"
    week_format = "%W"

    def get_queryset(self):
        return super(ItemWeekArchiveView, self).get_queryset().select_related('sender', 'receiver', 'category')


class AVListView(FilterView):
    template_name = 'post/av.html'
    model = Category
    filterset_class = AVFilterSet
