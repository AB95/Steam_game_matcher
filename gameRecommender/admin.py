from django.contrib import admin

# Register your models here.
from .models import GameInfo, GameFeatures, GameTags

admin.site.register(GameInfo)
admin.site.register(GameFeatures)
admin.site.register(GameTags)
