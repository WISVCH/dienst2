from functools import reduce

from django.db.models import Prefetch, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView, DeleteView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView

from itertools import chain

from ldb.filters import CommitteeMembershipFilter
from ldb.forms import (
    PersonForm,
    MemberFormSet,
    StudentFormSet,
    AlumnusFormSet,
    EmployeeFormSet,
    CommitteeMembershipFormSet,
)
from ldb.models import Organization, Person, CommitteeMembership


class IndexView(TemplateView):
    template_name = "ldb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ledenadministratie"
        return context


class ResultsView(TemplateView):
    template_name = "ldb/results.html"

    def get_results(self):
        q = self.request.GET.get("q")
        if q is not None:
            q = q.strip().split()

            person_filters = Q()
            organization_filters = Q()
            for word in q:
                person_filters &= (
                    Q(firstname__icontains=word)
                    | Q(preposition__icontains=word)
                    | Q(surname__icontains=word)
                    | Q(ldap_username__icontains=word)
                    | Q(street_name__icontains=word)
                    | Q(email__icontains=word)
                )
                organization_filters &= Q(name__icontains=word)

            person_qs = Person.objects.filter(person_filters)
            organization_qs = Organization.objects.filter(organization_filters)

            count = person_qs.count() + organization_qs.count()
            return list(chain(person_qs[:30], organization_qs[:30])), count
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results, count = self.get_results()
        context.update(
            {
                "results": results,
                "count": count,
                "remainder": count - 60,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return super().get(request, *args, **kwargs)
        else:
            return redirect("ldb_index")


class OrganizationDetailView(DetailView):
    context_object_name = "organization"
    model = Organization


class OrganizationDeleteView(DeleteView):
    context_object_name = "organization"
    model = Organization
    success_url = "/"


class OrganizationEditView(UpdateView):
    model = Organization
    fields = "__all__"

    def get_object(self, **kwargs):
        try:
            return super().get_object(**kwargs)
        except AttributeError:
            return None


class PersonDetailView(DetailView):
    context_object_name = "person"
    model = Person

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("member", "student", "alumnus", "employee")
        qs = qs.prefetch_related(
            Prefetch(
                "committee_memberships",
                queryset=CommitteeMembership.objects.order_by(
                    "-board"
                ).prefetch_related("committee"),
            )
        )
        return qs


class PersonDeleteView(DeleteView):
    context_object_name = "person"
    model = Person
    success_url = "/"


class PersonEditView(SingleObjectMixin, TemplateView):
    model = Person
    template_name = "ldb/person_form.html"

    def get_form_kwargs(self):
        kwargs = {}

        if self.request.method in ("POST", "PUT"):
            kwargs.update({"data": self.request.POST, "files": self.request.FILES})

        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})

        return kwargs

    def get_forms(self):
        return {
            "form": PersonForm(**self.get_form_kwargs()),
            "member_formset": MemberFormSet(**self.get_form_kwargs()),
            "student_formset": StudentFormSet(**self.get_form_kwargs()),
            "alumnus_formset": AlumnusFormSet(**self.get_form_kwargs()),
            "employee_formset": EmployeeFormSet(**self.get_form_kwargs()),
            "committeemembership_formset": CommitteeMembershipFormSet(
                **self.get_form_kwargs()
            ),
        }

    def are_forms_valid(self, forms):
        return reduce(
            lambda form_valid, valid: valid and form_valid,
            [form.is_valid() for form in forms.values()],
            True,
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
        form = forms.pop("form")
        person = form.save()

        for formset in forms.values():
            for form in formset.forms:
                if form.has_changed():
                    obj = form.save(commit=False)
                    obj.person = person
                    obj.save()

        # Save person again to set the right membership_status
        person.save()

        return HttpResponseRedirect(person.get_absolute_url())

    def get_object(self, **kwargs):
        try:
            return super().get_object(**kwargs)
        except AttributeError:
            return None


class CommitteeMembershipFilterView(FilterView):
    filterset_class = CommitteeMembershipFilter
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        self.object_list = (
            self.filterset.qs.select_related("person")
            .prefetch_related("committee")
            .order_by("-board", "committee__name", "person__firstname")
        )
        context = self.get_context_data(
            filter=self.filterset, object_list=self.object_list
        )
        return self.render_to_response(context)
