from django.db import models
from index.models import Problem
from users.codeforces_API import fetchAllProblems
# from django.apps import apps


class Contest(models.Model):
    contestID       = models.IntegerField(unique=True)
    index           = models.CharField(max_length=5)
    name            = models.CharField(max_length=50)
    type            = models.CharField(max_length=50)
    problems        = models.ManyToManyField(
                        Problem, blank=True, related_name="Problem")
    link            = models.URLField(max_length=200)

    class Meta:
        pass

    @classmethod
    def create(self, *args, **kwargs):
        cleaned_contest = self.cleanContestForDB(args[0])
        p = Contest(
            contestID=cleaned_contest["contestID"],
            index=cleaned_contest["index"],
            name=cleaned_contest["name"],
            type=cleaned_contest["type"],
            link=cleaned_contest["link"],
        )

        return p

    def link_problems(self, problems):
        for problem in problems:
            self.problems.add(problem)

    def cleanContestForDB(contest):

        name = contest["name"]
        typee = 0
        if (name.find("Div. 1") > -1):
            typee = 1
        if (name.find("Div. 2") > -1):
            typee = 2
        if (name.find("Div. 3") > -1):
            typee = 3
        if (name.find("Div. 4") > -1):
            typee = 4

        problems = []
        

        p = {'contestID': contest["id"],
             'index': contest["id"],
             'name': contest["name"],
             'type': typee,
             'problems': problems,
             'link': 'https://codeforces.com/contest/' + str(contest["id"]),
             }
        print(p)
        return p

    def __str__(self) -> str:
        return (str(self.contestID) + self.index + " " + self.name)
