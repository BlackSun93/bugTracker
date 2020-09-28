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
    bugList = Bug.objects.all().order_by('id').filter(status = 'unclaimed') #order bugs by reverse id (oldest bugs first) needs to exclude solved bugs
    try:
        solvedBugsForUserReview = Bug.objects.filter(status = 'solved', poster = request.user, fixed = False ).order_by('-modified') 
        #if there are solved bugs that the user posted, render them at the top of the page in most recently solved first order
        return render(request, "bugtrack/index.html", {
        "bugList": bugList, "solvedList": solvedBugsForUserReview
        })
    except:
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
    #profile page should show posted bugs from user (maybe just last 10 bugs?) last 5 bugs solved by user, total posted, total solved
    thisUser = User.objects.get(username = username) #gets the user object of this user for the profile
    thisUserPostedBugs = Bug.objects.filter(poster = thisUser) # all bugs where this user is the poster
    thisUserSolvedBugs = Bug.objects.filter(bugSolver__user = thisUser, fixed = True) # all instances where this user is the bug solver and bug is fixed
    usersSolvedBugs = Bug.objects.filter(poster__username=thisUser, fixed = True) #all the bugs this user poster which are fixed
    thisUserCurrentBugs = Bug.objects.filter(poster = thisUser, fixed = False).exclude(status = 'solved')
    thisUserSolving = Bug.objects.filter(bugSolver__user = thisUser, fixed = False)
    solved = thisUser.bugsSolved.count()
    posted = Bug.objects.filter(poster = thisUser).count()

    return render(request, "bugtrack/profile.html", {
        "posted": thisUserPostedBugs, "solved": thisUserSolvedBugs, "current": thisUserCurrentBugs, "user":thisUser, "solvednum": solved,
        "postednum":posted, "solving":thisUserSolving
    })

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
    newBug = Bug(title=bugTitle, location = bugLocation, description = bugDesc, priority = bugPriority, status = "unclaimed", poster = request.user)
    
    newBug.save()
    #print(Bug.objects.all()) commented out because it is showing new bugs as they're created
    return JsonResponse({"message": "bug sent successfully."}, status=201)

def bugPage (request, bugId):
    thisBug = Bug.objects.get(id=bugId)
    updates = thisBug.updates.all().order_by('-id')
    if request.user == thisBug.poster: #this means notifications will only set to read if the bug's poster looks at the page
        for update in updates:
            update.notifRead = True
            update.save() #when a bug's page is opened, it iterates through all the updates and sets them all to read
        #I've done it this way because there could potentially be many updates on one bug and it makes sense that once the bugpage is opened
        #the user will be able to see all of the updates
    #print(thisBug.updates)
    #print(updates)
    
    if thisBug.solverBug.exists(): #if this bug has a solver, pass solver info into the template
        solver = thisBug.solverBug.filter().first() #get solver object
        solver = solver.serialiseSolver() #JSON it
    else:
        solver = None
    jsBug = thisBug.serialiseBug() #JSON the bug
    jsBug = json.dumps(jsBug, default=str)
    print(thisBug.bugSolver)
    try:
        return render(request, "bugtrack/bugPage.html", {
         "bug": thisBug, "jsBug":jsBug,  "solver" : solver, "updates": updates
        })
    except:
        return render(request, "bugtrack/bugPage.html", {
         "bug": thisBug, "jsBug":jsBug,  "solver" : solver
        })


    #else: #if this bug doesn't have a solver yet
    #    jsBug = thisBug.serialiseBug()
    #    jsBug = json.dumps(jsBug, default=str)
     
    #    return render(request, "bugtrack/bugPage.html", {
    #    "bug": thisBug, "jsBug": jsBug #JsonResponse([thisBug.serialiseBug()], safe=False)# #bug is the bug object from the DB, jsBug is a json representation (no desc)
    #    })
@csrf_exempt
def newSolver (request):
    if  request.method != 'POST':
        return JsonResponse({"message": "Get request."}, status=201)
    data = json.loads(request.body)
    userId = data.get('userId')
    bugId= data.get('bugId')
    
    thisBug = Bug.objects.get(id=bugId)
    thisUser = User.objects.get(id=userId)
    #thisBug.poster.notification = True #notifies the bug's poster (as a bug they posted now has a solver)
    #thisBug.poster.notifType = 'notifSolver'
    #thisBug.poster.save()
    print(thisBug)
    print(thisUser)
    newSolver = Solver(user=thisUser, bug=thisBug)
    
    newSolver.save()
    newUpdate = Update(solver = newSolver, notifRead=False, notifType='notifSolver')
    newUpdate.save()
    thisBug.updates.add(newUpdate)
    thisBug.status = 'claimed'
    thisBug.bugSolver = newSolver
    #thisBug.notifType = 'notifSolver'
    thisBug.newNotif = True
    thisBug.save()
    print(newSolver)
    jsonBug = json.dumps(thisBug, default=str)
    return JsonResponse(jsonBug, safe=False) # I assume if i made a fetch
    #inside of the bugPage.js then I would be able to access the updated thisBug data

@csrf_exempt
def newUpdate(request): #update has to create new update object, add update to solver, update bug status
    if  request.method != 'POST':
        return JsonResponse({"message": "Get request."}, status=201)
    ##### GET DATA FROM FRONTEND #####
    data = json.loads(request.body)
    update = data.get('newUpdate')
    newStatus = data.get('newStatus')
    bugId = data.get('bugId')
    thisBug = Bug.objects.get(id=bugId) #get the bug the update is being posted on
    print(thisBug)
    thisSolver = Solver.objects.get(user = request.user, bug = thisBug) #get the user who has posted the update
    
    ##### UPDATE OBJECTS ######
    #addUpdate(newUpdate, thisBug, thisSolver)
    newUpdate = Update(solver = thisSolver, text = update, notifRead=False, notifType='notifUpdate') #create update object
    newUpdate.save()
    thisBug.status = newStatus #updates the bug's status as per the dropdown menu
    thisBug.updates.add(newUpdate) #adds update to the solver object, should add updates to the bug 
    print(newUpdate)
    #thisBug.poster.notification = True
    #thisBug.poster.notifType = 'notifUpdate'
    #thisBug.poster.save()
    thisBug.newNotif = True
    thisBug.save()
    print(newStatus)
    if newStatus == 'solved': #set update's status to solved here?
        newUpdate.status = 'solved'
        newUpdate.notifRead = False
        newUpdate.notifType = 'notifSolved'
        newUpdate.save() #this only changes the update status if it's solved
        thisSolver.result = 'solved'
        print(newUpdate)
        print(newUpdate.notifType)
        #thisBug.poster.notification = True
       # thisBug.poster.notifType = 'notifSolved'
       # thisBug.poster.save()
        return JsonResponse([newUpdate.serialiseUpdate()], safe=False)

    elif newStatus == 'unclaimed':
       
       # thisBug.poster.notifType = 'notifSolverQuit'
       # thisBug.poster.notification = True
      #  thisBug.poster.save()
        newUpdate.notifRead = False
        newUpdate.notifType = 'notifSolverQuit'
        newUpdate.save() #this only changes the update status if it's solved
        thisSolver.delete() # have to clear the solver object
        print(newUpdate)
        print(newUpdate.notifType)
        print("solver deleted")
        return JsonResponse([newUpdate.serialiseUpdate()], safe=False)

    else:
        print(newUpdate)
        print(thisBug.updates.all())
        return JsonResponse([newUpdate.serialiseUpdate()], safe=False)

@csrf_exempt
def bugSolved(request, bugId):
    data = json.loads(request.body)
    userData = data.get('userId')
    thisBug = Bug.objects.get(id=bugId) #the solved bug
    thisUser = User.objects.get(id=userData) #the user who accepted the fix to the bug
    if thisUser != request.user:
        return JsonResponse({"message": "You are not the user who posted this bug"}, status=201)
    thisBug.fixed = True
    thisBug.status = 'finished'
    
    #thisBug.poster.notifType = 'notifFixed'
   # thisBug.poster.notification = True
    #thisBug.poster.save()
    solver = thisBug.bugSolver.user #gets the user who solved the bug
    thisSolver = thisBug.bugSolver #gets this solver object
    solver.bugsSolved.add(thisSolver) #adds this object to the bugs solved of the solving user
    solver.save()
    print(thisBug.fixed)
    newUpdate = Update(solver = thisSolver, notifRead=False, notifType='notifFixed')
    newUpdate.save()
    thisBug.updates.add(newUpdate)
    thisBug.newNotif = True
    thisBug.save()
    
    jsonBug = json.dumps(thisBug, default=str)
    return JsonResponse(jsonBug, safe=False)

@csrf_exempt
def bugNotSolved(request, bugId):
    #kind of need the user to be able to give feedback on WHY they're saying the solution wasnt good enough
    #i want the user to be able to decide to make it unclaimed or to keep the current solver
    #user should be able to go to their bug at anytime and change it to 'unclaimed' tbh
    thisUser = request.user #the user who accepted the fix to the bug
    if thisUser != request.user:
        return JsonResponse({"message": "You are not the user who posted this bug"}, status=201)
    print(json.loads(request.body))
    data = json.loads(request.body)
    updateStatus = data.get('updateStatus')
    reasonText = data.get('reasonText')
    thisBug = Bug.objects.get(id=bugId) #the solved bug
    thisBug.status = updateStatus
    thisSolver = thisBug.bugSolver
    newUpdate = Update(solver = thisSolver, notifRead=False, notifType='notifNotSolved') #makes an update to say the bug wasn't solved
    newUpdate.save()
    thisBug.updates.add(newUpdate)
    thisBug.newNotif = True
    
    thisBug.save()
   # thisBug.poster.notification = True
   # thisBug.poster.notifType = 'notifUpdate'
   # thisBug.poster.save()
    #need to find most recent update (as last update will be when the bug was solved)
    lastUpdate = thisBug.updates.filter(notifType='notifUpdate').first() #needs to be the last 
    newUpdateComment = UpdateComment(user = thisUser, update = lastUpdate, text = reasonText)
    
    newUpdateComment.save()
    lastUpdate.comment=newUpdateComment
    lastUpdate.save()
    thisBug = json.dumps(thisBug, default=str)
    #create an update with the user and the reasontext
    return  JsonResponse(thisBug, safe=False) #solver not serialiseable

def finishedBugList (request):
    finishedBugs = Bug.objects.filter(fixed = True).order_by('-id') #all the bugs where user has said the solution worked
    return render(request, "bugtrack/index.html", {
        "bugList": finishedBugs, "header":'finishedBugs' #render a version of the index page, header is passed so main.js knows we only want fixed bugs
        })

def notifications (request):
    thisUser = request.user
    #bugsUserPosted = Bug.objects.filter(poster = thisUser)
    unreadBugs = Bug.objects.filter(newNotif= True, poster = thisUser).order_by('-modified') # will get all the bugs with unread notifications on them
    #could even sort the notification types on this side - BUT cant sort by time order if they are sorted here
    #firstNotif = unreadNotifs.first()
    print(unreadBugs)
    #print(firstNotif.updates.all())
    #firstUp = firstNotif.updates.first()
   # print(firstUp.notifType)

    updates = Update.objects.filter(notifRead= False, solver__bug__poster = thisUser)
    
    print(updates)
    
    #for bug in unreadBugs.all():
    #    updates = bug.updates.all()
    #    print(updates) #gets and stores 1 bug's updates
    

    return render(request, "bugtrack/notifications.html" , {
            "notifications": updates
        })

#def notificationPage (request):
    #have to get all updates for bugs this user has posted
    #find some way to alert user to this section if there is something not read by this user, might have to add a  'read by user' var to class
    #would add this in model for updates
 #   return render(request, "bugtrack/notification.html", {

#    })





#### function to take an update, a bug, save the update and it it to the bug ##### MAKE SURE THI WORKS
#def addUpdate(newUpdate, thisBug, thisSolver):
   
   # return print (newUpdate.id + " update added")

#def hello(word):
#    return print(word)

    




