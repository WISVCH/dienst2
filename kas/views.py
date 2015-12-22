from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from kas.models import Transaction

from kas.forms import TransactionForm


def index(request):
    post_data = {
        'title': 'Kasbeheer',
        'ng_app': 'kas',
        'navbar': {
            'title': 'Kasbeheer',
            'items': [
                ('#/transactions', 'Transacties'),
                ('#/closures', 'Dagafsluitingen'),
                ('#/barcode', 'Barcode Tool'),
            ]
        }
    }
    return render_to_response('kas/dashboard.html', post_data, context_instance=RequestContext(request))


class KasIndex(FormView):
    template_name = 'kas/index.html'
    form_class = TransactionForm
    success_url = '/kas/index'

    post_data = {
        'title': 'Kasbeheer',
        'form': form_class
    }

    def get(self, request):
        return render_to_response(self.template_name, self.post_data, context_instance=RequestContext(request))

    def form_valid(self, form):
        transaction = form.save()
        transaction.user = self.request.user
        transaction.full_clean()
        transaction.save()

        return super(KasIndex, self).form_valid(form)


class TransactionsView(TemplateView):
    template_name = 'kas/transactions.html'

    @staticmethod
    def get_results():
        return Transaction.objects.all().order_by("-date")

    def get_context_data(self, **kwargs):
        context = super(TransactionsView, self).get_context_data(**kwargs)
        results = self.get_results()

        # Pagination
        paginator = Paginator(results, 10)
        page = self.request.GET.get('page')

        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        context.update({
            'results': transactions
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(TransactionsView, self).get(request, *args, **kwargs)
