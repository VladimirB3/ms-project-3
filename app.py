import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'videogames'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_games')
def get_games():
    return render_template("games.html", games=list(mongo.db.games.find()))


@app.route('/add_game')
def add_game():
    return render_template('addgame.html', genres=mongo.db.genres.find())


@app.route('/insert_game', methods=['POST'])
def insert_game():
    games = mongo.db.games
    games.insert_one(request.form.to_dict())
    return redirect(url_for('get_games'))


@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game =  mongo.db.games.find_one({"_id": ObjectId(game_id)})
    all_genres =  mongo.db.genres.find()
    return render_template('editgame.html', game=the_game,
                           genres=all_genres)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
