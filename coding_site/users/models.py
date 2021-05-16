from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import requests
from index.models import Problem


# Create your models here.

class UserProfile(models.Model): 
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    name                = models.CharField(max_length=30, default="forgot")
    codeForces_username = models.CharField(max_length=30)
    year                = models.IntegerField(help_text='Year of Admission')
    rating              = models.IntegerField(default=800)
    sloved_problems     = models.ManyToManyField(Problem,blank=True,related_name="UserSolved")

    class Meta:
        ordering = ['-rating']
    
    def __str__(self):
        return "{}".format(self.codeForces_username)

    @classmethod
    def create(cls,*args, **kwargs):
        profile=UserProfile(
            
        )
        return profile

    def add_solvedProblems(self):
        url = "https://codeforces.com/api/user.status?handle="+str(self.codeForces_username)
        data = requests.get(url)
        JSONdata = data.json()
    
        if JSONdata["status"]!= 'OK':
            return False
        for problem in JSONdata["result"]:
            self.add_solvedProblem(problem)
        return True
    
    def add_solvedProblem(self,problem):
        if problem["verdict"] == 'OK' :
            contestID  = problem["problem"]["contestId"]
            index      = problem["problem"]["index"]
            try:
                
                self.sloved_problems.add(Problem.objects.get(contestID=contestID, index=index))
            except:
                self.addNewProblemtoDB(problem["problem"])
                self.sloved_problems.add(Problem.objects.get(contestID=contestID, index=index))
    

    def addNewProblemtoDB(self,problem):
        p_db = Problem.create(problem)
        p_db.save()
        p_db.link_tags(problem["tags"])
    