from django.shortcuts import redirect, render
from .forms import MeetingForm
from django.contrib.auth.decorators import login_required
from .models import Meeting
from django.utils import timezone


@login_required
def calendar_view(request):
    # Filtra eventos do usuário atual e busca os contatos convidados
    meetings = Meeting.objects.filter(user=request.user).prefetch_related('invited_contacts')

    # Serializa os dados para uso no frontend
    meetings_data = [
        {
            'id': meeting.id,
            'title': meeting.title,
            'start_time': meeting.start_time.isoformat(),
            'end_time': meeting.end_time.isoformat(),
            'contacts': [contact.first_name for contact in meeting.invited_contacts.all()],
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
            meeting.user = request.user  # Associa o evento ao usuário atual
            meeting.save()
            form.save_m2m()  # Salva a relação ManyToMany (contatos convidados)
            print("Meeting created:", meeting)  # Debug para verificar a criação
            return redirect('calendar')
    else:
        form = MeetingForm()

    return render(request, 'schedule/create_meeting.html', {'form': form})

@login_required
def meeting_detail(request, pk):
    meeting = Meeting.objects.prefetch_related('invited_contacts').get(pk=pk, user=request.user)
    return render(request, 'schedule/meeting_detail.html', {
        'meeting': meeting,
        'contacts': meeting.invited_contacts.all()
    })