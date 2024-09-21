from django.shortcuts import redirect, render
from .forms import MeetingForm
from django.contrib.auth.decorators import login_required
from .models import Meeting
from django.utils import timezone


@login_required
def calendar_view(request):
    meetings = Meeting.objects.filter(user=request.user).values(
        'id', 'title', 'start_time', 'end_time'
    )
    meetings_data = [
        {
            'id': meeting['id'],
            'title': meeting['title'],
            'start_time': meeting['start_time'].isoformat(),
            'end_time': meeting['end_time'].isoformat()
        }
        for meeting in meetings
    ]

    return render(request, 'schedule/calendar.html', {'meetings': meetings_data})


@login_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.user = request.user
            meeting.save()
            print("Meeting created:", meeting)  # Adicione isso para verificar
            return redirect('calendar')
    else:
        form = MeetingForm()

    return render(request, 'schedule/create_meeting.html', {'form': form})
