from django.db import migrations

def enforce_rls(apps, schema_editor):
    """
    Enables Row Level Security on all tables in the public schema.
    This is a professional, code-driven way to ensure Supabase security.
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            DO $$ 
            DECLARE 
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'ALTER TABLE public.' || quote_ident(r.tablename) || ' ENABLE ROW LEVEL SECURITY;';
                END LOOP;
            END $$;
        """)

class Migration(migrations.Migration):
    dependencies = [
        ('system', '0003_activesession_loginlog_pagevisit'),
    ]

    operations = [
        migrations.RunPython(enforce_rls),
    ]
