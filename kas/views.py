from __future__ import unicode_literals

from django.views.generic import TemplateView


class AngularIndexView(TemplateView):
    template_name = 'kas/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AngularIndexView, self).get_context_data(**kwargs)
        context.update(**{
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
        })

        return context
