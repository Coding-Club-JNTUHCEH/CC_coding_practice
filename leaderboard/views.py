from django.shortcuts import render

from API_manager import codeforces_API
from users.models import UserProfile
from . import services


# Create your views here.

def leaderboard_view(request):
    
    users_list  = UserProfile.objects.values_list('codeForces_username')
    users_str = ""
    users = []
    rank = 1
    usernames=[]
    for user in users_list:
        # print(user[0])
        usernames.append(user[0])
        users_str += user[0] + ";"
    print("in views")
    
    users_cfProfile = codeforces_API.fetchAllUsers(users_str)
    updated_data = zip(users_cfProfile,usernames)
    users_p,updated = UserProfile.updateRatings(updated_data)
    for user_p in users_p:
        users.append(services.extract_leaderboardData(user_p,rank))
        rank+=1
        
    context ={ "users" : users, "updated" : updated }
    if users_cfProfile == []:
        context["server_down"] = True
        
    return render(request,"leaderboard.html",context=context)
