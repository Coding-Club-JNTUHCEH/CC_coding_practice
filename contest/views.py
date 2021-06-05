from django.shortcuts import render
from users.models import UserProfile
from index.models import Problem
from django.contrib.auth.decorators import login_required
# from users.codeforces_API import fetchAllProblems
from users.codeforces_API import fetchAllContests
from .models import Contest
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@login_required
def contest_page(request, *args, **kwargs):
    context = {}
    contests = Contest.objects.filter(name__icontains="Div.").values()

    user_solved = UserProfile.objects.get(
        user=request.user).sloved_problems.all()
    user_not_solved = UserProfile.objects.get(
        user=request.user).not_sloved_problems.all()
    print(user_solved)
    if 'type1' in kwargs:
        typee = kwargs["type1"]
        contests = Contest.objects.filter(name__icontains="Div. "+typee)
    else:
        typee = '0'
        contests = Contest.objects.filter(name__icontains="Div.")

    page = request.GET.get('page', 1)
    paginator = Paginator(contests, 20)

    try:
        contest = paginator.page(page)
    except PageNotAnInteger:
        contest = paginator.page(1)
    except EmptyPage:
        contest = paginator.page(paginator.num_pages)


    ls = contest.paginator.num_pages - 1

    context['contests'] = contest
    context['user_not_solved'] = user_not_solved
    context['type'] = typee
    context['user_solved'] = user_solved
    context['ls'] = ls

    return render(request, 'contest_page.html', context=context)


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
