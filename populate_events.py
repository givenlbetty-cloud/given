import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from blog.models import Event

def run():
    print("Populating events...")
    
    events_data = [
        {"titre": "Webinaire : Réussir son Entretien", "days": 5, "lieu": "Zoom", "link": "https://zoom.us/j/123456"},
        {"titre": "Workshop : Python pour Débutants", "days": 12, "lieu": "Campus ATJ - Salle 101", "link": None},
        {"titre": "Conférence : L'Avenir de l'IA", "days": 20, "lieu": "Amphithéâtre Principal", "link": "https://eventbrite.com/atj-ia"},
    ]

    for e_data in events_data:
        date_event = timezone.now() + timedelta(days=e_data['days'])
        Event.objects.get_or_create(
            titre=e_data['titre'],
            defaults={
                "date": date_event,
                "lieu": e_data['lieu'],
                "lien_inscription": e_data['link']
            }
        )
        print(f"Created Event: {e_data['titre']}")

if __name__ == '__main__':
    run()
