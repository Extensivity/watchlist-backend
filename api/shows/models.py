from django.db import models

# Create your models here.
class Show(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Season(models.Model):
  name = models.CharField(max_length=100)
  show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seasons')
  order = models.SmallIntegerField()

  def __str__(self):
    return self.name

class Episode(models.Model):
  name = models.CharField(max_length=100)
  season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
  order = models.PositiveSmallIntegerField()
  seen = models.BooleanField()

  @property
  def show(self):
    return self.season.show

  def __str__(self):
    return self.name
