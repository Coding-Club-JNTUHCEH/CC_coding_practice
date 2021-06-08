from users.models import UserProfile
from .models import Problem, Tag


def fetchProblems(min=0, max=5000, tags=[], user=None, filter=False):
    
    if not filter:
        problemSet = Problem.objects.all().values()

    elif len(tags) == 0:
        problemSet = Problem.objects.filter(
            rating__lt=max, rating__gt=min).values()

    else:
        tags_objList = []
        for tag in tags:
            tags_objList.append(Tag.objects.get_or_create(tag_name=tag)[0])

        problemSet = Problem.objects.filter(
            rating__lt=max, rating__gt=min, tags__in=tags_objList)

    return problemSet


def friendsSubmissions(user):
    allProblems = []
    per = 2  # --> no of questions from each friend should be taken
    friends = UserProfile.objects.get(user=user).friends.all()
    for friend in friends:
        try:
            problems = friend.sloved_problems.all()[:per].values()
        except:
            problems = friend.sloved_problems.all().values()
        allProblems.extend(problems)

    return allProblems