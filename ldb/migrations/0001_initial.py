# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ldb.country_field
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'committee',
                'verbose_name_plural': 'committees',
            },
        ),
        migrations.CreateModel(
            name='CommitteeMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('board', models.IntegerField(verbose_name='board')),
                ('position', models.CharField(max_length=50, verbose_name='position', blank=True)),
                ('ras_months', models.IntegerField(null=True, verbose_name='RAS months', blank=True)),
                ('committee', models.ForeignKey(to='ldb.Committee')),
            ],
            options={
                'verbose_name': 'committee membership',
                'verbose_name_plural': 'committee memberships',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street_name', models.CharField(max_length=75, verbose_name='street name', blank=True)),
                ('house_number', models.CharField(max_length=7, verbose_name='house number', blank=True)),
                ('address_2', models.CharField(max_length=75, verbose_name='address row 2', blank=True)),
                ('address_3', models.CharField(max_length=75, verbose_name='address row 3', blank=True)),
                ('postcode', models.CharField(max_length=10, verbose_name='postcode', blank=True)),
                ('city', models.CharField(max_length=50, verbose_name='city', blank=True)),
                ('country', ldb.country_field.CountryField(blank=True, max_length=2, verbose_name='country', choices=[(b'AF', 'Afghanistan'), (b'AX', '\xc5landseilanden'), (b'AL', 'Albani\xeb'), (b'DZ', 'Algerije'), (b'AS', 'Amerikaans-Samoa'), (b'AD', 'Andorra'), (b'AO', 'Angola'), (b'AI', 'Anguilla'), (b'AQ', 'Antarctica'), (b'AG', 'Antigua en Barbuda'), (b'AR', 'Argentini\xeb'), (b'AM', 'Armeni\xeb'), (b'AW', 'Aruba'), (b'AU', 'Australi\xeb'), (b'AT', 'Oostenrijk'), (b'AZ', 'Azerbeidzjan'), (b'BS', "Bahama's"), (b'BH', 'Bahrein'), (b'BD', 'Bangladesh'), (b'BB', 'Barbados'), (b'BY', 'Wit-Rusland / Belarus'), (b'BE', 'Belgi\xeb'), (b'BZ', 'Belize'), (b'BJ', 'Benin'), (b'BM', 'Bermuda'), (b'BT', 'Bhutan'), (b'BO', 'Bolivia, Plurinationale Staat'), (b'BQ', 'Bonaire, Sint Eustatius en Saba'), (b'BA', 'Bosni\xeb en Herzegovina'), (b'BW', 'Botswana'), (b'BV', 'Bouvet'), (b'BR', 'Brazili\xeb'), (b'IO', 'Brits Territorium in de Indische Oceaan'), (b'BN', 'Brunei'), (b'BG', 'Bulgarije'), (b'BF', 'Burkina Faso'), (b'BI', 'Burundi'), (b'KH', 'Cambodja'), (b'CM', 'Kameroen'), (b'CA', 'Canada'), (b'CV', 'Kaap Verde'), (b'KY', 'Kaaimaneilanden'), (b'CF', 'Centraal-Afrikaanse Republiek'), (b'TD', 'Tsjaad'), (b'CL', 'Chili'), (b'CN', 'China'), (b'CX', 'Christmaseiland'), (b'CC', 'Cocoseilanden'), (b'CO', 'Colombia'), (b'KM', 'Comoren'), (b'CG', 'Congo-Brazzaville'), (b'CD', 'Congo-Kinshasa'), (b'CK', 'Cookeilanden'), (b'CR', 'Costa Rica'), (b'CI', 'Ivoorkust'), (b'HR', 'Kroati\xeb'), (b'CU', 'Cuba'), (b'CW', 'Cura\xe7ao'), (b'CY', 'Cyprus'), (b'CZ', 'Tsjechi\xeb'), (b'DK', 'Denemarken'), (b'DJ', 'Djibouti'), (b'DM', 'Dominica'), (b'DO', 'Dominicaanse Republiek'), (b'EC', 'Ecuador'), (b'EG', 'Egypte'), (b'SV', 'El Salvador'), (b'GQ', 'Equatoriaal-Guinea'), (b'ER', 'Eritrea'), (b'EE', 'Estland'), (b'ET', 'Ethiopi\xeb'), (b'FK', 'Falklandeilanden'), (b'FO', 'Faer\xf6er'), (b'FJ', 'Fiji'), (b'FI', 'Finland'), (b'FR', 'Frankrijk'), (b'GF', 'Frans-Guyana'), (b'PF', 'Frans-Polynesi\xeb'), (b'TF', 'Franse Zuidelijke en Antarctische Gebieden'), (b'GA', 'Gabon'), (b'GM', 'Gambia'), (b'GE', 'Georgi\xeb'), (b'DE', 'Duitsland'), (b'GH', 'Ghana'), (b'GI', 'Gibraltar'), (b'GR', 'Griekenland'), (b'GL', 'Groenland'), (b'GD', 'Grenada'), (b'GP', 'Guadeloupe'), (b'GU', 'Guam'), (b'GT', 'Guatemala'), (b'GG', 'Guernsey'), (b'GN', 'Guinee'), (b'GW', 'Guinee-Bissau'), (b'GY', 'Guyana'), (b'HT', 'Ha\xefti'), (b'HM', 'Heardeiland en McDonaldeilanden'), (b'VA', 'Vaticaanstad'), (b'HN', 'Honduras'), (b'HK', 'Hong Kong'), (b'HU', 'Hongarije'), (b'IS', 'IJsland'), (b'IN', 'IndiaIndia'), (b'ID', 'Indonesi\xeb'), (b'IR', 'Iran'), (b'IQ', 'Irak'), (b'IE', 'Ierland'), (b'IM', 'Man'), (b'IL', 'Isra\xebl'), (b'IT', 'Itali\xeb'), (b'JM', 'Jamaica'), (b'JP', 'Japan'), (b'JE', 'Jersey'), (b'JO', 'Jordani\xeb'), (b'KZ', 'Kazachstan'), (b'KE', 'Kenia'), (b'KI', 'KiribatiKiribati'), (b'KP', 'Noord-Korea'), (b'KR', 'Zuid-Korea'), (b'KW', 'Koeweit'), (b'KG', 'Kirgizi\xeb'), (b'LA', 'Laos'), (b'LV', 'Letland'), (b'LB', 'Libanon'), (b'LS', 'Lesotho'), (b'LR', 'Liberia'), (b'LY', 'Libi\xeb'), (b'LI', 'Liechtenstein'), (b'LT', 'Litouwen'), (b'LU', 'Luxemburg'), (b'MO', 'Macau'), (b'MK', 'Macedoni\xeb'), (b'MG', 'Madagaskar'), (b'MW', 'Malawi'), (b'MY', 'Maleisi\xeb'), (b'MV', 'Maldiven'), (b'ML', 'Mali'), (b'MT', 'Malta'), (b'MH', 'Marshalleilanden'), (b'MQ', 'Martinique'), (b'MR', 'Mauritani\xeb'), (b'MU', 'Mauritius'), (b'YT', 'Mayotte'), (b'MX', 'Mexico'), (b'FM', 'Micronesi\xeb'), (b'MD', 'Moldavi\xeb'), (b'MC', 'Monaco'), (b'MN', 'Mongoli\xeb'), (b'ME', 'Montenegro'), (b'MS', 'Montserrat'), (b'MA', 'Marokko'), (b'MZ', 'Mozambique'), (b'MM', 'Myanmar'), (b'NA', 'Namibi\xeb'), (b'NR', 'Nauru'), (b'NP', 'Nepal'), (b'NL', 'Nederland'), (b'NC', 'Nieuw-Caledoni\xeb'), (b'NZ', 'Nieuw Zeeland'), (b'NI', 'Nicaragua'), (b'NE', 'Niger'), (b'NG', 'Nigeria'), (b'NU', 'Niue'), (b'NF', 'Norfolk'), (b'MP', 'Noordelijke Marianen'), (b'NO', 'Noorwegen'), (b'OM', 'Oman'), (b'PK', 'Pakistan'), (b'PW', 'Palau'), (b'PS', 'Palestijnse Gebieden'), (b'PA', 'Panama'), (b'PG', 'Papoea-Nieuw-Guinea'), (b'PY', 'Paraguay'), (b'PE', 'Peru'), (b'PH', 'Filipijnen'), (b'PN', 'Pitcairneilanden'), (b'PL', 'Polen'), (b'PT', 'Portugal'), (b'PR', 'Puerto Rico'), (b'QA', 'Qatar'), (b'RE', 'R\xe9union'), (b'RO', 'Roemeni\xeb'), (b'RU', 'Rusland'), (b'RW', 'Rwanda'), (b'BL', 'Saint-Barth\xe9lemy'), (b'SH', 'Sint-Helena, Ascension en Tristan da Cunha'), (b'KN', 'Saint Kitts en Nevis'), (b'LC', 'Saint Lucia'), (b'MF', 'Saint-Martin'), (b'PM', 'Saint-Pierre en Miquelon'), (b'VC', 'Saint Vincent en de Grenadines'), (b'WS', 'Samoa'), (b'SM', 'San Marino'), (b'ST', 'Sao Tom\xe9 en Principe'), (b'SA', 'Saoedi-Arabi\xeb'), (b'SN', 'Senegal'), (b'RS', 'Servi\xeb'), (b'SC', 'Seychellen'), (b'SL', 'Sierra Leone'), (b'SG', 'Singapore'), (b'SX', 'Sint Maarten'), (b'SK', 'Slowakije'), (b'SI', 'Sloveni\xeb'), (b'SB', 'Salomonseilanden'), (b'SO', 'Somali\xeb'), (b'ZA', 'Zuid Afrika'), (b'GS', 'Zuid-Georgi\xeb en de Zuidelijke Sandwicheilanden'), (b'ES', 'Spanje'), (b'LK', 'Sri Lanka'), (b'SD', 'Soedan'), (b'SR', 'Suriname'), (b'SJ', 'Spitsbergen en Jan Mayen'), (b'SZ', 'Swaziland'), (b'SE', 'Zweden'), (b'CH', 'Zwitserland'), (b'SY', 'Syri\xeb'), (b'TW', 'Taiwan'), (b'TJ', 'Tadzjikistan'), (b'TZ', 'Tanzania'), (b'TH', 'Thailand'), (b'TL', 'Oost-Timor'), (b'TG', 'Togo'), (b'TK', 'Tokelau-eilanden'), (b'TO', 'Tonga'), (b'TT', 'Trinidad en Tobago'), (b'TN', 'Tunesi\xeb'), (b'TR', 'Turkije'), (b'TM', 'Turkmenistan'), (b'TC', 'Turks- en Caicoseilanden'), (b'TV', 'Tuvalu'), (b'UG', 'Oeganda'), (b'UA', 'Oekra\xefne'), (b'AE', 'Verenigde Arabische Emiraten'), (b'GB', 'Verenigd Koninkrijk'), (b'US', 'Verenigde Staten'), (b'UM', 'Kleine afgelegen eilanden van de Verenigde Staten'), (b'UY', 'Uruguay'), (b'UZ', 'Oezbekistan'), (b'VU', 'Vanuatu'), (b'VE', 'Venezuela'), (b'VN', 'Vietnam'), (b'VG', 'Maagdeneilanden, Brits'), (b'VI', 'Maagdeneilanden, Amerikaans'), (b'WF', 'Wallis en Futuna'), (b'EH', 'Westelijke Sahara'), (b'YE', 'Jemen'), (b'ZM', 'Zambia'), (b'ZW', 'Zimbabwe')])),
                ('email', models.EmailField(max_length=254, verbose_name='e-mail', blank=True)),
                ('phone_fixed', models.CharField(max_length=16, verbose_name='phone fixed', blank=True)),
                ('machazine', models.BooleanField(default=True, verbose_name='MaCHazine')),
                ('board_invites', models.BooleanField(default=False, verbose_name='board invites')),
                ('constitution_card', models.BooleanField(default=False, verbose_name='constitution card')),
                ('christmas_card', models.BooleanField(default=True, verbose_name='Christmas card')),
                ('yearbook', models.BooleanField(default=False, verbose_name='yearbook')),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'entity',
                'verbose_name_plural': 'entities',
            },
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('ip', models.CharField(max_length=40, verbose_name='ip address')),
                ('modification', models.TextField(verbose_name='modification', blank=True)),
            ],
            options={
                'verbose_name': 'modification',
                'verbose_name_plural': 'modifications',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ldb.Entity')),
                ('name_prefix', models.CharField(max_length=100, verbose_name='name prefix')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('name_short', models.CharField(max_length=100, verbose_name='name short', blank=True)),
                ('salutation', models.CharField(max_length=100, verbose_name='salutation')),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            },
            bases=('ldb.entity',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ldb.Entity')),
                ('titles', models.CharField(max_length=20, verbose_name='titles', blank=True)),
                ('initials', models.CharField(max_length=15, verbose_name='initials')),
                ('firstname', models.CharField(max_length=50, verbose_name='first name')),
                ('preposition', models.CharField(max_length=15, verbose_name='preposition', blank=True)),
                ('surname', models.CharField(max_length=100, verbose_name='surname')),
                ('postfix_titles', models.CharField(max_length=20, verbose_name='postfix titles', blank=True)),
                ('phone_mobile', models.CharField(max_length=16, verbose_name='phone mobile', blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, verbose_name='gender', choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('birthdate', models.DateField(null=True, verbose_name='birthdate', blank=True)),
                ('deceased', models.BooleanField(default=False, verbose_name='deceased')),
                ('mail_announcements', models.BooleanField(default=True, verbose_name='announcements mailing')),
                ('mail_company', models.BooleanField(default=True, verbose_name='company mailing')),
                ('ldap_username', models.CharField(max_length=50, verbose_name='LDAP username', blank=True)),
                ('netid', models.CharField(max_length=32, verbose_name='NetID', blank=True)),
                ('linkedin_id', models.CharField(max_length=32, verbose_name='LinkedIn ID', blank=True)),
                ('facebook_id', models.CharField(max_length=32, verbose_name='Facebook ID', blank=True)),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
            },
            bases=('ldb.entity',),
        ),
        migrations.CreateModel(
            name='Alumnus',
            fields=[
                ('person', models.OneToOneField(primary_key=True, serialize=False, to='ldb.Person')),
                ('study', models.CharField(max_length=100, verbose_name='study', blank=True)),
                ('study_first_year', models.IntegerField(null=True, verbose_name='study first year', blank=True)),
                ('study_last_year', models.IntegerField(null=True, verbose_name='study last year', blank=True)),
                ('study_research_group', models.CharField(max_length=100, verbose_name='research group', blank=True)),
                ('study_paper', models.CharField(max_length=300, verbose_name='paper', blank=True)),
                ('study_professor', models.CharField(max_length=100, verbose_name='professor', blank=True)),
                ('work_company', models.CharField(max_length=100, verbose_name='company', blank=True)),
                ('work_position', models.CharField(max_length=100, verbose_name='position', blank=True)),
                ('work_sector', models.CharField(max_length=100, verbose_name='sector', blank=True)),
                ('contact_method', models.CharField(default=b'e', max_length=1, verbose_name='contact method', choices=[(b'm', b'Mail'), (b'e', b'Email')])),
            ],
            options={
                'verbose_name': 'alumnus',
                'verbose_name_plural': 'alumni',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('person', models.OneToOneField(primary_key=True, serialize=False, to='ldb.Person')),
                ('faculty', models.CharField(max_length=50, verbose_name='faculty')),
                ('department', models.CharField(max_length=50, verbose_name='department')),
                ('function', models.CharField(max_length=50, verbose_name='function')),
                ('phone_internal', models.CharField(max_length=5, verbose_name='phone internal')),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('person', models.OneToOneField(primary_key=True, serialize=False, to='ldb.Person')),
                ('date_from', models.DateField(null=True, verbose_name='date from', blank=True)),
                ('date_to', models.DateField(null=True, verbose_name='date to', blank=True)),
                ('date_paid', models.DateField(null=True, verbose_name='date paid', blank=True)),
                ('amount_paid', models.IntegerField(null=True, verbose_name='amount paid', blank=True)),
                ('associate_member', models.BooleanField(default=False, verbose_name='associate member')),
                ('donating_member', models.BooleanField(default=False, verbose_name='donating member')),
                ('merit_date_from', models.DateField(null=True, verbose_name='merit member date from', blank=True)),
                ('merit_invitations', models.BooleanField(default=True, verbose_name='merit member invitations')),
                ('merit_history', models.TextField(verbose_name='merit member history', blank=True)),
                ('honorary_date_from', models.DateField(null=True, verbose_name='honorary member from date', blank=True)),
            ],
            options={
                'verbose_name': 'member',
                'verbose_name_plural': 'members',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('person', models.OneToOneField(primary_key=True, serialize=False, to='ldb.Person')),
                ('study', models.CharField(max_length=50, verbose_name='study')),
                ('first_year', models.IntegerField(null=True, verbose_name='first year', blank=True)),
                ('student_number', models.CharField(max_length=7, verbose_name='student number', blank=True)),
                ('graduated', models.BooleanField(default=False, verbose_name='graduated')),
                ('phone_parents', models.CharField(max_length=16, verbose_name='phone parents', blank=True)),
                ('yearbook_permission', models.BooleanField(default=True, verbose_name='yearbook permission')),
                ('date_verified', models.DateField(null=True, verbose_name='date verified', blank=True)),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='living_with',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ldb.Person'),
        ),
        migrations.AddField(
            model_name='modification',
            name='person',
            field=models.ForeignKey(to='ldb.Person'),
        ),
        migrations.AddField(
            model_name='committeemembership',
            name='person',
            field=models.ForeignKey(to='ldb.Person'),
        ),
        migrations.AddField(
            model_name='committee',
            name='members',
            field=models.ManyToManyField(to='ldb.Person', through='ldb.CommitteeMembership'),
        ),
    ]
