from django.shortcuts import render
from users.models import UserProfile
from index.models import Problem
# from users.codeforces_API import fetchAllProblems
from users.codeforces_API import fetchAllContests
from .models import Contest
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def contest_page(request, *args, **kwargs):

    user_solved = UserProfile.objects.get(
        user=request.user).sloved_problems.all()
    print(user_solved)
    if 'type1' in kwargs:
        typee = kwargs["type1"]
        contests = Contest.objects.filter(name__icontains="Div. "+typee)

    else:
        typee = '0'
        contests = Contest.objects.filter(name__icontains="Div.")

    flag = '0'
    limit = 15
    # if 'contest-all' in request.path:
    #     limit = 200

    # for contest in contests:
    #     if a < limit:

    #         print(contest)
    #         print(type(contest.type))

    #     else:
    #         break
    page = request.GET.get('page', 1)

    paginator = Paginator(contests, 10)
    try:
        contest = paginator.page(page)
    except PageNotAnInteger:
        contest = paginator.page(1)
    except EmptyPage:
        contest = paginator.page(paginator.num_pages)

    print(typee)
    print(request.path)
    print(contests)
    path = request.path + '-all'
    return render(request, 'contest_page.html', {'contests': contest, 'path': path, 'type': typee, 'user_solved': user_solved, 'flag': flag})


# https://codeforces.com/api/contest.list

def loadContests_view(request):

    contests = fetchAllContests()
    # problems = fetchAllProblems()
    # Contest.objects.all().delete()

    a, count = 1, 1
    if len(contests) == 0:  # or not request.user.is_superuser:
        print(":( !!!!!")
        print(contests)
        return render(request, "hello.html", context={"result": False})

    print(":) !!!!")

    for contest in contests:

        # if a < 20:

        c_db = Contest.create(contest)
        # c_db.problems = c_db.add_problems()

        try:
            c_db.save()
            count += 1
            # problems = Problem.objects.filter(
            #     contestID=contest['contestID']).order_by("index")
            # print(problems)
            # c_db.link_problems(problems)
            # print(str(a) + ".contest".format(a))
            # print(contest)
            # print("Contest added-"+a)
            # print(str(a)+".Contest ", c_db, " saved".format(a))
        except:
            print("Error!!!")
            # print(str(a)+".Contest ", c_db, " could not add".format(a))
        # a += 1

    print('yes!!!!')
    return render(request, "hello.html", context={"result": True, "count": count})


def update_contestProblems(request):
    contests = Contest.objects.filter(name__icontains="Div.")
    # a = 1
    for contest in contests:
        # if a < 20:
        print(contest.name)
        print(contest.contestID)
        print(contest.type)
        problems = Problem.objects.filter(
            contestID=contest.contestID).order_by("-index")
        print(problems)
        if problems.exists() and len(problems) > 4:
            # print(type(problems_list))
            contest.link_problems(problems)
            # a += 1

        print(contest)
        # contest.problems.all().order_by("index")
        print(contest.problems.all())

    return HttpResponse("Hello")
