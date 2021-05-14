from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required

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
    url = 'https://codeforces.com/api/problemset.problems'
    data = requests.get(url)
    JSONdata = data.json()
    problemSet = []

    if JSONdata["status"] != 'OK':
        return problemSet

    for problem in JSONdata['result']['problems']:
        p = ExtractProblem(problem)
        if( not filter or ( p['rating']>=min and p['rating']<=max ) ):
            problemSet.append(p)
        
    return problemSet

def ExtractProblem(problem):
    if 'rating' in problem:
        rating = problem["rating"]
    else:
        rating = 0

    p = {'contestID' : problem["contestId"],
            'index'  : problem["index"],
            'name'   : problem["name"],
            'rating' : rating,
            'link'   : 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
        }
    return p