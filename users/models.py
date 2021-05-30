
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from index.models import Problem

from .codeforces_API import getSolvedProblems
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
        profile = UserProfile(
            
        )
        return profile

    def add_solvedProblems(self):

        solvedProblems = getSolvedProblems( username = self.codeForces_username )
        for problem in solvedProblems:
            self.add_solvedProblem(problem)

    def updated_solvedProblems(self):
        solvedProblems  = getSolvedProblems( username = self.codeForces_username )
        remaing         = len(solvedProblems) - self.sloved_problems.count()
        for p in range(remaing):
            self.add_solvedProblem(solvedProblems[p])
        return self.sloved_problems


    def add_solvedProblem(self,problem):
        if problem["verdict"] == 'OK' :
            try:
                contestID  = problem["problem"]["contestId"]
                index      = problem["problem"]["index"]
            except:
                return
            try:
                
                self.sloved_problems.add(Problem.objects.get(contestID=contestID, index=index))
            except:
                self.addNewProblemtoDB(problem["problem"])
                self.sloved_problems.add(Problem.objects.get(contestID=contestID, index=index))
    

    def addNewProblemtoDB(self,problem):
        p_db = Problem.create(problem)
        p_db.save()
        p_db.link_tags(problem["tags"])

    @staticmethod
    def updateRatings(updated_data):
        status = False
        for user in updated_data:
            user_p = UserProfile.objects.get(codeForces_username = user["handle"])
            user_p.rating = user["rating"]
            user_p.save()
            status = True

        return UserProfile.objects.all(),status