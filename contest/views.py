from django.shortcuts import render
from users.models import UserProfile
from index.models import Problem
# from users.codeforces_API import fetchAllProblems
from users.codeforces_API import fetchAllContests
from .models import Contest
from django.http import HttpResponse
# Create your views here.


def contest_page(request):
    contests = Contest.objects.filter(name__icontains="Div.").values()
    a = 1
    for contest in contests:
        # if a < 10:
        print(contest)
        print(contest['name'])
        print(contest['contestID'])
        print(contest['type'])
        # print(contest['problems'])
        # # contest['problems'] = ['A']
        # problems = Problem.objects.filter(
        #     contestID=contest['contestID']).order_by("index")
        # print(problems)
        # print(len(problems))
        # # print(problems)
        # if problems.exists() and len(problems) > 4:

        #     # print(type(problems_list))
        #     contest['problems'] = list(problems)
        #     # a += 1
        # print(contest)
        # print(', '.join(contest.problems.values_list('name', flat=True)))
        # a += 1
    # print(contests)
    return render(request, 'contest_page.html', {'contests': contests})


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
        # print(c_db.problems)
        # problems = Problem.
        # c_db.problems.set(problems)
        try:
            c_db.save()
            count += 1
            # p_db.link_tags(problem["tags"])
            # print(str(a)+".Contest ", c_db, " saved" .format(a))
        except:
            print("Error!!!")
            # print(str(a)+".Contest ", c_db, " could not add" .format(a))
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
