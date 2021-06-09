
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied

from users.models import UserProfile
from API_manager import codeforces_API
from . import services 
from .models import Problem, Tag
# Create your views here.


@login_required
def dashboard_view(request):
    context = {"tags": list(Tag.objects.all())}

    if(request.method == "POST"):
        context["min"]      = int(request.POST.get("minPts"))
        context["max"]      = int(request.POST.get("maxPts"))
        tags                = request.POST.getlist("listOfTags")
        context["problems"] = services.fetchProblems(
                                    min=context["min"], max=context["max"], tags=tags, user=request.user, filter=True)

    else:
        context["min"]      = 0
        context["max"]      = 5000
        context["problems"] = services.fetchProblems(user=request.user)

    context['user_solved']      = UserProfile.objects.get(
                                    user=request.user).updated_solvedProblems().all().values()
    context['user_not_solved']  = UserProfile.objects.get(
                                    user=request.user).updated_not_solvedProblems().all().values()
    context['friends_solved']   = services.friendsSubmissions(user=request.user)

    page = request.GET.get('page', 1)
    paginator = Paginator(context["problems"], 20)
    try:
        context["problems"] = paginator.page(page)
    except PageNotAnInteger:
        context["problems"] = paginator.page(1)
    except EmptyPage:
        context["problems"] = paginator.page(paginator.num_pages)

    
    context['ls'] = context['problems'].paginator.num_pages - 1

    return render(request, "dashboard.html", context=context)


