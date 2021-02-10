import graphene
from graphene_django import debug
from api.shows import schema as shows


class Query(shows.Query, graphene.ObjectType):
  debug = graphene.Field(debug.DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query)
