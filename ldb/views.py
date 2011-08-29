from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.template.context import RequestContext
from haystack.query import SearchQuerySet
from ldb.models import Person, Member
from ldb.forms import *
from form_utils.forms import BetterModelForm
from djangorestframework.views import View
from djangorestframework.response import Response
from djangorestframework import status
import time

class OrganizationDetailView(DetailView):
    context_object_name = 'organization'
    model = Organization

class OrganizationDeleteView(DeleteView):
    context_object_name = 'organization'
    model = Organization
    success_url = '/'

def organization_edit(request, pk=None):
    data = {}
    if pk:
        organization = Organization.objects.get(pk=pk)
    else:
        organization = Organization()
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            person = form.save()
            return HttpResponseRedirect(reverse('ldb_organizations_detail', args=(organization.id,)))
    else:
        form = OrganizationForm(instance=organization)
    data['form'] = form
    return render_to_response('ldb/organization_form.html', data,
                              context_instance = RequestContext(request))

class PersonDetailView(DetailView):
    context_object_name = 'person'
    model = Person
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        # Fetch committee memberships
        try:
            context['committee_memberships'] = self.get_object().committeemembership_set.order_by('-board').all()
        except:
            pass
        return context

class PersonDeleteView(DeleteView):
    context_object_name = 'person'
    model = Person
    success_url = '/'

def person_edit(request, pk=None):
    data = {}
    if pk:
        person = Person.objects.get(pk=pk)
    else:
        person = Person()
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        member_formset = MemberFormSet(request.POST, instance=person)
        student_formset = StudentFormSet(request.POST, instance=person)
        alumnus_formset = AlumnusFormSet(request.POST, instance=person)
        employee_formset = EmployeeFormSet(request.POST, instance=person)
        committeemembership_formset = CommitteeMembershipFormSet(request.POST, instance=person)
        if form.is_valid() and \
           member_formset.is_valid() and \
           student_formset.is_valid() and \
           alumnus_formset.is_valid and \
           employee_formset.is_valid() and \
           committeemembership_formset.is_valid():
            person = form.save()

            member_form = member_formset.forms[0]
            if member_form.has_changed():
                member = member_form.save(commit=False)
                member.person = person
                member.save()

            student_form = student_formset.forms[0]
            if student_form.has_changed():
                student = student_form.save(commit=False)
                student.person = person
                student.save()

            alumnus_form = alumnus_formset.forms[0]
            if alumnus_form.has_changed():
                alumnus = alumnus_form.save(commit=False)
                alumnus.person = person
                alumnus.save()

            employee_form = employee_formset.forms[0]
            if employee_form.has_changed():
                employee = employee_form.save(commit=False)
                employee.person = person
                employee.save()

            for form in committeemembership_formset.forms:
                if form.has_changed():
                    committeemembership = form.save(commit=False)
                    committeemembership.person = person
                    committeemembership.save()
            return HttpResponseRedirect(reverse('ldb_people_detail', args=(person.id,)))
    else:
        form = PersonForm(instance=person)
        member_formset = MemberFormSet(instance=person)
        student_formset = StudentFormSet(instance=person)
        alumnus_formset = AlumnusFormSet(instance=person)
        employee_formset = EmployeeFormSet(instance=person)
        committeemembership_formset = CommitteeMembershipFormSet(instance=person)
    data['form'] = form
    data['member_formset'] = member_formset
    data['student_formset'] = student_formset
    data['alumnus_formset'] = alumnus_formset
    data['employee_formset'] = employee_formset
    data['committeemembership_formset'] = committeemembership_formset
    return render_to_response('ldb/person_form.html', data,
                              context_instance = RequestContext(request))

def index(request):
    data = {}
    return render_to_response( 'ldb/index.html', data,
                               context_instance = RequestContext(request))

def ajax_people_search(request):
    # if request.is_ajax():
    q = request.GET.get('q')
    if q is not None:
        results    = SearchQuerySet().auto_query(q)
        # suggestion = results.spelling_suggestion()
        template   = 'ldb/results.html'
        data       = {'results': results[:10], 'count': len(results), 'remainder': len(results)-10}
        return render_to_response( template, data,
                                   context_instance = RequestContext(request))
    # else:
        # return redirect('index')
