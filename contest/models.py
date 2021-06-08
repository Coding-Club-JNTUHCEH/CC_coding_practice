from django.db import models

from index.models import Problem



class Contest(models.Model):
    contestID       = models.IntegerField( unique=True )
    index           = models.CharField( max_length=5 )
    name            = models.CharField( max_length=50 )
    type            = models.CharField( max_length=50 )
    problems        = models.ManyToManyField( Problem, blank=True, related_name="Problem" )
    link            = models.URLField( max_length=200 )
    empty           = models.IntegerField(default=0 )
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


    def cleanContestForDB(contest):

        name    = contest["name"]
        type   = 0
        if (name.find("Div. 4") > -1):
            type = 4
        elif (name.find("Div. 3") > -1):
            type = 3
        elif (name.find("Div. 2") > -1):
            type = 2
        elif (name.find("Div. 1") > -1):
            type = 1

        p = {'contestID': contest["id"],
             'index': contest["id"],
             'name': contest["name"],
             'type': type,
             'link': 'https://codeforces.com/contest/' + str(contest["id"]),
             }
        return p

    def __str__(self) -> str:
        return (str(self.contestID) + " " + self.name)
