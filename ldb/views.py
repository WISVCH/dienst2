from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import DetailView, DeleteView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
from haystack.query import SQ

from dienst2.extras import convert_free_search
from ldb.forms import PersonForm, MemberFormSet, StudentFormSet, AlumnusFormSet, EmployeeFormSet, \
    CommitteeMembershipFormSet
from ldb.models import Organization, Person, CommitteeMembership


def index(request):
    post_data = {
        'title': 'Ledendatabase',
        'ng_app': 'ldb',
        'navbar': {
            'title': 'Ledendatabase',
            'items': [
                (reverse('ldb_index'), 'Zoeken'),
                (reverse('ldb_people_create'), 'Nieuw Persoon'),
                (reverse('ldb_organizations_create'), 'Nieuwe Organisatie'),
                ('#/committees', 'Commissies'),
                ('#/export', 'Exporteren')
            ]
        }
    }

    if request.user.has_module_perms('admin'):
        post_data['navbar']['items'].append((reverse('admin:ldb_person_changelist'), "Beheer"))

    return render_to_response('ldb/dashboard.html', post_data, context_instance=RequestContext(request))


def index_old(request):
    data = {
        'title': 'Ledenadministratie'
    }
    return render_to_response('ldb/index.html', data,
                              context_instance=RequestContext(request))


class ResultsView(TemplateView):
    template_name = 'ldb/results.html'

    def get_results(self):
        q = self.request.GET.get('q')
        if q is not None:
            search_term = convert_free_search(q)
            return SearchQuerySet().models(Person, Organization).filter(
                SQ(text=Raw(search_term)) |
                SQ(name=Raw(search_term)) |
                SQ(address=Raw(search_term)) |
                SQ(contact=Raw(search_term)) |
                SQ(ldap_username=Raw(search_term))
            )
        return []

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        results = self.get_results()
        context.update({
            'results': results[:10],
            'count': len(results),
            'remainder': len(results) - 10,
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(ResultsView, self).get(request, *args, **kwargs)
        else:
            return redirect('ldb_index')


class OrganizationDetailView(DetailView):
    context_object_name = 'organization'
    model = Organization


class OrganizationDeleteView(DeleteView):
    context_object_name = 'organization'
    model = Organization
    success_url = '/'


class OrganizationEditView(UpdateView):
    model = Organization
    fields = '__all__'

    def get_object(self, **kwargs):
        try:
            return super(OrganizationEditView, self).get_object(**kwargs)
        except AttributeError:
            return None


class PersonDetailView(DetailView):
    context_object_name = 'person'
    model = Person

    def get_queryset(self):
        qs = super(PersonDetailView, self).get_queryset()
        qs = qs.select_related('member', 'student', 'alumnus', 'employee')
        qs = qs.prefetch_related(
            Prefetch(
                'committee_memberships',
                queryset=CommitteeMembership.objects.order_by('-board').prefetch_related('committee')
            ))
        return qs


class PersonDeleteView(DeleteView):
    context_object_name = 'person'
    model = Person
    success_url = '/'


class PersonEditView(SingleObjectMixin, TemplateView):
    model = Person
    template_name = 'ldb/person_form.html'

    def get_form_kwargs(self):
        kwargs = {}

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        return kwargs

    def get_forms(self):
        return {
            'form': PersonForm(**self.get_form_kwargs()),
            'member_formset': MemberFormSet(**self.get_form_kwargs()),
            'student_formset': StudentFormSet(**self.get_form_kwargs()),
            'alumnus_formset': AlumnusFormSet(**self.get_form_kwargs()),
            'employee_formset': EmployeeFormSet(**self.get_form_kwargs()),
            'committeemembership_formset': CommitteeMembershipFormSet(**self.get_form_kwargs())
        }

    def are_forms_valid(self, forms):
        return reduce(
            lambda form_valid, valid: valid and form_valid,
            [form.is_valid() for form in forms.values()],
            True
        )

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        forms = self.get_forms()
        return self.render_to_response(self.get_context_data(**forms))

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        forms = self.get_forms()

        if self.are_forms_valid(forms):
            return self.forms_valid(forms)
        else:
            return self.render_to_response(self.get_context_data(**forms))

    def forms_valid(self, forms):
        form = forms.pop('form')
        person = form.save()

        for formset in forms.values():
            for form in formset.forms:
                if form.has_changed():
                    obj = form.save(commit=False)
                    obj.person = person
                    obj.save()

        return HttpResponseRedirect(person.get_absolute_url())

    def get_object(self, **kwargs):
        try:
            return super(PersonEditView, self).get_object(**kwargs)
        except AttributeError:
            return None
