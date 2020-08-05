import os
import datetime
import unittest
import json
import app
from models import setup_db, Movie, Actor

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.token_assistant = os.environ.get('CASTING_ASSISTANT_HEADER')
        self.token_director = os.environ.get('CASTING_DIRECTOR_HEADER')
        self.token_producer = os.environ.get('EXECUTIVE_PRODUCER_HEADER')



    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertEqual(res.status_code, 200)

    def test_no_actors(self):
        res = self.client().get('/actors', headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)


    def test_add_actor(self):
        actor = {
            'name': 'Actor Name',
            'age': '40',
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=actor, headers={"Authorization": 'Bearer '+ self.token_director})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor)
        self.assertEqual(data['total_actors'], len(Actor.query.all()))
        self.assertEqual(res.status_code, 200)


    def test_add_actor_fail(self):
        actor = {
            'name': 'Actor Name',
            'age': '30',
            'gender': 'Female'
        }
        res = self.client().post('/actors', json=actor, headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)



    def test_update_actor(self):
        res = self.client().patch('/actors/1', json={'age': '50'}, headers={"Authorization": 'Bearer '+ self.token_director})
        data = json.loads(res.data)
        actor = Actor.query.get(1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor)
        self.assertEqual(data['total_actors'], len(Actor.query.all()))
        self.assertEqual(res.status_code, 200)


    def test_update_actor_fail(self):
        res = self.client().patch('/actors/1', json={'age': '55'}, headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={"Authorization": 'Bearer '+ self.token_director})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/1', headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)



    '''
    MOVIES
    '''

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)
        movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], len(movies))
        self.assertEqual(data['movies'], movies)
        self.assertEqual(res.status_code, 200)

    def test_no_movies(self):
        res = self.client().get('/movies', headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)


    def test_add_movie(self):
        movie = {
            'title': 'Movie Title',
            'releaseDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        res = self.client().post('/movies', json=movie, headers={"Authorization": 'Bearer '+ self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], movie)
        self.assertEqual(data['total_movies'], len(Movie.query.all()))
        self.assertEqual(res.status_code, 200)

    def test_add_movie_fail(self):
        movie = {
            'title': 'The Movie Title',
            'releaseDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        res = self.client().post('/movies', json=movie, headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)


    def test_update_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'New Title'}, headers={"Authorization": 'Bearer '+ self.token_producer})
        data = json.loads(res.data)
        movie = Actor.query.get(1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], movie)
        self.assertEqual(data['total_movies'], len(Actor.query.all()))
        self.assertEqual(res.status_code, 200)

    def test_update_movie_fail(self):
        res = self.client().patch('/movies/1', json={'title': 'New Movie Title'}, headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={"Authorization": 'Bearer '+ self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/1', headers={"Authorization": 'Bearer '+ self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)



if __name__ == "__main__":
    unittest.main()
