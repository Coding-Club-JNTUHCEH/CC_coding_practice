from django.db import models
from index.models import Problem
from users.codeforces_API import fetchAllProblems
# from django.apps import apps
# Problem = apps.get_model('index', 'Problem')

# Create your models here.

# class Tag(models.Model) :
#     tag_name    = models.CharField(max_length=32)
#     tag_title   = models.CharField(max_length=64, default="did not set")

#     class Meta:
#         ordering = ['tag_name']

#     def __str__(self) -> str:
#         return self.tag_name


class Contest(models.Model):
    contestID = models.IntegerField()
    index = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    # rating = models.IntegerField(default=0)
    problems = models.ManyToManyField(
        Problem, blank=True, related_name="Problme")
    # problems = models.ForeignKey('index.Problem', on_delete=models.CASCADE,)
    link = models.URLField(max_length=200)
    # tags = models.ManyToManyField(Tag,blank=True,related_name="Problme")

    class Meta:
        unique_together = ['contestID', 'index']

    @classmethod
    def create(self, *args, **kwargs):
        cleaned_contest = self.cleanContestForDB(args[0])
        p = Contest(
            contestID=cleaned_contest["contestID"],
            index=cleaned_contest["index"],
            name=cleaned_contest["name"],
            # problems=cleaned_contest["problems"],
            type=cleaned_contest["type"],
            link=cleaned_contest["link"],
        )

        return p

    # def link_tags(self,tags):
    #     for tag in tags:
    #         tag_obj,created = Tag.objects.get_or_create(tag_name = tag)
    #         self.tags.add(tag_obj)

    def cleanContestForDB(contest):
        # if 'rating' in problem:
        #     rating = problem["rating"]
        # else:
        #     rating = 0
        # if 'tags' in problem:
        #     tags = problem["tags"]
        # else:
        #     tags = []

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

        # problems = Problem.objects.filter(
        #     index=contest["id"]).order_by("index")

        p = {'contestID': contest["id"],
             'index': contest["id"],
             'name': contest["name"],
             'type': typee,
             #  'problems': problems,
             'link': 'https://codeforces.com/contest/' + str(contest["id"]),
             }
        print(p)
        return p

    def __str__(self) -> str:
        return str(self.contestID) + self.index + " " + self.name

    def add_problems(self):

        # problems =getProblems(self.codeForces_username)
        problems = Problem.objects.filter(
            contestID=self.contestID).order_by("index").values()
        print(problems)
        print("Yea!!")

        for problem in problems:
            print(problem)
            self.add_problem(problem)

    def add_problem(self, problem):

        print("inside add_problem")

        try:
            contestID = problem["contestId"]
            # index = problem["index"]
        except:
            return

        try:
            self.problems.add(Problem.objects.get(
                contestID=contestID))
        except:
            self.addNewProblemtoDB(problem)
            self.problems.add(Problem.objects.get(
                contestID=contestID))

    def addNewProblemtoDB(self, problem):
        p_db = Problem.create(problem)
        p_db.save()
        p_db.link_tags(problem["tags"])
