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
        'release_date':request.form.get('release_date')
    })
    return redirect(url_for('get_games'))

@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('get_games'))

@app.route('/get_genres')
def get_genres():
    return render_template('genres.html',
    genres=mongo.db.genres.find())

@app.route('/edit_genre/<genre_id>')
def edit_genre(genre_id):
    return render_template('editgenre.html',
                           genre=mongo.db.genres.find_one(
                           {'_id': ObjectId(genre_id)}))


@app.route('/update_genre/<genre_id>', methods=['POST'])
def update_genre(genre_id):
    mongo.db.genres.update(
        {'_id': ObjectId(genre_id)},
        {'genre_name': request.form.get('genre_name')})
    return redirect(url_for('get_genres'))

@app.route('/delete_genre/<genre_id>')
def delete_genre(genre_id):
    mongo.db.genres.remove({'_id': ObjectId(genre_id)})
    return redirect(url_for('get_genres'))    

@app.route('/insert_genre', methods=['POST'])
def insert_genre():
    genre_doc = {'genre_name': request.form.get('genre_name')}
    mongo.db.genres.insert_one(genre_doc)
    return redirect(url_for('get_genres'))


@app.route('/add_genre')
def add_genre():
    return render_template('addgenre.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
