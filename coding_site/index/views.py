from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard_view(request):
    problemSet = fetchProblems()
    context = {"problems" : problemSet}
    return render(request,"dashboard.html",context=context)




def fetchProblems():
    url = 'https://codeforces.com/api/problemset.problems'
    data = requests.get(url)
    JSONdata = data.json()
    problemSet = []
    if JSONdata["status"] != 'OK':

        return problemSet

    for problem in JSONdata['result']['problems']:
        p = ExtractProblem(problem)
        problemSet.append(p)
    
    return problemSet

def ExtractProblem(problem):

    p = {'contestID' : problem["contestId"],
            'index'  : problem["index"],
            'name'   : problem["name"],
            'link'   : 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
        }
    return p