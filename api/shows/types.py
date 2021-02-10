import graphene
from graphene_django import types
from api.shows import models


class SearchType(graphene.InputObjectType):
  name__startswith = graphene.String(name="name_startswith")
  name__endswith = graphene.String(name="name_endswith")
  name__icontains = graphene.String(name="name_icontains")
  seen__all = graphene.Boolean(name="seen_all")


class ShowType(types.DjangoObjectType):
  class Meta:
    model = models.Show
    fields = '__all__'
  
  class SearchType(SearchType):
    class Meta:
      name = 'ShowSearchType'


class SeasonType(types.DjangoObjectType):
  class Meta:
    model = models.Season
    fields = '__all__'
  
  class SearchType(SearchType):
    class Meta:
      name = 'SeasonSearchType'


class EpisodeType(types.DjangoObjectType):
  class Meta:
    model = models.Episode
    fields = '__all__'
  
  class SearchType(SearchType):
    class Meta:
      name = 'EpisodeSearchType'
    seen__all = graphene.Boolean(name='seen')
