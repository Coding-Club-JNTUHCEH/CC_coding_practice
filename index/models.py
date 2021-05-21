from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Tag(models.Model) :
    tag_name    = models.CharField(max_length=32)
    # tag_title   = models.CharField(max_length=64, default="did not set")

    class Meta:
        ordering = ['tag_name']

    def __str__(self) -> str:
        return self.tag_name


class Problem(models.Model):
    contestID = models.IntegerField()
    index = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    link = models.URLField(max_length=200)
    tags = models.ManyToManyField(Tag,blank=True,related_name="Problme")

    class Meta:
        unique_together = ['contestID', 'index']

    @classmethod
    def create(self,*args, **kwargs):
        cleaned_problem = self.cleanProblemForDB(args[0])
        p = Problem(
            contestID   = cleaned_problem["contestID"],
            index       = cleaned_problem["index"],
            name        = cleaned_problem["name"],
            rating      = cleaned_problem["rating"],
            link        = cleaned_problem["link"],
        )

        return p
    
    
    def link_tags(self,tags):
        for tag in tags:
            tag_obj,created = Tag.objects.get_or_create(tag_name = tag)
            self.tags.add(tag_obj)
    
    def cleanProblemForDB(problem):
        if 'rating' in problem:
            rating = problem["rating"]
        else:
            rating = 0
        if 'tags' in problem:
            tags = problem["tags"]
        else:
            tags = []

        p = {'contestID' : problem["contestId"],
                'index'  : problem["index"],
                'name'   : problem["name"],
                'rating' : rating,
                'tags'   : tags,
                'link'   : 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
            }
        return p
    def __str__(self) -> str:
        return str(self.contestID) + self.index + " " + self.name


