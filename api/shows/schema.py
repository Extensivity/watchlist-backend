import graphene
from graphene_django import types
from django.db.models import Q
from api.shows import models


class ShowType(types.DjangoObjectType):
    class Meta:
        model = models.Show
        fields = '__all__'
    
    class SearchType(graphene.InputObjectType):
        class Meta:
            name = "ShowSearchType"

        name__startswith = graphene.String(name="name_startswith")
        name__endswith = graphene.String(name="name_endswith")
        name__icontains = graphene.String(name="name_icontains")
        seen__all = graphene.Boolean(name="seen_all")


class SeasonType(types.DjangoObjectType):
    class Meta:
        model = models.Season
        fields = '__all__'
    
    class SearchType(ShowType.SearchType):
        class Meta:
            name = "SeasonSearchType"


class EpisodeType(types.DjangoObjectType):
    class Meta:
        model = models.Episode
        fields = '__all__'
    
    class SearchType(ShowType.SearchType):
        class Meta:
            name = "EpisodeSearchType"
        
        seen__all = graphene.Boolean(name="seen")


class Query(graphene.ObjectType):
    show = graphene.Field(ShowType, id=graphene.Int(required=True))
    shows = graphene.List(ShowType, search=ShowType.SearchType())
    season = graphene.Field(SeasonType, id=graphene.Int(required=True))
    seasons = graphene.List(SeasonType, search=SeasonType.SearchType())
    episode = graphene.Field(EpisodeType, id=graphene.Int(required=True))
    episodes = graphene.List(EpisodeType, search=EpisodeType.SearchType())

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
        