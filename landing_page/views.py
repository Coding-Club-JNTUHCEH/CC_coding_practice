
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.


def landing(request):
    return render(request, 'landing.html')
