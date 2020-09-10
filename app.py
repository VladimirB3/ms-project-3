import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env


# Environment Variable and code necessary to connect to mongo DB

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'videogames'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


# Home page rendering (Referenced from Code Institute tutorial)

@app.route('/')
@app.route('/get_games')
def get_games():
    return render_template("games.html", games=list(mongo.db.games.find()))


# Add game page render (Referenced from Code Institute tutorial)

@app.route('/add_game')
def add_game():
    return render_template('addgame.html', genres=mongo.db.genres.find())


# Method to inject necessary information into MongoDB (Referenced from Code Institute tutorial)

@app.route('/insert_game', methods=['POST'])
def insert_game():
    games = mongo.db.games
    games.insert_one(request.form.to_dict())
    return redirect(url_for('get_games'))


# Function to edit the information inside MongoDB by ID (Referenced from Code Institute tutorial)

@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game =  mongo.db.games.find_one({"_id": ObjectId(game_id)})
    all_genres =  mongo.db.genres.find()
    return render_template('editgame.html', game=the_game,
                           genres=all_genres)


# Function to update information in the database

@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    games = mongo.db.games
    games.update( {'_id': ObjectId(game_id)},
    {
        'game_name': request.form.get('game_name'),
        'genre_name': request.form.get('genre_name'),
        'developer_name': request.form.get('developer_name'),
        'director_name': request.form.get('director_name'),
        'summary': request.form.get('summary'),
        'quality': request.form.get('quality'),
        'release_date':request.form.get('release_date'),
        'platforms': request.form.get('platforms')
    })
    return redirect(url_for('get_games'))


# Function to delete information from the database (Referenced from Code Institute tutorial)

@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('get_games'))


# Genres Page render (Referenced from Code Institute tutorial)

@app.route('/get_genres')
def get_genres():
    return render_template('genres.html',
    genres=mongo.db.genres.find())


# Function to edit genre name (Referenced from Code Institute tutorial)

@app.route('/edit_genre/<genre_id>')
def edit_genre(genre_id):
    return render_template('editgenre.html',
                           genre=mongo.db.genres.find_one(
                           {'_id': ObjectId(genre_id)}))


# Function to change and update genre name (Referenced from Code Institute tutorial)

@app.route('/update_genre/<genre_id>', methods=['POST'])
def update_genre(genre_id):
    mongo.db.genres.update(
        {'_id': ObjectId(genre_id)},
        {'genre_name': request.form.get('genre_name')})
    return redirect(url_for('get_genres'))


# Function to delete a genre (Referenced from Code Institute tutorial)

@app.route('/delete_genre/<genre_id>')
def delete_genre(genre_id):
    mongo.db.genres.remove({'_id': ObjectId(genre_id)})
    return redirect(url_for('get_genres'))    


# Function to insert genre to the genre list (Referenced from Code Institute tutorial)

@app.route('/insert_genre', methods=['POST'])
def insert_genre():
    genre_doc = {'genre_name': request.form.get('genre_name')}
    mongo.db.genres.insert_one(genre_doc)
    return redirect(url_for('get_genres'))


# Render of the page where genres are added (Referenced from Code Institute tutorial)

@app.route('/add_genre')
def add_genre():
    return render_template('addgenre.html')


# Environment variables to run the app locally (Referenced from Code Institute tutorial)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
