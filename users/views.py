from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from API_manager import codeforces_API
from .models import UserProfile
from .forms import SignUpForm, EditProfileForm


def landing(request):
    return render(request, 'landing.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form = SignUpForm()
                return render(request, 'signup.html', {'form': form, 'msg': "Error while saving please Try again"})

            user = authenticate(
                    request, username=form.cleaned_data["username"], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            return redirect('/dasboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if(request.method == "GET"):
        context = {}
        return render(request, "login.html", context)

    if(request.method == "POST"):
        print(request.POST)
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        user        = authenticate(request, username=username, password=password)
        context = {}
        if user is not None:
            login(request, user)
            return redirect('/dasboard')

        context = {"message": "Invalid Login Credentials"}

        return render(request, "login.html", context)


@login_required
def profile_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST.get('username')
        return HttpResponseRedirect('/users/'+username)

    else:
        try:
            username = kwargs["username"]
        except:
            return HttpResponseRedirect('/users/'+request.user.username)

    try:
        user = User.objects.get(username=username)
    except:
        return render(request, '404.html', {})

    user_details                = UserProfile.objects.get(user=user).__dict__
    user_details["username"]    = user.username
    user_details["codeforces"]  = codeforces_API.fetchCFProfileInfo(
                                    user_details["codeForces_username"])
    if user_details["codeforces"] != {}:
        UserProfile.objects.filter(user=user).update(
            rating=user_details["codeforces"]["rating"])
    else:
        user_details["server_down"] = True

    if request.user.id == user_details["user_id"]:
        user_details["friends"]             = UserProfile.objects.get(user = request.user ).getFriendsList()
        user_details["view_friends"]        = True
        user_details["edit_profile"]        = True
    else:
        friends = UserProfile.objects.get(user = request.user).friends.all()
        if UserProfile.objects.get(user = user) in friends:
            user_details["friend"] = True

    return render(request, "profile.html", context=user_details)


@login_required
def editProfile_view(request):

    if request.method == 'POST':
        form = EditProfileForm( request.POST, instance=request.user )
       
        if form.is_valid():
            
            form.save()
            
            return redirect(reverse('profile'))
        else:
            return render(request, 'editprofile.html', {'form': form, 'msg': "Error while saving please Try again"})
    else:
        user_profile    = UserProfile.objects.get(user=request.user).__dict__
        form            = EditProfileForm(instance=request.user, initial=user_profile)
        context         = {'form': form}
        return render(request, 'editprofile.html', context)


@login_required
def changePassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('profile'))

        else:
            return render(request, 'editprofile.html', {'form': form, 'msg': "Error while saving please Try again"})
    else:
        form    = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'change_password.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse(login_view))


def help_CF_view(request):
    return render(request, 'help_CF.html')


def add_friend_JSON(request, *args, **kwargs):
    print("received add request")
    
    username = kwargs["username"]
    try:
        friend = UserProfile.objects.get(user = User.objects.get(username = username))
        UserProfile.objects.get(user = request.user).friends.add(friend)
        return JsonResponse({'status': 0 })
    except:
        return JsonResponse({'status': 1 })

def remove_friend_JSON(request, *args, **kwargs):
    print("remove request received")
    username = kwargs["username"]
    try:
        friend = UserProfile.objects.get(user = User.objects.get(username = username))
        UserProfile.objects.get(user = request.user).friends.remove(friend)
        return JsonResponse({'status': 0 })
    except:
        return JsonResponse({'status': 1 })

def find_users_JSON(request, *args, **kwargs):
    username    = kwargs["username"]
    users       = User.objects.filter(username__contains = username)
    usernames   = []
    for user in users:
        usernames.append(user.username)
    
    return JsonResponse({'usernames': usernames })
