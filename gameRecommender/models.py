from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class GameTags(models.Model):
    tags = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.tags


class GameFeatures (models.Model):
    features = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.features


class GameInfo(models.Model):
    name = models.CharField(max_length=255)
    app_id = models.PositiveIntegerField(unique=True, primary_key=True)
    metascore = models.PositiveIntegerField(null=True, blank=True)
    positive_reviews = models.PositiveIntegerField(null=True, blank=True)
    negative_reviews = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    store_url = models.URLField(null=True, blank=True)
    gameTags = models.ManyToManyField(GameTags, blank=True)
    gameFeatures = models.ManyToManyField(GameFeatures, blank=True)
    operating_systems = ArrayField(models.CharField(max_length=255, blank=True, null=True),
                                   size=3, null=True, blank=True)

    class Meta:
        ordering = ('app_id',)

    def __unicode__(self):
        return self.name
