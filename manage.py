#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atj_site.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Nettoyer les anciennes tables formations (refonte LMS)
    # UNIQUEMENT avant la commande migrate
    if len(sys.argv) >= 2 and sys.argv[1] == 'migrate':
        import django
        django.setup()
        from django.db import connection
        with connection.cursor() as c:
            # DROP toutes les tables formations (PostgreSQL uniquement)
            if connection.vendor == 'postgresql':
                c.execute("""
                    DO $$ DECLARE
                        r RECORD;
                    BEGIN
                        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'formations_%') LOOP
                            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                        END LOOP;
                    END $$;
                """)
            c.execute("DELETE FROM django_migrations WHERE app = 'formations'")

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
