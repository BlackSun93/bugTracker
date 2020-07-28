import json
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import *


def index(request): 
    #default view should display all the bugs, so I will get them here and pass them into index.html
    #need to exclude bugs that have been taken on by someone (to prevent multiple users takng them on)
    bugList = Bug.objects.all().order_by('-id') #order bugs by reverse id (newest bugs first)
    return render(request, "bugtrack/index.html", {
        "bugList": bugList
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bugtrack/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bugtrack/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bugtrack/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bugtrack/register.html")

def profile(request, username):
    return render(request, "bugtrack/profile.html")

@csrf_exempt
def createBug(request):
    if  request.method != 'POST':
        return JsonResponse({"message": "Get request."}, status=201)
    print('creating bug')
    data = json.loads(request.body) #data from the form in index.html
    print(data)
    bugTitle = data.get('title')
    bugLocation = data.get('location')
    bugDesc = data.get('description')
    bugPriority=data.get('priority')
    newBug = Bug(title=bugTitle, location = bugLocation, description = bugDesc, priority = bugPriority, status = "unclaimed")
    
    newBug.save()
    #print(Bug.objects.all()) commented out because it is showing new bugs as they're created
    return JsonResponse({"message": "bug sent successfully."}, status=201)

def bugPage (request, bugId):
    thisBug = Bug.objects.get(id=bugId)

    return render(request, "bugtrack/bugPage.html", {
        "bug": thisBug
    })

    




