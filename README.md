# Udacity FSND: Capstone Project


## Motivation :

This is the last project of the Udacity-Full-Stack-Nanodegree , where I was challenged to use all of the concepts and the skills taught in the courses to build an API from start to finish and host it.

## Getting started :

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server


```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

### base URL :

#### https://casting-agency-fs.herokuapp.com/

### GET /movies :

#### - General:

Returns an object that contains list of movies and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/movies

{
'success': True,
'total_movies': 1,
"movies": [
{
"id": 2,
"title": "avengers",
"release_date": "01/01/2020"
}
]
}

### GET /actors :

#### - General:

Returns an object that contains list of actors and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/actors

{
'success': True,
'total_actors': 1,
"actors": [
{
"id": 2,
"name": "abdulrahman",
"age": "23",
"gender": "M"
}
]
}

### POST /MOVIE :

#### - General:

Returns an object that contains created movie and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/movies -X POST -H "Content-Type: application/json" -d '{"title": "avengers civil war" , ”releaseDate": "07/07/2020"}'

{
'success': True,
'movie': {
"id": 3,
"title": "avengers civil war"
"releaseDate": "07/07/2020"
},
'total_movies': 2
}

### POST /ACTOR :

#### - General:

Returns an object that contains created actor and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d '{"name": "mshary", "age": "27", "gender":"M"}'

{
'success': True,
'actor': {
"id": 3,
"name": "mshary",
"age": "27",
"gender":"M"
},
'total_actors': 2
}

### PATCH /MOVIE :

#### - General:

Returns an object that contains updated movie and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/movies/3 -X PATCH -H "Content-Type: application/json" -d '{”releaseDate": "07/05/2020"}'

{
'success': True,
'movie': {
"id": 3,
"title": "avengers civil war"
"releaseDate": "07/05/2020",
},
'total_movies': 2
}

### PATCH /ACTOR :

#### - General:

Returns an object that contains updated actor and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/actors/3 -X PATCH -H "Content-Type: application/json" -d '{"age": "25"}'
{
'success': True,
'actor': {
"id": 3,
"name": "mshary"
"age": "25",
"gender":"M""
},
'total_actors': 2
}

### DELETE /MOVIE :

#### - General:

Returns an object that contains deleted movie id and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/movies/2 -X DELETE

{
"deleted": 2,
"success": true
}

### DELETE /ACTOR :

#### - General:

Returns an object that contains deleted actor id and success value

#### - Sample: curl -H "Authorization": "Bearer {your_token}" https://casting-agency-fs.herokuapp.com/actors/2 -X DELETE

{
"deleted": 2,
"success": true
}

## Roles:

### Casting Assistant

- Can view actors and movies

### Casting Director

- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

### Executive Producer

- All permissions a Casting Director has and…
- Add or delete a movie from the database