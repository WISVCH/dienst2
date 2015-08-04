# coding: utf-8
import sys
import re
import csv
import StringIO
import traceback

from tastypie.resources import Resource
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from tastypie import fields
from django.db.models import Q
import simplejson
from tastypie.serializers import Serializer

from ldb.models import *


class CSVSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'csv']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'csv': 'text/csv',
    }

    def to_csv(self, data, options=None):
        options = options or {}

        raw_data = StringIO.StringIO()

        try:
            if len(data['objects']) < 1:
                return ""

            order = ['name', 'streetnumber', 'postcodecity', 'kixcode', 'street_name', 'house_number', 'address_2',
                     'address_3', 'postcode', 'city', 'country', 'email', 'phone_fixed', 'organization__name_prefix',
                     'organization__name', 'organization__name_short', 'organization__salutation', 'person__titles',
                     'person__initials', 'person__firstname', 'person__preposition', 'person__surname',
                     'person__postfix_titles', 'person__phone_mobile', 'person__gender', 'person__birthdate',
                     'person__ldap_username', 'person__netid', 'person__student__study', 'person__student__first_year',
                     'person__student__student_number', 'person__student__enrolled', 'person__student__phone_parents',
                     'person__alumnus__study', 'person__alumnus__study_first_year', 'person__alumnus__study_last_year',
                     'person__alumnus__work_company']

            fields = data['objects'][0].data['data'].keys()
            fields.sort(key=lambda p: order.index(p))
            header = {}
            for field in fields:
                header[field] = field

            writer = csv.DictWriter(raw_data, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)

            for obj in data.get('objects', []):
                try:
                    writer.writerow(obj.data.get('data', {}))
                except:
                    utf = {}
                    for k in obj.data['data']:
                        try:
                            utf[k] = str(obj.data['data'].get(k))
                        except:
                            utf[k] = obj.data['data'].get(k).encode('utf-8', "replace")

                    writer.writerow(utf)
            return raw_data.getvalue()
        except:
            return "Unexpected error:", sys.exc_info()[0], '\n', traceback.format_exc()

    def from_csv(self, content):
        pass


class ExportObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


# Helpers

def flatten(infile):
    output = []
    for obj in infile:
        fields = infile.get(obj)
        if obj == 'entity':
            output += fields
        else:
            for field in fields:
                output.append('%s__%s' % (obj, field))
    return output


# API Functions

class ExportResource(Resource):
    class Meta:
        allowed_methods = ['get']
        authorization = DjangoAuthorization()
        cache = SimpleCache(timeout=10)
        resource_name = 'export'
        object_class = ExportObject
        limit = 5000
        max_limit = 5000
        serializer = CSVSerializer()

    # Fields

    allowed_fields = {
        'entity': ['street_name', 'house_number', 'address_2', 'address_3', 'postcode', 'city', 'country', 'email',
                   'phone_fixed'],
        'organization': ['name_prefix', 'name', 'name_short', 'salutation'],
        'person': ['titles', 'initials', 'firstname', 'preposition', 'surname', 'postfix_titles', 'phone_mobile',
                   'gender', 'birthdate', 'ldap_username', 'netid'],
        'person__member': [],
        'person__student': ['study', 'first_year', 'student_number', 'enrolled', 'phone_parents'],
        'person__alumnus': ['study', 'study_first_year', 'study_last_year', 'work_company'],
        'person__employee': [],
    }

    def set_fields(self, query):
        export_fields = {}
        allowed_fields = flatten(self.allowed_fields)
        requested_fields = query.get("fields", "[]")
        requested_fields = simplejson.loads(str(requested_fields))

        fields = {}
        for k, v in requested_fields.iteritems():
            if v == True:
                fields[k] = v
        requested_fields = fields

        export_fields = list(set(allowed_fields) & set(requested_fields))
        if len(export_fields) == 0:
            export_fields = ['id']
        return export_fields

    # Querysets

    living_person = Q(~Q(person__isnull=True), Q(person__deceased=False))

    allowed_querysets = {
        'organizations': Q(~Q(organization__isnull=True)),
        'members': Q(living_person, Q(person__member__date_from__isnull=False),
                     Q(person__member__date_to__isnull=True) | Q(person__member__date_to__gt=date.today())),
        'merit': Q(living_person, ~Q(person__member__merit_date_from__isnull=True)),
        'honorary': Q(living_person, ~Q(person__member__honorary_date_from__isnull=True)),
        'students': Q(living_person, ~Q(person__student__isnull=True)),
        'alumni': Q(living_person, ~Q(person__alumnus__isnull=True)),
        'employees': Q(living_person, ~Q(person__employee__isnull=True))
    }

    def set_querysets(self, query):
        requested_querysets = query.get('queryset', '[]')
        requested_querysets = simplejson.loads(str(requested_querysets))

        querysets = {}
        for k, v in requested_querysets.iteritems():
            if v == True:
                querysets[k] = v
        requested_querysets = querysets

        export_querysets = list(set(self.allowed_querysets) & set(requested_querysets))
        return export_querysets

    # Filters

    allowed_filters = {
        'entity': ['country', 'machazine', 'board_invites', 'constitution_card', 'christmas_card', 'yearbook'],
        'organization': [],
        'person': ['mail_announcements', 'mail_company'],
        'person__member': ['associate_member', 'donating_member', 'merit_invitations'],
        'person__student': ['first_year', 'enrolled', 'yearbook_permission'],
        'person__alumnus': [],
        'person__employee': []
    }

    def set_filters(self, query):
        export_filters = {}
        allowed_filters = flatten(self.allowed_filters)
        requested_filters = query.get('filters', "[]")
        requested_filters = simplejson.loads(str(requested_filters))
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

    # Other
    def detail_uri_kwargs(self, bundle_or_obj):
        return {}

    # Export action
    def obj_get_list(self, bundle, **kwargs):

        get = {}
        if hasattr(bundle.request, 'GET'):
            get = bundle.request.GET.copy()

        querysets = self.set_querysets(get)

        import operator

        objects = Entity.objects.filter(reduce(operator.or_, map(lambda x: self.allowed_querysets.get(x), querysets)))

        filters = self.set_filters(get)
        objects = objects.filter(**filters)

        addresslist = get.get('addresslist', 'off')
        if addresslist == 'off':
            export_fields = self.set_fields(get)
            objects = objects.values(*export_fields)
            converted = map(ExportObject, objects)
        elif addresslist in ['doubles', 'living_with']:
            objects = objects.filter(
                ~Q(street_name=''), ~Q(house_number='')
            ).values('street_name', 'house_number', 'address_2', 'address_3', 'postcode', 'city',
                     'organization__name_prefix', 'organization__name', 'organization__name_short',
                     'organization__salutation',
                     'person__titles', 'person__initials', 'person__firstname', 'person__preposition',
                     'person__surname', 'person__postfix_titles',
                     'person__living_with', 'person__gender', 'id'
                     )

            def getname(obj):
                if obj.get('organization__name'):
                    name = obj.get('organization__name_prefix', "")
                    name += " "
                    name += obj.get('organization__name')
                    name = re.sub("\s+", " ", name)
                    return name.strip()
                elif obj.get('person__surname'):
                    titles = obj.get('person__titles')
                    if titles:
                        firstname = "%s %s" % (titles, obj.get('person__initials', obj.get('person__firstname', '')))
                    else:
                        firstname = obj.get('person__firstname', obj.get('person__initials', ''))

                    name = "%s %s %s %s" % (
                        firstname, obj.get('person__preposition', ''), obj.get('person__surname', ''),
                        obj.get('person__postfix_titles', ''))
                    name = re.sub("\s+", " ", name)
                    return name.strip()
                else:
                    return ""

            if addresslist == 'living_with':
                doubles = {}
                others = []
                for obj in objects:
                    if obj.get('person__living_with'):
                        if doubles.get(obj['person__living_with']):
                            other = doubles[obj['person__living_with']]

                            if obj.get('person__gender') == "M":
                                obj['combined_name'] = "%s en %s" % (getname(obj), getname(other))
                            else:
                                obj['combined_name'] = "%s en %s" % (getname(other), getname(obj))

                            others.append(obj)
                        else:
                            doubles[obj['id']] = obj
                    else:
                        others.append(obj)

                objects = others

            def format(obj):
                converted_obj = {}
                converted_obj['streetnumber'] = "%s %s" % (obj.get('street_name'), obj.get('house_number'))
                postcode = obj.get('postcode').replace(' ', '')
                converted_obj['postcodecity'] = "%s %s" % (postcode, obj.get('city'))
                converted_obj['kixcode'] = "%s%s" % (postcode, obj.get('house_number'))
                converted_obj['name'] = obj.get('combined_name', getname(obj))
                return ExportObject(converted_obj)

            converted = map(format, objects)
            converted.sort(key=lambda p: p.kixcode)

        return converted

    # Field

    data = fields.DictField()

    def dehydrate_data(self, bundle):
        return bundle.obj.to_dict()
