from django.contrib import admin

from .models import Problem,Tag

# Register your models here.

admin.site.register(Problem)

admin.site.register(Tag)