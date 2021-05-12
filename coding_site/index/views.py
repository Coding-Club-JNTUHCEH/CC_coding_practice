from django.shortcuts import render
import requests


# Create your views here.
def dashboard(request):
    problemSet = fetchProblems()
    context = {"problems" : problemSet}
    return render(request,"dashboard.html",context=context)




def fetchProblems():
    url = 'https://codeforces.com/api/problemset.problems'
    data = requests.get(url)
    JSONdata = data.json()
    if JSONdata["status"] != 'OK':
        return []
    problemSet = []
    for problem in JSONdata['result']['problems']:
        p = {'contestID' : problem["contestId"],
                'index'  : problem["index"],
                'name'   : problem["name"],
                'link'   : 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
            }
    
        problemSet.append(p)
    return problemSet