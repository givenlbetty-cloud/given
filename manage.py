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
    # avant le migrate du dashboard Render
    import django
    django.setup()
    from django.db import connection
    with connection.cursor() as c:
        c.execute("DROP TABLE IF EXISTS formations_formation, formations_lecon, formations_session, formations_inscription, formations_paiement CASCADE")
        c.execute("DELETE FROM django_migrations WHERE app = 'formations'")

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
