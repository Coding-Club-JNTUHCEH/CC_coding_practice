from users.codeforces_API import fetchAllProblems
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from .models import Problem,Tag

# Create your views here.
@login_required
def dashboard_view(request):

    if(request.method=="POST"):
        min_rating = int(request.POST.get("minPts"))
        max_rating = int(request.POST.get("maxPts"))
        problemSet = fetchProblems(min = min_rating, max = max_rating, filter = True)

    else:
        problemSet = fetchProblems()
    
    context = {"problems" : problemSet}

    return render(request,"dashboard.html",context=context)



def fetchProblems(min = 0, max = 5000, filter = False):

    if not filter:
        problemSet = Problem.objects.all().values()
    else:
        problemSet = Problem.objects.filter(rating__lt = max,rating__gt = min).values()

        
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


