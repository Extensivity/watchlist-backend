import json
from graphene_django.utils.testing import GraphQLTestCase


class TestCase(GraphQLTestCase):
  GRAPHQL_URL = '/api/graphql'
  fixtures = ['tests_shows.json']

class ShowGraphQLTestCase(TestCase):
  def test_basic_get_all(self):
    response = self.query(
      '''
      query {
        shows {
          id
          name
        }
      }
      '''
    )
    content = json.loads(response.content)
    expecting = [
      {'id': '1', 'name': 'Show 1'},
      {'id': '2', 'name': 'Show 2'},
      {'id': '3', 'name': 'Show 3'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['shows'])
  
  def test_basic_get_one_by_id(self):
    response = self.query(
      '''
      query show($pk: Int!) {
        show(id: $pk) {
          name
        }
      }
      ''',
      variables={'pk': "1"}
    )

    content = json.loads(response.content)
    expecting = {'name': 'Show 1'}

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['show'])
  
  def test_search_by_name(self):
    response = self.query(
      '''
      query shows($start: String!, $end: String!, $contains: String!) {
        shows(search: {
          name_startswith: $start
          name_endswith: $end
          name_icontains: $contains
        }) {
          name
        }
      }
      ''',
      variables={
        'start': 'S',
        'end': '3',
        'contains': 'ow'
      }
    )

    content = json.loads(response.content)
    expecting = [{'name': 'Show 3'}]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['shows'])
  
  def test_search_by_finished(self):
    response = self.query(
      '''
      query shows($seen: Boolean!) {
        shows(search: {
          seen_all: $seen
        }) {
          name
        }
      }
      ''',
      variables={'seen': True}
    )
    
    content = json.loads(response.content)
    expecting = [{'name': 'Show 1'}]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['shows'])

  def test_search_by_not_finished(self):
    response = self.query(
      '''
      query shows($seen: Boolean!) {
        shows(search: {
          seen_all: $seen
        }) {
          name
        }
      }
      ''',
      variables={'seen': False}
    )
    
    content = json.loads(response.content)
    expecting = [
      {'name': 'Show 2'},
      {'name': 'Show 3'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['shows'])

class SeasonGraphQLTestCase(TestCase):
  def test_basic_get_all(self):
    response = self.query(
      '''
      query {
        seasons {
          id
          name
        }
      }
      '''
    )
    content = json.loads(response.content)
    expecting = [
      {'id': '1', 'name': 'Season 1'},
      {'id': '2', 'name': 'Season 2'},
      {'id': '3', 'name': 'Season 3'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['seasons'])
  
  def test_basic_get_one_by_id(self):
    response = self.query(
      '''
      query season($pk: Int!) {
        season(id: $pk) {
          name
        }
      }
      ''',
      variables={'pk': "1"}
    )

    content = json.loads(response.content)
    expecting = {'name': 'Season 1'}

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['season'])
  
  def test_search_by_name(self):
    response = self.query(
      '''
      query seasons($start: String!, $end: String!, $contains: String!) {
        seasons(search: {
          name_startswith: $start
          name_endswith: $end
          name_icontains: $contains
        }) {
          name
        }
      }
      ''',
      variables={
        'start': 'S',
        'end': '3',
        'contains': 'on'
      }
    )

    content = json.loads(response.content)
    expecting = [{'name': 'Season 3'}]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['seasons'])
  
  def test_search_by_finished(self):
    response = self.query(
      '''
      query seasons($seen: Boolean!) {
        seasons(search: {
          seen_all: $seen
        }) {
          name
        }
      }
      ''',
      variables={'seen': True}
    )
    
    content = json.loads(response.content)
    expecting = [{'name': 'Season 1'}]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['seasons'])

  def test_search_by_not_finished(self):
    response = self.query(
      '''
      query seasons($seen: Boolean!) {
        seasons(search: {
          seen_all: $seen
        }) {
          name
        }
      }
      ''',
      variables={'seen': False}
    )
    
    content = json.loads(response.content)
    expecting = [
      {'name': 'Season 2'},
      {'name': 'Season 3'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['seasons'])

class EpisodeGraphQLTestCase(TestCase):
  def test_basic_get_all(self):
    response = self.query(
      '''
      query {
        episodes {
          id
          name
        }
      }
      '''
    )
    content = json.loads(response.content)
    expecting = [
      {'id': '1', 'name': 'Episode 1.1'},
      {'id': '2', 'name': 'Episode 1.2'},
      {'id': '3', 'name': 'Episode 2.1'},
      {'id': '4', 'name': 'Episode 3.1'},
      {'id': '5', 'name': 'Episode 3.2'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['episodes'])
  
  def test_basic_get_one_by_id(self):
    response = self.query(
      '''
      query episode($pk: Int!) {
        episode(id: $pk) {
          name
        }
      }
      ''',
      variables={'pk': "1"}
    )

    content = json.loads(response.content)
    expecting = {'name': 'Episode 1.1'}

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['episode'])
  
  def test_search_by_name(self):
    response = self.query(
      '''
      query episodes($start: String!, $end: String!, $contains: String!) {
        episodes(search: {
          name_startswith: $start
          name_endswith: $end
          name_icontains: $contains
        }) {
          name
        }
      }
      ''',
      variables={
        'start': 'Ep',
        'end': '2',
        'contains': '3'
      }
    )

    content = json.loads(response.content)
    expecting = [{'name': 'Episode 3.2'}]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['episodes'])
  
  def test_search_by_finished(self):
    response = self.query(
      '''
      query episodes($seen: Boolean!) {
        episodes(search: {
          seen: $seen
        }) {
          name
        }
      }
      ''',
      variables={'seen': True}
    )
    
    content = json.loads(response.content)
    expecting = [
      {'name': 'Episode 1.1'},
      {'name': 'Episode 1.2'},
      {'name': 'Episode 3.1'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['episodes'])

  def test_search_by_not_finished(self):
    response = self.query(
      '''
      query episodes($seen: Boolean!) {
        episodes(search: {
          seen: $seen
        }) {
          name
        }
      }
      ''',
      variables={'seen': False}
    )
    
    content = json.loads(response.content)
    expecting = [
      {'name': 'Episode 2.1'},
      {'name': 'Episode 3.2'}
    ]

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['episodes'])
