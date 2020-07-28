from django.contrib.auth.models import AbstractUser#
from django.db import models
from django.utils import timezone
import datetime

class User(AbstractUser):
    bugsPosted = models.IntegerField(default=0)
    bugsSolved = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.id} {self.username}"
    def SerialiseUser(self):
        return {
        "solved": self.bugsSolved, "posted": self.bugsPosted, "username": self.username
        }   

class Bug (models.Model):
    status = models.CharField(max_length=50) #will be in 1 of 5 states, unclaimed, claimed, processing, testing, closed
    priority = models.CharField(max_length=10) #so the user can give the bug a presumed priority (low, med, high)
    title = models.CharField(max_length=50) #brief description of the bug 
    description = models.CharField(max_length=500) # full description of the issue
    location = models.CharField( max_length=50) #where the issue is located (file, program)
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField( blank=True, null=True)
    image = models.ImageField() # bootstrap has class img-fluid
    score = models.IntegerField(default=0)

    #no slugfield, being able to make a url based on an issue's id will probably impart as much information to a user as an out of context title
    def __str__(self):
        return f"Bug {self.id}" #short representation because any of these fields could be potentially very long

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id: #if an id doesnt exist for this bug, then it has just been created
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Bug, self).save(*args, **kwargs)
    
    def serialiseBug(self):
        return{
            "id": self.id,
            "title": self.title,
            "modified": self.modified,
            "usersOnBug": self.usersOnBug
        }

   
class Comment (models.Model): #1-1 relationship for a user making a comment on a bug
    user        = models.ForeignKey("User", on_delete=models.PROTECT,  related_name='userComment')
    bug         = models.ForeignKey("Bug", on_delete=models.CASCADE, related_name='bugComment')
    comment     = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment {self.id} From {self.user.username}, on bug {self.bug.id}"
    def serialiseComment(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "bug": self.bug.id,
            "comment": self.comment
        }

class Follow (models.Model): #gives a relationship between a user and the bugs they are following
    user        = models.ForeignKey("User", on_delete=models.CASCADE,  related_name='followUser')#this user
    bug         = models.ForeignKey("Bug", on_delete=models.CASCADE, related_name='followBug',  blank=True, null=True) # the bugs being followed
    def __str__(self):
        return f"follow {self.id} From {self.user.username}, on bug {self.bug.id} "
    def serialiseFollow(self):
        return{
            "id": self.id,
            "user": self.user,
            "bug": self.bug
        }


class Solver (models.Model): #gives a 1-1 relationship of a user and a bug they are solving, only 1 user per bug
    user        = models.ForeignKey("User", on_delete=models.CASCADE, related_name='solverUser')
    bug         = models.ForeignKey("Bug",  on_delete=models.CASCADE, related_name='solverBug')
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()
    action      = models.CharField(max_length=500, blank=True, null=True) #field to allow a bug fix to be supplied, allowing it as null here but expect a
                                                                #check in html to not actually pass a blank value (this is the fix so why is it null?)
    updates     = models.ManyToManyField("Update", related_name='solverUpdate') #should allow many updates to made by one solver
    result      = models.CharField(max_length=500, blank=True, null=True) #result can be blank in case of awaiting result/ etc
    def __str__(self):
        return f"Solver {self.user.username} on {self.bug.id} current status: {self.bug.status}"
    def serialiseSolver(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "bug": self.bug.id
        }
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id: #if an id doesnt exist for this bug, then it has just been created
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Solver, self).save(*args, **kwargs)
    

class Update(models.Model): #the Solver will be able to post updates about the bug (if user is solver of this bug then x, y)
    solver      = models.ForeignKey("Solver", on_delete=models.CASCADE, related_name='updateSolver')
    text        = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"update #{self.id} from {self.solver.user.username} on bug {self.solver.bug.id}"
    

class Votes (models.Model): #any user can vote on a bug (either for solution or for urgency? or interest)
    user        = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    bug         = models.ForeignKey("Bug", on_delete=models.CASCADE)

  
