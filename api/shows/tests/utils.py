import json
from graphene_django.utils.testing import GraphQLTestCase


class TestCase(GraphQLTestCase):
  GRAPHQL_URL = '/api/graphql'
  fixtures = ['tests_shows.json']

  @staticmethod
  def get_content(response):
    return json.loads(response.content)
