
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from users.codeforces_API import fetchAllProblems

from .models import Problem,Tag
# Create your views here.


@login_required
def dashboard_view(request):
    context = {}
    if(request.method == "POST"):
        context["min"] = int(request.POST.get("minPts"))
        context["max"] = int(request.POST.get("maxPts"))
        tags = request.POST.getlist("listOfTags")
        context["problems"] = fetchProblems( min=context["min"] , max=context["max"] , tags=tags, user = request.user, filter=True )

    else:
        context["min"] = 0
        context["max"] = 5000
        context["problems"] = fetchProblems()

    context["tags"]     = list(Tag.objects.all())

    return render(request, "dashboard.html", context=context)


def fetchProblems(min=0, max=5000, tags=[],user = None ,filter=False):

    if not filter:
        problemSet = Problem.objects.all().values()
        
    elif len(tags) == 0:
        problemSet = Problem.objects.filter(rating__lt = max, rating__gt = min).values()

    else:
        tags_objList = []
        for tag in tags:
            tags_objList.append(Tag.objects.get_or_create(tag_name = tag)[0])
            
        problemSet = Problem.objects.filter(rating__lt = max, rating__gt = min, tags__in = tags_objList )
    
    user_solved =  UserProfile.objects.get(user = user).sloved_problems.all()
    problemSet = problemSet.difference(user_solved).values()
        
    return problemSet


def loadProblems_view(request):
    
    problems  = fetchAllProblems()
    a,count = 1,1
    if len(problems) == 0 or not request.user.is_superuser :
        return render(request,"hello.html",context = {"result"  : False})

    for problem in problems:
        
        p_db = Problem.create(problem)
        try:
            p_db.save()
            count+=1
            p_db.link_tags(problem["tags"])
            print(str(a)+".Problem ",p_db," saved" .format(a))
        except:
            print(str(a)+".Problem ",p_db ," could not add" .format(a))
        a+=1

    return render(request,"hello.html",context = {"result"  : True, "count" : count})

 
