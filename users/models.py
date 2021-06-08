
from django.db import models
from django.contrib.auth.models import User

from index.models import Problem
from API_manager import codeforces_API
# Create your models here.


class UserProfile(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=30, default="forgot")
    codeForces_username     = models.CharField(max_length=30)
    year                    = models.IntegerField(help_text='Year of Admission')
    rating                  = models.IntegerField(default=800)
    sloved_problems         = models.ManyToManyField(
                                Problem, blank=True, related_name="UserSolved")
    not_sloved_problems     = models.ManyToManyField(
                                Problem, blank=True, related_name="UserNotSolved")
    friends                 = models.ManyToManyField(
                                "UserProfile", blank=True, related_name="friend")

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return "{}".format(self.codeForces_username)

    @classmethod
    def create(cls, *args, **kwargs):
        profile = UserProfile(

        )
        return profile

    def add_solvedProblems(self):

        solvedProblems = codeforces_API.getSolvedProblems(username=self.codeForces_username)
        for problem in solvedProblems:
            self.add_solvedProblem(problem)

    def updated_solvedProblems(self):
        problems    = codeforces_API.getSolvedProblems(username=self.codeForces_username)
        if problems == []:
            return self.sloved_problems
        remaing     = len(problems) - self.sloved_problems.count() - \
            self.not_sloved_problems.count()
        for p in range(remaing):
            if problems[p]["verdict"] == 'OK':
                prob    = problems[p]["problem"]
                problem = Problem.objects.get(contestID = prob["contestId"] , index = prob["index"])
                self.sloved_problems.add(problem)
                if prob in self.not_sloved_problems.all():
                        self.not_sloved_problems.remove(problem)
        return self.sloved_problems

    def updated_not_solvedProblems(self):
        problems    = codeforces_API.getSolvedProblems(username=self.codeForces_username)
        if problems == []:
            return self.sloved_problems
        remaing     = len(problems) - self.sloved_problems.count() - \
            self.not_sloved_problems.count()
        for p in range(remaing):
            if problems[p]["verdict"] != 'OK' and problems[p]["problem"] not in self.sloved_problems.all():
                prob = problems[p]["problem"]
                problem = Problem.objects.get(contestID = prob["contestId"] , index = prob["index"])
                self.not_sloved_problems.add(problem)
        
        return self.not_sloved_problems

    def add_solvedProblem(self, problem):
        if problem["verdict"] == 'OK' or problem["verdict"] == 'WRONG_ANSWER':
            try:
                contestID   = problem["problem"]["contestId"]
                index       = problem["problem"]["index"]
            except:
                return

            try:
                problem1 = Problem.objects.get(
                            contestID=contestID, index=index)

                if problem["verdict"] == 'OK':
                    self.sloved_problems.add(problem1)
                else:
                    if problem not in self.sloved_problems.all():
                        self.not_sloved_problems.add(problem1)
            except:
                self.addNewProblemtoDB(problem["problem"])
                problem1 = Problem.objects.get(
                    contestID=contestID, index=index)

                if problem["verdict"] == 'OK':
                    if problem in self.not_sloved_problems.all():
                        self.not_sloved_problems.remove(problem1)
                    self.sloved_problems.add(problem1)
                else:
                    if problem not in self.sloved_problems.all():
                        self.not_sloved_problems.add(problem1)

    def addNewProblemtoDB(self, problem):
        p_db = Problem.create(problem)
        p_db.save()
        p_db.link_tags(problem["tags"])

    def getFriendsList(self):
        fr_list = []
        for friend in self.friends.all():
            fr_list.append(friend.user.username)
        return fr_list
        
    @staticmethod
    def updateRatings(updated_data):
        status = False
        for user in updated_data:
            user_p = UserProfile.objects.get(
                        codeForces_username=user["handle"])
            user_p.rating = user["rating"]
            user_p.save()
            status = True

        return UserProfile.objects.all(), status
    
    def __str__(self) -> str:
        return self.name
