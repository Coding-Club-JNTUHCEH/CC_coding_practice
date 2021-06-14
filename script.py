import os
import django
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE'))
django.setup()

from django.db import IntegrityError

from contest.models import Contest
from index.models import Problem
from API_manager import codeforces_API
from users.models import UserProfile

def loadProblems():
    
    problems = codeforces_API.fetchAllProblems()
    a,count = 1,1

    for problem in problems:

        p_db = Problem.create(problem)
        try:
            p_db.save()
            p_db.link_tags(problem["tags"])
            print(str(a)+".Problem ", p_db, " saved")
            count += 1
            
        except:
            print(str(a)+".Problem ", p_db, " could not add")
        a+=1
        
    print("Problems updated")
    print(str(count) + " Problems lodaed")


def loadContests():
    no_columns = 8
    contests = codeforces_API.fetchAllContests()
    count = 0
   
    for contest in contests:

        c_db = Contest.create(contest)
        problems = Problem.objects.filter(
                    contestID=c_db.contestID).order_by("-index")

        if problems.exists() and 4 < len(problems) < 9 and "Div" in c_db.name:
            c_db.empty = no_columns - len(problems)
            try:
                c_db.save()
                c_db.problems.add(*problems)
                print(str(count)+". Contest " + str(c_db) + " saved")

            except IntegrityError:
                Contest.objects.filter(contestID=c_db.contestID).update(
                    empty=no_columns - len(problems))
                print(str(count)+". Contest " + str(c_db) + " updated")
            except:
                pass
            count += 1

    print("Contests updated")
    print(str(count) + " Contests lodaed")

def update_solvedProblems_count_value():
    users = UserProfile.objects.all()
    for user in users:
        try:
            user.sloved_problems_count = user.sloved_problems.all().count()
            user.save()
        except:
            print("failure")
            break
    else:
        print("success")

if __name__ == "__main__":

    loadProblems()
    loadContests()