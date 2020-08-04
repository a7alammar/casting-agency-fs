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

        # self.casting_assistant_header = os.environ.get('CASTING_ASSISTANT_HEADER')
        self.casting_assistant_header = {'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwNFAzemRMWTJYUUFDNTlNNW9UTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1meS0wdDB2Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk1Mjg3OTczNDk5MjkwMjM5MjYiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9kZXYtZnktMHQwdmYudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NjU3NDI2NywiZXhwIjoxNTk2NTgxNDY3LCJhenAiOiIwMXM3NlhORW9vRFpQNmh0aEdWYVlTVUhidUJXdFAydSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.OtZ_sgdcvoVATgPKMrXadmcdt96d9x3VzFyUVAo5uyaT3QfTC0fgVrnCj-AeYlNDHOkgk0cy_QNSrcXuIqoYdkV7aRqJDeuTsS0VKgn4uPMAb8rncwN1lHpQv3RjtABgu6BLVB4CVqgJDIBrNx78L98QQcfzjStf-2wphpA8SfiR2phRUOmWr6uJzVpJ2vV8hOObWOP4rFzvd2qeEVzQYvoEwtLF04i4w6CtY5AF3CR-pkDNbxcbS5soMqzvHSGoGTlo2ZDDwAe-0W3JJiz160vR9136ct53vnqBd7HQxQoD6-oG5qSA0AP-08jLsTSOb5ZrXOYC9uETYUosNveQ8g' }


        # self.casting_director_header = os.environ.get('CASTING_DIRECTOR_HEADER')
        self.casting_director_header = {'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwNFAzemRMWTJYUUFDNTlNNW9UTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1meS0wdDB2Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQ3Nzc1Mjc3NjYyMzI2MzE3MTQiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9kZXYtZnktMHQwdmYudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NjU3NDExMSwiZXhwIjoxNTk2NTgxMzExLCJhenAiOiIwMXM3NlhORW9vRFpQNmh0aEdWYVlTVUhidUJXdFAydSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.blNLM7T-OGV59nF3gKRnYORCFdneU2JgzvVCRv2yyuXVXI-R5ZBO0KU86ylXiq1QwWapHjhbyI7f8svtMi_1JJsgX-hO6ok_bZ7uGmHku_khqsSQfdQcfo2fuJkp10jC0puWNm0yoN6ZT_MnHZx9Zvf4fif0hEhHo94mNcaoaTVvDIE9ZNguwOuHE7OsT1bKJul-ZLsNT0G_QUXb6T-jxrndRMg5uAOLWudNEwUSiTDVjca8-adtjkoQwOADdK9YcL_4FWXetKo3oyYf25_3AwlRHNSEK7A-tMec4GbAYuOzavscJTuDdKJBne8I2hMoUZ3j_SkoOd-_V7ecDQfwRQ' }


        # self.executive_producer_header = os.environ.get('EXECUTIVE_PRODUCER_HEADER')
        self.executive_producer_header = {'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwNFAzemRMWTJYUUFDNTlNNW9UTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1meS0wdDB2Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk0MDQyODAzMjY4MTkzOTE1NTMiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9kZXYtZnktMHQwdmYudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NjU3Mjg5NywiZXhwIjoxNTk2NTgwMDk3LCJhenAiOiIwMXM3NlhORW9vRFpQNmh0aEdWYVlTVUhidUJXdFAydSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.W0HTmkzG-7WZg26AlpxQTFyToq5ZOVZ5OmLTIFqZ5tQlmlO1HAAlp_mmsxGJdbwg88rGLKG93xqLii07Yss97B89PszIQyMA9Tn2hW7TAiWkUP5iL5evvGec3UMjzrMK-_h-e6mwjGBiJ9qC5qq4FJAkkoktJk8y6VCogcfd7o0tghZ2CfwPNHFco2-GKRm22rKYSzL9AKm3rDo94uoXImhgk7S1j6HFklB0W02f7n5fryzwWh1jmq0BrCCsoNVfGq8uzRk1QJwHg3tmA6rKy9FPFXGBlbJyJqZI0b-AfDG_N48e63jVEvdOIW7O1gfQkzw9Bc2WX8OiNYTsn7s-gA' }




    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertEqual(res.status_code, 200)

    def test_no_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)


    def test_add_actor(self):
        actor = {
            'name': 'Actor Name',
            'age': '40',
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=actor, headers=self.casting_director_header)
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
        res = self.client().post('/actors', json=actor, headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)



    def test_update_actor(self):
        res = self.client().patch('/actors/1', json={'age': '50'}, headers=self.casting_director_header)
        data = json.loads(res.data)
        actor = Actor.query.get(1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor)
        self.assertEqual(data['total_actors'], len(Actor.query.all()))
        self.assertEqual(res.status_code, 200)


    def test_update_actor_fail(self):
        res = self.client().patch('/actors/1', json={'age': '55'}, headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.casting_director_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/1', headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)



    '''
    MOVIES
    '''

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant_header)
        data = json.loads(res.data)
        movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], len(movies))
        self.assertEqual(data['movies'], movies)
        self.assertEqual(res.status_code, 200)

    def test_no_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)


    def test_add_movie(self):
        movie = {
            'title': 'Movie Title',
            'releaseDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        res = self.client().post('/movies', json=movie, headers=self.executive_producer_header)
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
        res = self.client().post('/movies', json=movie, headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)


    def test_update_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'New Title'}, headers=self.executive_producer_header)
        data = json.loads(res.data)
        movie = Actor.query.get(1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], movie)
        self.assertEqual(data['total_movies'], len(Actor.query.all()))
        self.assertEqual(res.status_code, 200)

    def test_update_movie_fail(self):
        res = self.client().patch('/movies/1', json={'title': 'New Movie Title'}, headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/1', headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)



if __name__ == "__main__":
    unittest.main()
