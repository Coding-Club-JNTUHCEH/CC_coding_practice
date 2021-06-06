from django.shortcuts import render
from users.models import UserProfile
from index.models import Problem
from django.contrib.auth.decorators import login_required
# from users.codeforces_API import fetchAllProblems
from users.codeforces_API import fetchAllContests
from .models import Contest
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

# Create your views here.


@login_required
def contest_page(request, *args, **kwargs):
    context = {}
    
    user_solved = UserProfile.objects.get(
                    user=request.user).sloved_problems.all()
    user_not_solved = UserProfile.objects.get(
                    user=request.user).not_sloved_problems.all()
    
    
    if 'type1' in kwargs:
        typee = kwargs["type1"]
        
        contests = (Contest.objects.annotate(num_problems=Count('problems'))
                            .filter(name__icontains="Div. "+typee, num_problems__gt=4))
        print(len(contests))

    else:
        typee = '0'
        contests = (Contest.objects.annotate(num_problems=Count('problems'))
                            .filter(name__icontains="Div.", num_problems__gt=4))
        print(len(contests))

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
    a, count = 1, 1
    if len(contests) == 0 or not request.user.is_superuser:
        return render(request, "hello.html", context={"result": False})

    print(":) !!!!")

    for contest in contests:

        if a < 100:

            c_db = Contest.create(contest)

            try:
                problems = Problem.objects.filter(
                            contestID=c_db.contestID).order_by("-index")
                if problems.exists() and len(problems) > 4 and len(problems)<9:
                    c_db.save()
                    c_db.problems.add(*problems)

                count += 1
                print(str(a)+"  .Contest " + c_db +" saved")
            except:
                pass
            
            a += 1

    return render(request, "hello.html", context={"result": True, "count": count})



