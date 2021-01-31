from django.db import models


class NameBasics(models.Model):
    nconst = models.TextField(primary_key=True)
    primaryname = models.TextField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['primaryname']),
        ]

class TitleBasics(models.Model):
    tconst = models.TextField(primary_key=True)
    titletype = models.TextField(null=True)
    primarytitle = models.TextField(null=True)
    originaltitle = models.TextField(null=True)
    isadult = models.IntegerField(null=True)
    startyear = models.TextField(null=True)
    endyear = models.IntegerField(null=True)
    runtimeminutes = models.IntegerField(null=True)
    genres = models.TextField(null=True)
    imagelink = models.URLField(null=True)
    directors = models.ManyToManyField(NameBasics, related_name='movies')
    writers = models.ManyToManyField(NameBasics, related_name='writers')

    class Meta:
        indexes = [
            models.Index(fields=['primarytitle']),
            models.Index(fields=['originaltitle']),
        ]

class Link(models.Model):
    movieid = models.IntegerField()
    imdbid = models.OneToOneField(TitleBasics, on_delete=models.CASCADE)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['movieid']),
    #         models.Index(fields=['imdbid']),
    #     ]

class TitleRating(models.Model):
    imdbid = models.OneToOneField(TitleBasics, on_delete=models.CASCADE, related_name='rating')
    averagerating = models.FloatField(null=True)
    numofvotes = models.IntegerField(null=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['imdbid']),
    #     ]

class TitlePrincipals(models.Model):
    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE, related_name='crew')
    ordering = models.IntegerField()
    nconst = models.ForeignKey(NameBasics, on_delete=models.CASCADE)
    category = models.TextField(null=True)
    job = models.TextField(null=True)
    characters = models.TextField(null=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['tconst']),
    #         models.Index(fields=['nconst']),
    #     ]

class TitleAkas(models.Model):
    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    localtitle = models.TextField(null=True)
    region = models.TextField(null=True)
    language = models.TextField(null=True)
    type = models.TextField(null=True)
    attributes = models.TextField(null=True)
    original = models.TextField(null=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['tconst']),
    #     ]
