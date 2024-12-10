import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#9B59B6', '#E74C3C', '#1ABC9C']
    
    meetings_data = [
        {
            'id': meeting['id'],
            'title': meeting['title'],
            'start_time': meeting['start_time'].isoformat(),
            'end_time': meeting['end_time'].isoformat(),
            'color': random.choice(colors),  # Escolhe uma cor aleatória
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

@csrf_exempt  # Para simplificar, mas poda pra melhorar a segurança
def update_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_id = data.get('id')
            start = data.get('start')
            end = data.get('end')

            # Validações básicas
            if not event_id or not start:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Atualiza o evento no banco de dados
            meeting = Meeting.objects.get(id=event_id)
            meeting.start_time = start
            meeting.end_time = end if end else meeting.start_time
            meeting.save()

            return JsonResponse({'success': True, 'message': 'Event updated successfully'})
        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def meeting_detail(request, pk):
    meeting = Meeting.objects.prefetch_related('invited_contacts').get(pk=pk, user=request.user)
    return render(request, 'schedule/meeting_detail.html', {
        'meeting': meeting,
        'contacts': meeting.invited_contacts.all()
    })