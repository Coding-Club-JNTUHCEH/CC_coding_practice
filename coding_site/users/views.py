from django.contrib.admin.sites import DefaultAdminSite
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import time
import requests
from .models import UserProfile
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            cf = cleanFormData(form)

            user = User.objects.create_user(username= cf['username'], password= cf['raw_password'], email = cf['email'])
            
            user_profile = UserProfile.objects.create(user = user,name = cf['name'],codeForces_username =cf['CodeForces_Username'], year = cf['year'],rating = getRating(cf["CodeForces_Username"]))
            user_profile.add_solvedProblems()

            user = authenticate(request, username=cf['username'], password=cf['raw_password'])
            if user is not None:
                login(request, user)
            return redirect('/dasboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request): 
    if(request.method=="GET"):
        context={}

        return render(request,"login.html",context)
    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        context={}
        if user is not None:
            login(request,user)
            return redirect('/dasboard')

        context={"message":"Invalid Login Credentials"}
        
        return render(request,"login.html",context)


@login_required
def profile_view(request,*args,**kwargs):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            return HttpResponseRedirect('/users/'+username)
            
        else:
            username = kwargs["username"]
    except:
        username = request.user.username
    try:
        user = User.objects.get(username = username)
    except:
        return  render(request, "hello.html")
    user_details = UserProfile.objects.get(user = user)
    code_forces_info = fetchCFProfileInfo(user_details.codeForces_username)
    context={
            "username"          : user.username ,  
            "name"              : user_details.name ,
            "codeForces_name"   : user_details.codeForces_username , 
            "year"              : user_details.year ,
            "codeforces"        : code_forces_info
        }
        
    return  render(request, "profile.html", context = context)



def logout_view(request,*args,**kwargs):
    logout(request)
    return redirect(reverse(login_view))

def fetchCFProfileInfo(username):
    url = 'https://codeforces.com/api/user.info?handles='+str(username)

    JSONdata = fetchURL(url)
    if JSONdata["status"] != 'OK' :
        return {}
    profile_0 = JSONdata["result"][0]
    lastOnline = convertTime(profile_0["lastOnlineTimeSeconds"])

    p = {
        "rating"    :   profile_0["rating"] , 
        "maxRating" :   profile_0["maxRating"],
        "titlePhoto":   profile_0["titlePhoto"],
        "lastonline" :  lastOnline
    }

    return p

def convertTime(seconds):
    now = time.time()
    diff  = now - seconds
    return diff/3600
    


def cleanFormData(form):
    profile={}
    profile['username'] = form.cleaned_data.get('username')
    profile['raw_password'] = form.cleaned_data.get('password1')
    profile['name'] = form.cleaned_data.get('name')
    profile['CodeForces_Username'] = form.cleaned_data.get('CodeForces_Username')
    profile['email'] = form.cleaned_data.get('email')
    profile['year'] = form.cleaned_data.get('year')

    return profile


def getRating(username):
    try:
        return fetchCFProfileInfo(username)["rating"]
    except:
        return 800


def fetchURL(url):
    data = requests.get(url)
    return data.json()