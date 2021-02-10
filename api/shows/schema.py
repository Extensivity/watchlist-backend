import graphene
from django.db.models import Q
from api.shows import (
    types, mutations, models
)


class Query(graphene.ObjectType):
    show = graphene.Field(types.ShowType, id=graphene.Int(required=True))
    shows = graphene.List(types.ShowType, search=types.ShowType.SearchType())
    season = graphene.Field(types.SeasonType, id=graphene.Int(required=True))
    seasons = graphene.List(types.SeasonType, search=types.SeasonType.SearchType())
    episode = graphene.Field(types.EpisodeType, id=graphene.Int(required=True))
    episodes = graphene.List(types.EpisodeType, search=types.EpisodeType.SearchType())

    def resolve_shows(self, context, search={}):
        exclude = Q()
        seen = search.pop('seen__all', None)
        if seen is not None:
            if seen:
                exclude = Q(seasons__episodes__seen=not seen)
            else:
                search['seasons__episodes__seen'] = seen
        return models.Show.objects.filter(Q(**search)).exclude(exclude)
    
    def resolve_show(self, context, id=None):
        return models.Show.objects.get(pk=id)
    
    def resolve_seasons(self, context, search={}):
        exclude = Q()
        seen = search.pop('seen__all', None)
        if seen is not None:
            if seen:
                exclude = Q(episodes__seen=not seen)
            else:
                search['episodes__seen'] = seen
        return models.Season.objects.filter(Q(**search)).exclude(exclude)
    
    def resolve_season(self, context, id=None):
        return models.Season.objects.get(pk=id)
    
    def resolve_episodes(self, context, search={}):
        if search.get('seen__all') is not None:
            search['seen'] = search.pop('seen__all')
        return models.Episode.objects.filter(Q(**search))

    def resolve_episode(self, context, id=None):
        return models.Episode.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_show = mutations.ShowMutations.Create.Field()
    update_show = mutations.ShowMutations.Update.Field()
    delete_show = mutations.ShowMutations.Delete.Field()
    create_season = mutations.SeasonMutations.Create.Field()
    update_season = mutations.SeasonMutations.Update.Field()
    delete_season = mutations.SeasonMutations.Delete.Field()
    create_episode = mutations.EpisodeMutations.Create.Field()
    update_episode = mutations.EpisodeMutations.Update.Field()
    delete_episode = mutations.EpisodeMutations.Delete.Field()
