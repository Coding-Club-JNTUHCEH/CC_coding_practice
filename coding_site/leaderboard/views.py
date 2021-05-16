from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from users.models import UserProfile

# Create your views here.
@login_required
def leaderboard_view(request):
    
    users_list  = UserProfile.objects.values_list('codeForces_username')
    users_str = ""
    for user in users_list:
        users_str += user[0] + ";"
    
    url = "https://codeforces.com/api/user.info?handles="+ users_str
    data = requests.get(url)
    JSONdata = data.json()
    context ={}
    return render(request,"leaderboard.html",context=context)