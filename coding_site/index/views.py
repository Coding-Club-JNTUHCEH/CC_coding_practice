from django.shortcuts import render
import requests
from django.core import serializers
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
    
    context = {"result" : fetchProblemsForDB()}

    return render(request,"hello.html",context)

def fetchProblemsForDB():
    url = 'https://codeforces.com/api/problemset.problems'
    data = requests.get(url)
    JSONdata = data.json()
    
    if JSONdata["status"] != 'OK':    
        return False
    a = 1
    for problem in JSONdata['result']['problems']:
        p = ExtractProblemForDB(problem)
        p_db = Problem.create(p)

        try:
            p_db.save()
            p_db.link_tags(p["tags"])
            print(str(a)+".Problem "+ str(p["contestID"])+p["index"]+" saved" .format(a))
        except:
            pass
        a+=1
    return True

def ExtractProblemForDB(problem):
    if 'rating' in problem:
        rating = problem["rating"]
    else:
        rating = 0
    if 'tags' in problem:
        tags = problem["tags"]
    else:
        tags = []

    p = {'contestID' : problem["contestId"],
            'index'  : problem["index"],
            'name'   : problem["name"],
            'rating' : rating,
            'tags'   : tags,
            'link'   : 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
        }
    return p
