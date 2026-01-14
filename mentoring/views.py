from django.shortcuts import render, get_object_or_404
from .models import Mentor

from django.db.models import Q

def mentor_list(request):
    query = request.GET.get('q')
    if query:
        mentors = Mentor.objects.filter(
            Q(user__username__icontains=query) | 
            Q(expertise__icontains=query)
        )
    else:
        mentors = Mentor.objects.all()
    return render(request, 'mentoring/list.html', {'mentors': mentors, 'query': query})

def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    # Increment views
    mentor.views_count += 1
    mentor.save()
    return render(request, 'mentoring/detail.html', {'mentor': mentor})
