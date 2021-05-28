from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.http import HttpResponse

from users.codeforces_API import fetchAllUsers

# Create your views here.

def leaderboard_view(request):
    
    users_list  = UserProfile.objects.values_list('codeForces_username')
    users_str = ""
    users = []
    rank = 1
    for user in users_list:
        users_str += user[0] + ";"
    
    users_cfProfile = fetchAllUsers(users_str)

    users_p,status = UserProfile.updateRatings(users_cfProfile)
    for user_p in users_p:
        users.append(extract_leaderboardData(user_p,rank))
        rank+=1
        
        
    context ={ "users" : users, "status" : status }
    
    return render(request,"leaderboard.html",context=context)


def extract_leaderboardData(user,rank):
    return {
        "username" : user.user.username ,
        "rating"   : user.rating,
        "rank"     : rank

    }
