from django.db.models import Q,Count
from ldb.models import Member, Entity, Person, Organization, Committee, CommitteeMembership

import re
import xlwt
import datetime

# Mailing lists

def persons_announcements():
	return Person.objects.all().filter(
		Q(deceased=False),
		Q(Q(member__date_from__isnull=False), Q(member__date_to__isnull=True)),
		Q(mail_announcements=True)
	)

def persons_company():
	return Person.objects.all().filter(
		Q(deceased=False),
		Q(Q(member__date_from__isnull=False), Q(member__date_to__isnull=True)),
		Q(mail_company=True)
	)

def persons_all():
	return Person.objects.all().filter(
		Q(country='NL',deceased=False),
		Q(Q(member__date_from__isnull=False), Q(member__date_to__isnull=True) )| 
		~Q(member__merit_date_from__isnull=True) | 
		~Q(member__honorary_date_from__isnull=True) |
		~Q(alumnus__isnull=True) |
		~Q(employee__isnull=True)
	)

def organizations_all():
	return Organization.objects.all().filter(
		Q(country='NL')
	)

def merge_persons_organizations(persons, organizations):
    items = []

    for person in persons:
        items.append(person)

    for organization in organizations:
        items.append(organization)

    return items

def all_machazine():
	return merge_persons_organizations(persons_all().filter(Q(machazine=True)), organizations_all().filter(Q(machazine=True)))

def all_christmas():
	return merge_persons_organizations(persons_all().filter(Q(christmas_card=True)), organizations_all().filter(Q(christmas_card=True)))

def all_constitution():
	year = (datetime.datetime.now() - datetime.datetime(1957, 3, 6)).days / 365 + 1

	return merge_persons_organizations(
		persons_all().filter(Q(constitution_card=True)) | 
		oudbestuurdersvanaf(year-8), 
		organizations_all().filter(Q(constitution_card=True))
		)

	return year

def oudbestuurdersvanaf(year):
	board = Committee.objects.get(name="Bestuur")
	return Person.objects.all().filter(
		Q(deceased=False),
		Q(committeemembership__committee=board),
		Q(committeemembership__board__gt=year-1)
	).order_by('committeemembership__board').reverse()

def lvvers():
	return persons_all().filter(~Q(member__merit_date_from__isnull=True) | ~Q(member__honorary_date_from__isnull=True))

def alumni():
	return persons_all().filter(~Q(alumnus__isnull=True))

def persons_constitutioncard():
	return Person.objects.all().filter(
		Q(deceased=False),
		Q(constitution_card=True)
	)

def organizations_constitutioncard():
	return Organization.objects.all().filter(
		Q(constitution_card=True)
	)

def mailingitem(item):
	return [item.email]

def addressitem(item):
	if type(item) == Person:
		if item.initials is None:
			init = item.firstname
		else:
			init = item.initials

		return [
			"",
			re.sub(' +', ' ', item.titles + " " + init + " " + item.preposition + " " + item.surname + " " + item.postfix_titles).strip(),
			re.sub(' +', ' ', item.street_name + " " + item.house_number), 
			re.sub(' +', '', item.postcode) + " " + item.city,
			re.sub(' +', '', item.postcode) + item.house_number,
			item.country,
			]
	elif type(item) == Organization:
		return [
			item.name_prefix,
			item.name,
			re.sub(' +', ' ', item.street_name + " " + item.house_number), 
			re.sub(' +', '', item.postcode) + " " + item.city,
			re.sub(' +', '', item.postcode) + item.house_number,
			item.country,
			]
	else:
		return []

def fullitem(item):
	if type(item) == Person:
		return [
			item.titles, 
			item.initials, 
			item.firstname, 
			item.preposition, 
			item.surname, 
			item.postfix_titles, 

			item.street_name, 
			item.house_number, 
			re.sub(' +', '', item.postcode),
			item.city,
			item.country,
			item.email
			]
	elif type(item) == Organization:
		return [
			"", 
			"", 
			item.name_prefix, 
			"", 
			item.name, 
			"", 

			item.street_name, 
			item.house_number, 
			re.sub(' +', '', item.postcode),
			item.city,
			item.country,
			item.email
			]
	else:
		return []