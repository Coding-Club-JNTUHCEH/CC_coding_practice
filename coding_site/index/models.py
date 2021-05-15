from django.db import models

# Create your models here.

class Tag(models.Model) :
    tag_name = models.CharField(max_length=32)

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
    def create(*args, **kwargs):
        p = Problem(
            contestID = args[1]["contestID"],
            index = args[1]["index"],
            name  = args[1]["name"],
            rating= args[1]["rating"],
            link   = args[1]["link"],
        )

        return p

    def link_tags(self,tags):
        for tag in tags:
            tag_obj = Tag.objects.get(tag_name = tag)
            self.tags.add(tag_obj)
    
    def __str__(self) -> str:
        return self.name



    