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
    
    if thisBug.solverBug.exists(): #if this bug has a solver, pass solver info into the template
        solver = thisBug.solverBug.get() #get solver object
        solver = solver.serialiseSolver() #JSON it
        jsBug = thisBug.serialiseBug() #JSON the bug
        jsBug = json.dumps(jsBug, default=str)
        print(thisBug.bugSolver)
        return render(request, "bugtrack/bugPage.html", {
        "bug": thisBug, "jsBug":jsBug,  "solver" : solver
    })

    else: #if this bug doesn't have a solver yet
        jsBug = thisBug.serialiseBug()
        jsBug = json.dumps(jsBug, default=str)
     
        return render(request, "bugtrack/bugPage.html", {
        "bug": thisBug, "jsBug": jsBug #JsonResponse([thisBug.serialiseBug()], safe=False)# #bug is the bug object from the DB, jsBug is a json representation (no desc)
        })
@csrf_exempt
def newSolver (request):
    if  request.method != 'POST':
        return JsonResponse({"message": "Get request."}, status=201)
    data = json.loads(request.body)
    userId = data.get('userId')
    bugId= data.get('bugId')
    
    thisBug = Bug.objects.get(id=bugId)
    thisUser = User.objects.get(id=userId)
    print(thisBug)
    print(thisUser)
    newSolver = Solver(user=thisUser, bug=thisBug)
    newSolver.save()
    thisBug.status = 'claimed'
    thisBug.bugSolver = newSolver
    thisBug.save()
    print(newSolver)
    return JsonResponse([thisBug.serialiseBug()], safe=False) # I assume if i made a fetch
    #inside of the bugPage.js then I would be able to access the updated thisBug data

@csrf_exempt
def newUpdate(request): #update has to create new update object, add update to solver, update bug status
    if  request.method != 'POST':
        return JsonResponse({"message": "Get request."}, status=201)
    ##### GET DATA FROM FRONTEND #####
    data = json.loads(request.body)
    update = data.get('newUpdate')
    newStatus = data.get('newStatus')
    thisSolver = Solver.objects.get(user = request.user) #get the user who has posted the update
    thisBug = thisSolver.bug #get the bug the update is being posted on
    ##### UPDATE OBJECTS ######
    if newStatus == 'solved':
        

    else:
        thisBug.status = newStatus #updates the bug's status as per the dropdown menu
        thisBug.save()
        newUpdate = Update(solver = thisSolver, text = update) #create update object
        newUpdate.save()
        print(newUpdate)
        thisSolver.updates.add(newUpdate) #adds update to the solver object, should add updates to the bug 
        thisSolver.save()
        print(thisSolver.updates.all())
        return JsonResponse([newUpdate.serialiseUpdate()], safe=False)

    




