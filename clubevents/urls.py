from django.contrib import admin
from django.urls import include, path
from clubevents import views as v
urlpatterns = [
    path('events', v.events,name='events'),

 ]