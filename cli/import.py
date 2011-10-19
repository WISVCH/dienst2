#!/usr/bin/python

import os
import sys

# This will insert the parent directory to the path so we can import the settings.
sys.path.insert(0, os.path.normpath(sys.path[0]+"/.."))

from django.core.management import setup_environ 
import settings
from settings import *
setup_environ(settings)

from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User, Permission
from ldb.models import *
import ldb.admin
import reversion
import datetime

import MySQLdb, MySQLdb.cursors

conn = MySQLdb.connect(host   = LEDEN48_HOST,
                       user   = LEDEN48_USER,
                       passwd = LEDEN48_PASSWORD,
                       db     = "leden48",
                       cursorclass=MySQLdb.cursors.DictCursor,
                       use_unicode=True)
cursor = conn.cursor()

countries = {
    'Nederland': 'NL',
    'Belgi': 'BE',
    u'Belgi\xeb': 'BE',
    'Zwitserland': 'CH',
    ' USA': 'US',
    'Verenigde Staten': 'US',
    'United Stated of America': 'US',
    'Singapore 118572': 'SG',
    'Engeland': 'UK',
    'Australia': 'AU',
    'Australia 4812': 'AU',
    'Australie': 'AU',
    'USA': 'US',
    'France': 'FR',
    'Noorwegen': 'NO',
    'Ned. Antillen': 'CW',
    u'Cura\xe7ao': 'CW',
    'Hong Kong': 'HK',
    'Spanje': 'ES',
    'Frankrijk': 'FR',
    'Oostenrijk': 'AT',
    'United Kingdom': 'GB',
    'England': 'GB',
    'Belgie': 'BE',
    'Duitsland': 'DE',
    'Maleisie': 'MY',
    'Nederlandse Antillen': 'CW',
    'Morokko': 'MA',
    'Mexico': 'MX',
    'Indonesia': 'ID',
    'Indonesie': 'ID',
    'Co. Cork, Ireland': 'IE',
    'Zweden': 'SE',
    u'M\xe9xico': 'MX',
    'Suriname': 'SR',
    'Luxemburg': 'LU',
    'Great Britain ': 'GB',
    'Nieuw-Zeeland': 'NZ',
    'New Zealand': 'NZ'
}
id_migration = {}
id_committee = {}
unknown_date = datetime.date(1,1,1)

cursor.execute("SELECT * FROM Persoon")
for k in cursor:
    print k['ID'],
    with reversion.revision:
        p = Person()

        reversion.revision.comment = 'Migration: initial'

        # Name
        p.titles         = k['Titels']
        p.initials       = k['Voorletters']
        p.firstname      = k['Voornaam']
        p.preposition    = k['Tussenvoegsels']
        p.surname        = k['Achternaam']
        p.postfix_titles = k['PostTitels']

        # Other
        p.gender = k['Geslacht']
        if k['Geboortedatum']:
            p.birthdate = k['Geboortedatum'].date()

        p.deceased = k['Overleden'] != 0

        # Subscriptions
        p.mail_announcements = k['Mailing_algemeen'] != 0
        p.mail_company       = k['Mailing_bedrijven'] != 0
        p.machazine          = k['Machazine'] != 0

        p.ldap_username = k['Username']
        p.comment = k['Opmerkingen']

        if k['Adres_controledatum']:
            p.comment += '\nLegacy address checked: ' \
                       + k['Adres_controledatum'].strftime('%Y-%m-%d')

        # Adress
        if 'INTERN' in k['Postcode']:
            p.street_name = k['Adres']
            p.postcode    = 'INTERN'
        else:
            if len(k['Adres'].split(' ')[-1]) <= 7:
                p.street_name = ' '.join(k['Adres'].split(' ')[0:-1])
                p.house_number = k['Adres'].split(' ')[-1]
            else:
                p.street_name = k['Adres']
            if k['Land'] == 'Co. Cork, Ireland':
                p.address_2 = 'Co. Cork'
            p.postcode = k['Postcode']
            p.city     = k['Plaats']
        p.country  = countries[k['Land']] if k['Land'] else 'NL'
        p.email    = k['Email']

        # Telephone
        p.phone_fixed  = k['Telefoonnummer']
        p.phone_mobile = k['Mobiel_telefoonnummer']

        p.save()

    with reversion.revision:
        if k['Adres_correct'] == 0:
            print '(incorrect)',
            p.set_address_incorrect()
            p.save()
            reversion.revision.comment = 'Migration: address incorrect'

    print 'migrated to %04d - %s' % (p.id, p)
    id_migration[k['ID']] = p.id

    with reversion.revision:
        c2 = conn.cursor()
        c2.execute("SELECT * FROM Student WHERE ID_persoon=%d" % int(k['ID']))
        l = c2.fetchone()

        if l:
            q = Student()
            q.person = p
            if l['Studienummer']:
                q.student_number  = l['Studienummer']
            q.first_year          = l['TUinschrijfjaar']
            q.study               = l['Studierichting']
            q.telephone_parents   = l['TelefoonOuders']
            q.yearbook_permission = l['JaarboekToestemming'] != 0
            q.graduated           = l['Afgestudeerd'] != 0
            q.save()

        c2.execute("SELECT * FROM Lid WHERE ID_persoon=%d" % int(k['ID']))
        m = c2.fetchone()

        if m:
            r = Member()
            r.person = p
            if m['Inschrijfdatum']:
                r.date_from = m['Inschrijfdatum'].date()
            else:
                r.date_from = unknown_date
            if m['Betaaldatum']:
                r.date_paid = m['Betaaldatum'].date()
            r.amount_paid = m['Bedrag']
            if 'Lidtype' in m:
                r.associate_member = m['Lidtype'] == 'BGL'
                r.donating_member  = m['Lidtype'] == 'DON'
            r.save()

        c2.execute("SELECT * FROM LidAf WHERE ID_persoon=%d" % int(k['ID']))
        n = c2.fetchone()

        if n:
            r = Member()
            r.person = p
            if n['Inschrijfdatum']:
                r.date_from = n['Inschrijfdatum'].date()
            else:
                r.date_from = unknown_date
            if n['DatumLidAf']:
                r.date_to = n['DatumLidAf'].date()
            else:
                r.date_to = unknown_date
            if n['Betaaldatum']:
                r.date_paid = n['Betaaldatum'].date()
            r.amount_paid = n['Bedrag']
            if 'Lidtype' in n:
                r.associate_member = n['Lidtype'] == 'BGL'
                r.donating_member  = n['Lidtype'] == 'DON'
            p.comment += '\nLegacy reden lid af: ' + n['RedenLidAf']
            r.save()

        c2.execute("SELECT * FROM Medewerker WHERE ID_persoon=%d" % int(k['ID']))
        o = c2.fetchone()

        if o:
            s = Employee()
            s.person = p

            s.faculty        = o['Faculteit']
            s.department     = o['Afdeling']
            s.function       = o['Functie']
            s.phone_internal = o['Telefoonnummer_TU'][-5:]
            s.save()

        c2.execute("SELECT * FROM Alumnus WHERE ID_persoon=%d" % int(k['ID']))
        q = c2.fetchone()

        if q:
            t = Alumnus()
            t.person = p
            t.study                = q['Study']
            t.study_first_year     = q['StudyFirstYear']
            t.study_last_year      = q['StudyLastYear']
            t.study_research_group = q['StudyResearchGroup']
            t.study_paper          = q['StudyPaper']
            t.study_professor      = q['StudyProfessor']
            t.work_company         = q['WorkCompany']
            t.work_position        = q['WorkPosition']
            t.work_sector          = q['WorkType']
            p.yearbook             = q['Jaarboek'] != 0

            if q['Interests']:
                p.comment += '\nLegacy alumnus interests: ' + q['Interests']

            t.save()

        c2.execute("SELECT * FROM LVV_ERE WHERE ID_persoon=%d" % int(k['ID']))
        u = c2.fetchone()

        if u:
            if m['Lidtype'] == 'LVV':
                if u['Datum_benoeming']:
                    r.merit_date_from = u['Datum_benoeming'].date()
                else:
                    r.merit_date_from = unknown_date
                r.merit_invitations = u['Benaderbaar'] != 0

            if m['Lidtype'] == 'ERE':
                if u['Datum_benoeming']:
                    r.honorary_date_from = u['Datum_benoeming'].date()
                else:
                    r.honorary_date_from = unknown_date

            r.merit_history = u['Geschiedenis']

            if u['Datum_aanvaard']:
                p.comment += '\nLegacy LvV datum aanvaard: ' \
                           + u['Datum_aanvaard'].strftime('%Y-%m-%d')
            r.save()
        elif m and m['Lidtype'] and m['Lidtype'] == 'LVV': # Yes, 3 of those
            r.merit_date_from = unknown_date

            r.save()
        reversion.revision.comment = 'Migration: additional properties'
        p.save()

        c2.execute("SELECT * FROM CommissieLeden c INNER JOIN Afdeling a ON (a.ID=c.ID_commissie) WHERE c.ID_persoon=%d" % int(k['ID']))
        for s in c2:
            if not s['ID_commissie'] in id_committee:
                committee = Committee()
                committee.name = s['Naam']
                committee.description = s['Omschrijving']
                committee.save()
                cid = committee.id
                id_committee[s['ID_commissie']] = cid
            else:
                cid = id_committee[s['ID_commissie']]

            # try: p.member
            # except:
            #     r = Member()
            #     r.person = p
            #     r.date_from = unknown_date
            #     r.date_to = unknown_date
            #     r.save()
            
            cm              = CommitteeMembership()
            cm.person       = p
            cm.committee_id = cid
            cm.board        = s['Jaargang'] - 1957 # Convert to board number instead of year
            cm.position     = s['Functie']
            cm.save()

cursor = conn.cursor()
cursor.execute("SELECT * FROM Persoon WHERE Samenwonen <> 0")
for k in cursor:
    person_id = id_migration[k['ID']]
    person    = Person.objects.get(pk=person_id)

    other_id  = id_migration[k['Samenwonen_link']]
    other     = Person.objects.get(pk=other_id)

    print '%s & %s' % (person, other)
    with reversion.revision:
        if other.street_name  != person.street_name or \
           other.house_number != person.house_number or \
           other.address_2    != person.address_2 or \
           other.postcode     != person.postcode or \
           other.city         != person.city or \
           other.country      != person.country:
            print k['ID'] + k['Samenwonen_link'],
            print 'addresses are different; not setting as living together'
            person.comment += '\nLegacy samenwonend met ' + str(other)
        else:
            person.living_with = other

        reversion.revision.comment = 'Migration: lives together'
        person.save()

print '\n\nInstanties'

cursor = conn.cursor()
cursor.execute("SELECT * FROM Instantie")
for k in cursor:
    print k['ID'],
    o                    = Organization()
    o.name_prefix        = k['AanhefAdres']
    o.name               = k['Naam']
    o.name_short         = k['NaamKort']
    o.salutation         = k['AanhefBrief']
    
    # Adress
    if len(k['Adres'].split(' ')[-1]) <= 7:
        o.street_name    = ' '.join(k['Adres'].split(' ')[0:-1])
        o.house_number   = k['Adres'].split(' ')[-1]
    else:
        o.street_name    = k['Adres']
    o.postcode           = 'INTERN' if k['Intern'] != 0 else k['Postcode']
    o.city               = k['Plaats']
    o.country            = countries[k['Land']] if k['Land'] else 'NL'
    o.email              = k['Email']
    
    # Telephone
    o.phone_fixed        = k['Telefoonnummer']
    
    # Subscriptions
    o.machazine          = k['MaCHazine'] != 0
    o.board_invites      = k['UitnodigingWisseling'] != 0
    o.constitution_card  = k['Constitutiekaartje'] != 0
    o.christmas_card     = k['Kerstkaartje'] != 0
    o.yearbook           = False
    
    o.save()
    print 'migrated to %04d - %s' % (o.id, o)
