from django.contrib import admin
from api.shows import models

# Register your models here.
@admin.register(models.Show)
class ShowAdmin(admin.ModelAdmin):
  pass

@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
  pass

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
  pass
