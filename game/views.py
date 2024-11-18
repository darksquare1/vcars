from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import ListView, View

from game.models import Record


class GameView(ListView):
    template_name = 'game/game.html'
    model = Record
    context_object_name = 'records'


class RecordView(View):
    def post(self, request, *args, **kwargs):
        score = int(request.POST.get('score'))
        if score and request.user.is_authenticated:
            all_records = Record.objects.all()
            owner = request.user
            records = all_records.filter(owner=owner)
            if records.exists():
                record = records.first()
                best_owner_score = record.record
                if score > best_owner_score:
                    record.record = score
                    record.save()
            else:
                all_records.create(owner=owner, record=score)
            return render(request, 'includes/records.html', {'records': all_records})
        return HttpResponseBadRequest()
