from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from .models import Problem,Tag
# Create your views here.


@login_required
def dashboard_view(request):

    if(request.method == "POST"):
        min_rating = int(request.POST.get("minPts"))
        max_rating = int(request.POST.get("maxPts"))
        tags = request.POST.getlist("listOfTags")
        # print(tags)
        problemSet = fetchProblems(
            min=min_rating, max=max_rating, tags=tags, filter=True)

    else:
        problemSet = fetchProblems()

    context = {"problems": problemSet}

    return render(request, "dashboard.html", context=context)


def fetchProblems(min=0, max=5000, tags=[], filter=False):

    if not filter:
        problemSet = Problem.objects.all().values()
    else:
        tags_objList = []
        for tag in tags:
            try:
                tags_objList.append(Tag.objects.get(tag_name = tag))
            except:
                pass
        problemSet = Problem.objects.filter(rating__lt = max, rating__gt = min, tags__in = tags_objList).values()

        
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

    # url = 'https://codeforces.com/api/problemset.problems'
    # data = requests.get(url)
    # JSONdata = data.json()
    # problemSet = []

    # if JSONdata["status"] != 'OK':
    #     return problemSet

    # for problem in JSONdata['result']['problems']:
    #     p = ExtractProblem(problem)
    #     check = any(tag in p['tags'] for tag in tags)
    #     if(not filter or ((p['rating'] >= min and p['rating'] <= max) and check)):
    #         problemSet.append(p)

    # return problemSet


# def ExtractProblem(problem):
#     if 'rating' in problem and 'tags' in problem:
#         rating = problem["rating"]
#         tags = problem["tags"]
#     elif 'rating' in problem:
#         rating = problem["rating"]
#         tags = []
#     elif 'tags' in problem:
#         tags = problem["tags"]
#         rating = 0
#     else:
#         rating = 0
#         tags = []

#     p = {'contestID': problem["contestId"],
#          'index': problem["index"],
#          'name': problem["name"],
#          'rating': rating,
#          'tags': tags,
#          'link': 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
#          }
#     return p
