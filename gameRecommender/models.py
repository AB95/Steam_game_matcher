from django.db import models


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
    game_name = models.CharField(max_length=255)
    app_ID = models.PositiveIntegerField(unique=True)
    metascore = models.PositiveIntegerField(null=True, blank=True)
    positive_review_numbers = models.PositiveIntegerField(null=True, blank=True)
    negative_review_numbers = models.PositiveIntegerField(null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    store_page = models.URLField(null=True, blank=True)
    gameTags = models.ManyToManyField(GameTags, null=True, blank=True)
    gameFeatures = models.ManyToManyField(GameFeatures, null=True, blank=True)

    class Meta:
        ordering = ('app_ID',)

    def __unicode__(self):
        return self.game_name
