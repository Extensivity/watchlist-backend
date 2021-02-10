import graphene
from graphene_django import debug
from api.shows import schema as shows


class Query(shows.Query, graphene.ObjectType):
  debug = graphene.Field(debug.DjangoDebug, name='_debug')


class Mutation(shows.Mutation, graphene.ObjectType):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)
