from django.contrib import admin
from .models import Mentor

class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'views_count')

admin.site.register(Mentor, MentorAdmin)
