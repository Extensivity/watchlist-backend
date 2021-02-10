import graphene
from api.shows import types, models

class ShowMutations:
  class Create(graphene.Mutation):
    class Meta:
      name = 'ShowCreate'

    class Arguments:
      name = graphene.String(required=True)
    
    show = graphene.Field(types.ShowType)
  
    @classmethod
    def mutate(cls, root, info, name):
      show = models.Show.objects.create(name=name)
      show.save()
      return cls(show=show)
  
  class Update(graphene.Mutation):
    class Meta:
      name = 'ShowUpdate'

    class Arguments:
      id = graphene.Int(required=True)
      name = graphene.String(required=True)

    show = graphene.Field(types.ShowType)
  
    @classmethod
    def mutate(cls, root, info, id, name):
      show = models.Show.objects.get(pk=id)
      show.name = name
      show.save()
      return cls(show=show)
  
  class Delete(graphene.Mutation):
    class Meta:
      name = 'ShowDelete'

    class Arguments:
      id = graphene.Int(required=True)
    
    shows = graphene.List(types.ShowType)
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
      successful = True
      show = models.Show.objects.get(pk=id)
      try:
        show.delete()
      except:
        successful = False
      return cls(shows=models.Show.objects.all(), ok=successful)


class SeasonMutations:
  class Create(graphene.Mutation):
    class Meta:
      name = 'SeasonCreate'

    class Arguments:
      name = graphene.String(required=True)
      show_id = graphene.Int(name='show', required=True)
      order = graphene.Int(required=True)
    
    season = graphene.Field(types.SeasonType)

    @classmethod
    def mutate(cls, root, info, name, show_id, order):
      show = models.Show.objects.get(pk=show_id)
      season = models.Season.objects.create(
        name=name, show=show, order=order
      )
      season.save()
      return cls(season=season)
  
  class Update(graphene.Mutation):
    class Meta:
      name = 'SeasonUpdate'

    class Arguments:
      id = graphene.Int(required=True)
      name = graphene.String()
      show_id = graphene.Int(name='show')
      order = graphene.Int()
    
    season = graphene.Field(types.SeasonType)

    @classmethod
    def mutate(cls, root, info, id, name, show_id, order):
      season = models.Season.objects.get(pk=id)
      if name:
        season.name = name
      if show_id:
        show = models.Show.objects.get(pk=show_id)
        season.show = show
      if order:
        season.order = order
      season.save()
      return cls(season=season)
  
  class Delete(graphene.Mutation):
    class Meta:
      name = 'SeasonDelete'

    class Arguments:
      id = graphene.Int(required=True)
    
    ok = graphene.Boolean()
    seasons = graphene.List(types.SeasonType)

    @classmethod
    def mutate(cls, root, info, id):
      successful = True
      try:
        season = models.Season.objects.get(pk=id)
        season.delete()
      except:
        successful = False
      return cls(ok=successful, seasons=models.Season.objects.all())


class EpisodeMutations:
  class Create(graphene.Mutation):
    class Meta:
      name = 'EpisodeCreate'

    class Arguments:
      name = graphene.String(required=True)
      season_id = graphene.Int(name='season', required=True)
      order = graphene.Int(required=True)
      seen = graphene.Boolean(required=True)
    
    episode = graphene.Field(types.EpisodeType)

    @classmethod
    def mutate(cls, root, info, name, season_id, order, seen):
      season = models.Season.objects.get(pk=season_id)
      episode = models.Episode.objects.create(
        name=name, season=season, seen=seen, order=order
      )
      episode.save()
      return cls(episode=episode)
  
  class Update(graphene.Mutation):
    class Meta:
      name = 'EpisodeUpdate'

    class Arguments:
      id = graphene.Int(required=True)
      name = graphene.String()
      season_id = graphene.Int(name='season')
      order = graphene.Int()
      seen = graphene.Boolean()
    
    episode = graphene.Field(types.EpisodeType)

    @classmethod
    def mutate(cls, root, info, id, name, season_id, order, seen):
      episode = models.Episode.objects.get(pk=id)
      if name:
        episode.name = name
      if season_id:
        season = models.Season.objects.get(pk=season_id)
        episode.season = season
      if order:
        episode.order = order
      if seen:
        episode.seen = seen
      episode.save()
      return cls(episode=episode)
  
  class Delete(graphene.Mutation):
    class Meta:
      name = 'EpisodeDelete'

    class Arguments:
      id = graphene.Int(required=True)
    
    ok = graphene.Boolean()
    episodes = graphene.List(types.EpisodeType)
  
    @classmethod
    def mutate(cls, root, info, id):
      successful = True
      try:
        episode = models.Episode.objects.get(pk=id)
        episode.delete()
      except:
        successful = False
      return cls(ok=successful, episodes=models.Episode.objects.all())
