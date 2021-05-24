from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from users.models import UserProfile

# Create your views here.

def leaderboard_view(request):
    
    users_list  = UserProfile.objects.values_list('codeForces_username')
    users_str = ""
    for user in users_list:
        users_str += user[0] + ";"
    
    url = "https://codeforces.com/api/user.info?handles="+ users_str
    data = requests.get(url)
    JSONdata = data.json()
    if JSONdata["status"] != "OK" :
        pass
    else:
        users = []
        rank = 1
        for user in JSONdata["result"]:
            user_p = UserProfile.objects.get(codeForces_username = user["handle"])
            user_p.rating = user["rating"]
            user_p.save()
            users.append({
                            "username" : user_p.user.username ,
                            "rating"   : user_p.rating,
                            "rank"     : rank
                        })
            rank+=1
    
    context ={ "users" : users }
    return render(request,"leaderboard.html",context=context)

