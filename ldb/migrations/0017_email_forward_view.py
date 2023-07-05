from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("ldb", "0016_person_email_forward")]

    operations = [migrations.RunSQL("""CREATE OR REPLACE VIEW email_forward AS
                SELECT p.ldap_username AS "from", e.email AS "to" FROM ldb_person p
                INNER JOIN ldb_entity e on p.entity_ptr_id = e.id
                WHERE email_forward = TRUE;
            """)]
