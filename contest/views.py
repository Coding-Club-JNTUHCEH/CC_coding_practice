from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

from users.models import UserProfile
from index.models import Problem
from API_manager import codeforces_API

from .models import Contest


# Create your views here.

@login_required
def contest_page(request, *args, **kwargs):
    context = {}

    user_solved     = UserProfile.objects.get(
                        user=request.user).sloved_problems.all()
    user_not_solved = UserProfile.objects.get(
                        user=request.user).not_sloved_problems.all()

    if 'type1' in kwargs:
        typee = kwargs["type1"]

        contests = (Contest.objects.annotate(num_problems=Count('problems'))
                    .filter(name__icontains="Div. "+typee, num_problems__gt=4))

    else:
        typee = '0'
        contests = (Contest.objects.annotate(num_problems=Count('problems'))
                    .filter(name__icontains="Div.", num_problems__gt=4))

    page = request.GET.get('page', 1)
    paginator = Paginator(contests, 20)

    try:
        contest = paginator.page(page)
    except PageNotAnInteger:
        contest = paginator.page(1)
    except EmptyPage:
        contest = paginator.page(paginator.num_pages)

    ls = contest.paginator.num_pages - 1

    context['contests'] = contest
    context['user_not_solved'] = user_not_solved
    context['type'] = typee
    context['user_solved'] = user_solved
    context['ls'] = ls

    return render(request, 'contest_page.html', context=context)


# https://codeforces.com/api/contest.list

