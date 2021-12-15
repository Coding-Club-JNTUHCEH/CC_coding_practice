from django.shortcuts import render
from django.http import HttpResponse
from .models import Clubevents

# Create your views here.

def events(request):
    Clubeventobj=Clubevents.objects.all()
    context={"Clubeventobj":Clubeventobj}

    return render(request,"Eventspage.html",context)
