from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template

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
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
        # Hier prüfen, ob Benutzer bereits existiert und Passwort übereinstimmt
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Erfolgreich angemeldet!', 'success')
            response = redirect(url_for('index'))
            response.set_cookie('username', username)  # Hier wird das Cookie gesetzt
            print("Cookie wurde gesetzt mit Benutzername:", username)  # Debugging-Anweisung
            return response
        else:
            flash('Ungültige Anmeldeinformationen. Bitte versuchen Sie es erneut.', 'error')
    return render_template('login.html')


# Registrierungsseite
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        if len(username) <= 100 and username.isalnum():
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, lastname=lastname, username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Erfolgreich registriert! Bitte melden Sie sich an.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ungültiger Benutzername! Bitte verwenden Sie nur Buchstaben und Zahlen.', 'error')
    return render_template('register.html')

# Hauptseite
@app.route('/')
def index():
    movies = Movie.query.all()
    print("Benutzername aus Cookie:", request.cookies.get('username'))  # Debugging-Anweisung
    username = request.cookies.get('username')  # Hole den Benutzernamen aus dem Cookie
    print("Benutzername aus Cookie:", request.cookies.get('username'))  # Debugging-Anweisung
    return render_template('index.html', movies=movies, username=username)  # Render das Template mit dem Benutzernamen
    



# Funktion zum Hinzufügen eines Films
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if 'username' in request.cookies:
        title = request.form['title']
        rating = int(request.form['rating'])
        if rating < 1 or rating > 6:  # Bewertung sollte zwischen 1 und 6 liegen
            flash('Die Bewertung muss zwischen 1 und 6 liegen.', 'error')
            return redirect(url_for('index'))
        comment = request.form['comment']
        added_by = request.cookies.get('username')  # Erfassen Sie den Benutzernamen des eingeloggten Benutzers
        new_movie = Movie(title=title, rating=rating, comment=comment, added_by=added_by)  # Speichern Sie den Benutzernamen des hinzufügenden Benutzers
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
@app.route('/logout', methods=['POST'])
def logout():
    # Lösche den Benutzer-Cookie oder beende die Sitzung
    response = redirect(url_for('login'))  # Hier kannst du die Umleitung auf die Login-Seite durchführen
    response.delete_cookie('username')  # Lösche den Benutzer-Cookie
    return response  # Gib die Umleitungsantwort zurück

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
