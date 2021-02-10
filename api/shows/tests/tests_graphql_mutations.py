import unittest
from django.forms.models import model_to_dict
from api.shows import models
from .utils import TestCase


class ShowMutationGraphQLTestCase(TestCase):
  def test_create(self):
    count = models.Show.objects.count()
    response = self.query(
      '''
      mutation create($name: String!){
        createShow(name: $name) {
          show {
            id
            name
          }
        }
      }
      ''',
      variables={ 'name': 'Created Show' }
    )

    content = self.get_content(response)
    expecting = { 'id': '4', 'name': 'Created Show' }
    show = models.Show.objects.get(pk=4)

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['createShow']['show'])
    self.assertEquals(expecting['name'], show.name)
    self.assertEquals(count + 1, models.Show.objects.count())
  
  def test_update(self):
    response = self.query(
      '''
      mutation update($id: Int!, $name: String!) {
        updateShow(id: $id, name: $name) {
          show {
            id
            name
          }
        }
      }
      ''',
      variables={ 'id': 1, 'name': 'Changed Name' }
    )

    content = self.get_content(response)
    expecting = { 'id': '1', 'name': 'Changed Name' }
    show = models.Show.objects.get(pk=1)

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['updateShow']['show'])
    self.assertEquals(expecting['name'], show.name)

  def test_delete(self):
    count = models.Show.objects.count()
    response = self.query(
      '''
      mutation delete($id: Int!) {
        deleteShow(id: $id) {
          ok
          shows {
            id
          }
        }
      }
      ''',
      variables={ 'id': 2 }
    )

    content = self.get_content(response)
    expecting = {
      'ok': True,
      'shows': [
        { 'id': '1' },
        { 'id': '3' }
      ]
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['deleteShow'])
    self.assertEquals(count - 1, models.Show.objects.count())

class SeasonMutationGraphQLTestCase(TestCase):
  def test_create(self):
    objects = models.Season.objects
    count = objects.count()

    response = self.query(
      '''
      mutation create($name: String!, $show: Int!, $order: Int!) {
        createSeason(name: $name, show: $show, order: $order) {
          season {
            id
            name
            show {
              id
            }
            order
          }
        }
      }
      ''',
      variables={ 'name': 'Test Season', 'show': 1, 'order': 1 }
    )

    content = self.get_content(response)
    season = objects.get(pk=4)
    expecting = {
      'id': '4',
      'name': 'Test Season',
      'order': 1,  # Everything else a string but this???
      'show': {
        'id': '1'
      }
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['createSeason']['season'])
    self.assertEquals(expecting['name'], season.name)
    self.assertEquals(count + 1, objects.count())

  def test_update(self):
    response = self.query(
      '''
      mutation update($id: Int!, $name: String!, $show: Int!, $order: Int!) {
        updateSeason(id: $id, name: $name, show: $show, order: $order) {
          season {
            id
            name
            order
            show {
              id
            }
          }
        }
      }
      ''',
      variables= { 'id': '1', 'name': 'Changed Name', 'show': '2', 'order': '2' }
    )

    content = self.get_content(response)
    season = models.Season.objects.get(pk=1)
    expecting = {
      'id': '1',
      'name': 'Changed Name',
      'order': 2,
      'show': {
        'id': '2'
      }
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['updateSeason']['season'])
    self.assertEquals(expecting['name'], season.name)

  def test_delete(self):
    count = models.Season.objects.count()
    response = self.query(
      '''
      mutation delete($id: Int!) {
        deleteSeason(id: $id) {
          ok
          seasons {
            id
          }
        }
      }
      ''',
      variables={ 'id': 2 }
    )

    content = self.get_content(response)
    expecting = {
      'ok': True,
      'seasons': [
        { 'id': '1' },
        { 'id': '3' }
      ]
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['deleteSeason'])
    self.assertEquals(count - 1, models.Season.objects.count())

class EpisodeMutationGraphQLTestCase(TestCase):
  def test_create(self):
    count = models.Episode.objects.count()
    response = self.query(
      '''
      mutation create($name: String!, $season: Int!, $order: Int!, $seen: Boolean!) {
        createEpisode(name: $name, season: $season, order: $order, seen: $seen) {
          episode {
            id
            name
            order
            seen
            season {
              id
            }
          }
        }
      }
      ''',
      variables={ 'name': 'Test Episode', 'season': 1, 'order': 1, 'seen': True }
    )

    content = self.get_content(response)
    episode = models.Episode.objects.get(pk=6)
    expecting = {
      'id': '6',
      'name': 'Test Episode',
      'order': 1,
      'seen': True,
      'season': {
        'id': '1'
      }
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['createEpisode']['episode'])
    self.assertEquals(expecting['name'], episode.name)
    self.assertEquals(count + 1, models.Episode.objects.count())

  def test_update(self):
    response = self.query(
      '''
      mutation update($id: Int!, $name: String!, $season: Int!, $order: Int!, $seen: Boolean!) {
        updateEpisode(id: $id, name: $name, season: $season, order: $order, seen: $seen) {
          episode {
            id
            name
            order
            seen
            season {
              id
            }
          }
        }
      }
      ''',
      variables={ 'id': '1', 'name': 'Changed Name', 'season': '2', 'order': '2', 'seen': True }
    )

    content = self.get_content(response)
    episode = models.Episode.objects.get(pk=1)
    expecting = {
      'id': '1',
      'name': 'Changed Name',
      'order': 2,
      'seen': True,
      'season': {
        'id': '2'
      }
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['updateEpisode']['episode'])
    self.assertEquals(expecting['name'], episode.name)

  def test_delete(self):
    count = models.Episode.objects.count()
    response = self.query(
      '''
      mutation delete($id: Int!) {
        deleteEpisode(id: $id) {
          ok
          episodes {
            id
          }
        }
      }
      ''',
      variables={ 'id': 2 }
    )

    content = self.get_content(response)
    expecting = {
      'ok': True,
      'episodes': [
        { 'id': '1' },
        { 'id': '3' },
        { 'id': '4' },
        { 'id': '5' }
      ]
    }

    self.assertResponseNoErrors(response)
    self.assertEquals(expecting, content['data']['deleteEpisode'])
    self.assertEquals(count - 1, models.Episode.objects.count())
