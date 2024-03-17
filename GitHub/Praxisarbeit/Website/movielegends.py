from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'geheimnis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:AdminMariaDB$1@localhost/movie_legends_db'
db = SQLAlchemy(app)

# Datenbankmodell für Benutzer
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)

# Datenbankmodell für Filme
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    added_by = db.Column(db.String(100), nullable=False)

# Anmeldeseite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        username = request.form['username']
        if len(username) <= 100 and username.isalnum():
            new_user = User(name=name, lastname=lastname, username=username)
            db.session.add(new_user)
            db.session.commit()
            flash('Erfolgreich registriert!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ungültiger Benutzername! Bitte verwenden Sie nur Buchstaben und Zahlen.', 'error')
    return render_template('login.html')

# Hauptseite
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

# Funktion zum Hinzufügen eines Films
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if 'username' in request.cookies:
        title = request.form['title']
        rating = request.form['rating']
        comment = request.form['comment']
        added_by = request.cookies.get('username')
        new_movie = Movie(title=title, rating=rating, comment=comment, added_by=added_by)
        db.session.add(new_movie)
        db.session.commit()
        flash('Film erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Sie müssen angemeldet sein, um einen Film hinzuzufügen.', 'error')
        return redirect(url_for('login'))

# Funktion zum Löschen eines Films
@app.route('/delete_movie/<int:id>')
def delete_movie(id):
    if 'username' in request.cookies:
        if request.cookies.get('username') == 'admin':
            movie_to_delete = Movie.query.get_or_404(id)
            db.session.delete(movie_to_delete)
            db.session.commit()
            flash('Film erfolgreich gelöscht!', 'success')
        else:
            flash('Nur Admins dürfen Filme löschen.', 'error')
    else:
        flash('Sie müssen angemeldet sein, um einen Film zu löschen.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
