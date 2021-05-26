from django.shortcuts import render
from users.models import UserProfile
from index.models import Problem
# from users.codeforces_API import fetchAllProblems
from users.codeforces_API import fetchAllContests
from .models import Contest
from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def contest_page(request):
    contests = Contest.objects.filter(name__icontains="Div.").values()
    a = 1
    limit = 15
    if 'contest-all' in request.path:
        limit = 200

    for contest in contests:
        if a < limit:
            print(contest)
            print(contest['name'])
            print(contest['contestID'])
            print(contest['type'])
            # print(contest['problems'])
            # contest['problems'] = ['A']
            problems = Problem.objects.filter(
                contestID=contest['contestID']).order_by("index")
            print(problems)
            print(len(problems))
            # print(problems)
            if problems.exists() and len(problems) > 4:
                # print(type(problems_list))
                contest['problems'] = list(problems)
                a += 1
            # print(contest['problems'])
            print(contest)
            # print(', '.join(contest.problems.values_list('name', flat=True)))

        else:
            break

    print(request.path)
    path = request.path + '-all'
    return render(request, 'contest_page.html', {'contests': contests, 'path': path})


# https://codeforces.com/api/contest.list

def loadContests_view(request):

    contests = fetchAllContests()
    # problems = fetchAllProblems()
    a, count = 1, 1
    if len(contests) == 0:  # or not request.user.is_superuser:
        print(":( !!!!!")
        print(contests)
        return render(request, "hello.html", context={"result": False})

    print(":) !!!!")

    for contest in contests:

        c_db = Contest.create(contest)
        c_db.problems = c_db.add_problems()

        try:
            c_db.save()
            count += 1
        except:
            print("Error!!!")
        a += 1

    print('yes!!!!')
    return render(request, "hello.html", context={"result": True, "count": count})


def update_contestProblems(request):
    contests = Contest.objects.all().filter(name__icontains="Div.")
    a = 1
    for contest in contests:
        if a < 15:
            print(contest.name)
            print(contest.contestID)
            print(contest.type)
            # print(Problem.objects.all())
            problems = Problem.objects.filter(
                contestID=contest.contestID).order_by("index")
            print(problems)
            print(len(problems))
            # print(problems)
            if problems.exists() and len(problems) > 4:

                # print(type(problems_list))
                contest.problems.add(*problems)
            a += 1
            print(contest.problems.all())
            print(contest)
    # print(contests)
    return HttpResponse("Hello")
