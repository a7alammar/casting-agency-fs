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

        self.casting_assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwNFAzemRMWTJYUUFDNTlNNW9UTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1meS0wdDB2Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk1Mjg3OTczNDk5MjkwMjM5MjYiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9kZXYtZnktMHQwdmYudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NjAyODk2MSwiZXhwIjoxNTk2MDM2MTYxLCJhenAiOiIwMXM3NlhORW9vRFpQNmh0aEdWYVlTVUhidUJXdFAydSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.TWwhlVQx--riRocjiqkXQvHkXsVawV3heb6aaZz_3LELgsmSSXqniroalV6z-yX3joDSwpcZ_xgBDiVm_sahVB3a-hL8QQm5RyDshYMf1ExKAboSsO5zv_4QE1jD5fkNbAnIWbXEEI-BrpIC40P3KvNTwHk-wfDr2eeHSe3FkiWaFtNW5ZEKlzAqC1hAPxWCYAGmnvGSIKJVXhci5FmmbRthNxB7NyvR-_CbB9sxX7VkSmvf2ZT-1V-KJ7fcmzlkzd66g3qd5CO1XZBvk_e4dZgXAfJii1FVDRu8wwOY3gApp9LlhMmQ-DIUe2VjF03DsCJAHOqN_W9jZM0BdrlexQ'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwNFAzemRMWTJYUUFDNTlNNW9UTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1meS0wdDB2Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQ3Nzc1Mjc3NjYyMzI2MzE3MTQiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9kZXYtZnktMHQwdmYudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NjAyODczNCwiZXhwIjoxNTk2MDM1OTM0LCJhenAiOiIwMXM3NlhORW9vRFpQNmh0aEdWYVlTVUhidUJXdFAydSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.F764m4EpmeYMyeDmJBJOZAYto916st6gMygNHPvo6Vigz1ggiWf3SizQoNe9SrJT-N7ttqhpOaTvafkWP7--T7ZdwwiXmSow7i077w6YpCAtB-eQI-D29aymss9WZiEsmYRxrvUSPVsVYYQLVhayvEGC3_Hh4z92n9eB6IwWpQLECC_192WuJWqBDdJcMaMAPhHEf01-WTxo4J41yZrATK-DSG4m1a1ja9y-clUSyF88RiaHueFRQMoEcXAFdUjLCsps4VNWoMhH-hyRz7eFFLLKEPKoNuYqL2A5VgZ4-ODb8Fd_bVjYbxFb9040cvlhRChdhBWkzkZrsJWM8NarPA'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwNFAzemRMWTJYUUFDNTlNNW9UTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1meS0wdDB2Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk0MDQyODAzMjY4MTkzOTE1NTMiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9kZXYtZnktMHQwdmYudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NjAyODY0OCwiZXhwIjoxNTk2MDM1ODQ4LCJhenAiOiIwMXM3NlhORW9vRFpQNmh0aEdWYVlTVUhidUJXdFAydSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.ucqQQDsuL3Nj2G5MaYmh1t1LixxsDw49whT0vixqm-wj8T87GP5u0YEF5L5FMLzjQjPhyb79aHoin2uM6dqs55RfZBHuqurLxm6tdT5yLmoWYRrpi5gGE_AcslPb83ZwnmwQTwZEUUIbTDRSfQ2s8egokGO4Sb6zAxrI0L6mFxl3U6E9665pa7UDTjoW1M_WGIisuaClQiSjQ0fkQ2yDhj6n7Dqpx5urUkc5Ns-R_VHkhagcYuDA2MpfTR7xptmaodQsCsiN-fFw9J4X8nlHAiOGtcRKXjYWwFF9t8DJViMoQACyjDQrIoY1MXjmXJC4rRMr_L_RuuDupwkE3EveDg'
        }

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
