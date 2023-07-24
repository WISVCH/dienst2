import csv
import operator
import re
from functools import reduce
from io import StringIO

from datetime import date
from django.db.models import Q
from django.utils.encoding import smart_str
from rest_framework import renderers, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ldb.models import Entity


class CSVRenderer(renderers.BaseRenderer):
    media_type = "text/csv"
    format = "csv"

    def render(self, data, media_type=None, renderer_context=None):
        if not isinstance(data, list):
            return data

        if len(data) < 1:
            return "Geen resultaten"

        order = [
            "name",
            "streetnumber",
            "postcodecity",
            "kixcode",
            "street_name",
            "house_number",
            "address_2",
            "address_3",
            "postcode",
            "city",
            "country",
            "email",
            "phone_fixed",
            "organization__name_prefix",
            "organization__name",
            "organization__name_short",
            "organization__salutation",
            "person__titles",
            "person__initials",
            "person__firstname",
            "person__preposition",
            "person__surname",
            "person__postfix_titles",
            "person__phone_mobile",
            "person__gender",
            "person__pronouns",
            "person__birthdate",
            "person__email_forward",
            "person__ldap_username",
            "person__google_username",
            "person__netid",
            "person__student__study",
            "person__student__first_year",
            "person__student__student_number",
            "person__student__enrolled",
            "person__student__emergency_name",
            "person__student__emergency_phone",
            "person__alumnus__study",
            "person__alumnus__study_first_year",
            "person__alumnus__study_last_year",
            "person__alumnus__work_company",
            "id",
        ]

        fields = list(data[0]._data.keys())
        fields.sort(key=lambda p: order.index(p))

        raw_data = StringIO()
        writer = csv.DictWriter(raw_data, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for obj in data:
            writer.writerow({k: smart_str(v) for k, v in obj._data.items()})
        return raw_data.getvalue()


class ExportObject:
    def __init__(self, initial=None):
        self.__dict__["_data"] = {}

        if hasattr(initial, "items"):
            self.__dict__["_data"] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__["_data"][name] = value

    def to_dict(self):
        return self._data


def flatten(infile):
    output = []
    for obj in infile:
        fields = infile.get(obj)
        if obj == "entity":
            output += fields
        else:
            for field in fields:
                output.append("{}__{}".format(obj, field))
    return output


class Export(APIView):
    renderer_classes = (TemplateHTMLRenderer, CSVRenderer)

    def get(self, request):
        data = {"title": "Ledendatabase", "ng_app": "ldb"}
        return Response(data, template_name="ldb/export.html")

    # Fields
    allowed_fields = {
        "entity": [
            "street_name",
            "house_number",
            "address_2",
            "address_3",
            "postcode",
            "city",
            "country",
            "email",
            "phone_fixed",
        ],
        "organization": ["name_prefix", "name", "name_short", "salutation"],
        "person": [
            "titles",
            "initials",
            "firstname",
            "preposition",
            "surname",
            "postfix_titles",
            "phone_mobile",
            "gender",
            "pronouns",
            "birthdate",
            "email_forward",
            "ldap_username",
            "google_username",
            "netid",
        ],
        "person__member": [],
        "person__student": [
            "study",
            "first_year",
            "student_number",
            "enrolled",
            "emergency_name",
            "emergency_phone",
        ],
        "person__alumnus": [
            "study",
            "study_first_year",
            "study_last_year",
            "work_company",
        ],
        "person__employee": [],
    }

    def set_fields(self, query):
        allowed_fields = flatten(self.allowed_fields)
        requested_fields = query.get("fields", [])

        fields = {}
        for k, v in requested_fields.items():
            if v:
                fields[k] = v
        requested_fields = fields

        export_fields = list(set(allowed_fields) & set(requested_fields))
        if len(export_fields) == 0:
            export_fields = ["id"]
        return export_fields

    # Querysets
    living_person = Q(~Q(person__isnull=True), Q(person__deceased=False))
    allowed_querysets = {
        "organizations": Q(~Q(organization__isnull=True)),
        "members": Q(
            living_person,
            Q(person__member__date_from__isnull=False),
            Q(person__member__date_to__isnull=True)
            | Q(person__member__date_to__gt=date.today()),
        ),
        "merit": Q(living_person, ~Q(person__member__merit_date_from__isnull=True)),
        "honorary": Q(
            living_person, ~Q(person__member__honorary_date_from__isnull=True)
        ),
        "students": Q(living_person, ~Q(person__student__isnull=True)),
        "alumni": Q(living_person, ~Q(person__alumnus__isnull=True)),
        "employees": Q(living_person, ~Q(person__employee__isnull=True)),
    }

    def set_querysets(self, query):
        requested_querysets = query.get("queryset", [])

        querysets = {}
        for k, v in requested_querysets.items():
            if v is True:
                querysets[k] = v
        requested_querysets = querysets

        export_querysets = list(set(self.allowed_querysets) & set(requested_querysets))
        return export_querysets

    # Filters
    allowed_filters = {
        "entity": [
            "country",
            "machazine",
        ],
        "organization": [],
        "person": ["mail_announcements", "mail_company", "mail_education"],
        "person__member": ["associate_member", "donating_member", "merit_invitations"],
        "person__student": ["first_year", "enrolled"],
        "person__alumnus": [],
        "person__employee": [],
    }

    def set_filters(self, query):
        export_filters = {}
        allowed_filters = flatten(self.allowed_filters)
        requested_filters = query.get("filters", [])
        for field in requested_filters:
            if field in allowed_filters:
                value = requested_filters.get(field)
                if value == "true":
                    export_filters[field] = True
                elif value == "false":
                    export_filters[field] = False
                elif value != "undefined":
                    export_filters[field] = value
        return export_filters

    def post(self, request):
        querysets = self.set_querysets(request.data)

        if not querysets:
            return Response("No groups selected", status=status.HTTP_400_BAD_REQUEST)

        objects = Entity.objects.filter(
            reduce(
                operator.or_, map(lambda x: self.allowed_querysets.get(x), querysets)
            )
        )
        filters = self.set_filters(request.data)
        objects = objects.filter(**filters)

        addresslist = request.data.get("addresslist", "off")
        if addresslist == "off":
            export_fields = self.set_fields(request.data)
            objects = objects.values(*export_fields)
            converted = list(map(ExportObject, objects))
        elif addresslist in ["doubles", "living_with"]:
            objects = objects.filter(~Q(street_name=""), ~Q(house_number="")).values(
                "street_name",
                "house_number",
                "address_2",
                "address_3",
                "postcode",
                "city",
                "organization__name_prefix",
                "organization__name",
                "organization__name_short",
                "organization__salutation",
                "person__titles",
                "person__initials",
                "person__firstname",
                "person__preposition",
                "person__surname",
                "person__postfix_titles",
                "person__living_with",
                "person__gender",
                "person__pronouns",
                "id",
            )

            def getname(obj):
                if obj.get("organization__name"):
                    name = obj.get("organization__name_prefix", "")
                    name += " "
                    name += obj.get("organization__name")
                    name = re.sub(r"\s+", " ", name)
                    return name.strip()
                elif obj.get("person__surname"):
                    titles = obj.get("person__titles")
                    if titles:
                        firstname = "{} {}".format(
                            titles,
                            obj.get(
                                "person__initials", obj.get("person__firstname", "")
                            ),
                        )
                    else:
                        firstname = obj.get(
                            "person__firstname", obj.get("person__initials", "")
                        )

                    name = "{} {} {} {}".format(
                        firstname,
                        obj.get("person__preposition", ""),
                        obj.get("person__surname", ""),
                        obj.get("person__postfix_titles", ""),
                    )
                    name = re.sub(r"\s+", " ", name)
                    return name.strip()
                else:
                    return ""

            if addresslist == "living_with":
                doubles = {}
                others = []
                for obj in objects:
                    if obj.get("person__living_with"):
                        if doubles.get(obj["person__living_with"]):
                            other = doubles[obj["person__living_with"]]

                            obj["combined_name"] = "{} en {}".format(
                                getname(obj),
                                getname(other),
                            )

                            others.append(obj)
                        else:
                            doubles[obj["id"]] = obj
                    else:
                        others.append(obj)

                objects = others

            def format(obj):
                converted_obj = {}
                converted_obj["streetnumber"] = "{} {}".format(
                    obj.get("street_name"),
                    obj.get("house_number"),
                )
                postcode = obj.get("postcode").replace(" ", "")
                converted_obj["postcodecity"] = "{} {}".format(
                    postcode, obj.get("city")
                )
                converted_obj["kixcode"] = "{}{}".format(
                    postcode, obj.get("house_number")
                )
                converted_obj["name"] = obj.get("combined_name", getname(obj))
                return ExportObject(converted_obj)

            converted = list(map(format, objects))
            converted.sort(key=lambda p: p.kixcode)

        return Response(converted)
