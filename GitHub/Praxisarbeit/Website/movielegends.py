from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'geheimnis'

# Dummy-Datenbank für Benutzer und Filme
users = []
movies = []

# Anmeldeseite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        username = request.form['username']
        if len(username) <= 100 and username.isalnum():
            users.append({'name': name, 'lastname': lastname, 'username': username})
            flash('Erfolgreich registriert!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ungültiger Benutzername! Bitte verwenden Sie nur Buchstaben und Zahlen.', 'error')
    return render_template('login.html')

# Hauptseite
@app.route('/')
def index():
    return render_template('index.html', movies=movies)

# Funktion zum Hinzufügen eines Films
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if 'username' in request.cookies:
        title = request.form['title']
        rating = request.form['rating']
        comment = request.form['comment']
        added_by = request.cookies.get('username')
        movies.append({'title': title, 'rating': rating, 'comment': comment, 'added_by': added_by})
        flash('Film erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Sie müssen angemeldet sein, um einen Film hinzuzufügen.', 'error')
        return redirect(url_for('login'))

# Funktion zum Löschen eines Films
@app.route('/delete_movie/<int:index>')
def delete_movie(index):
    if 'username' in request.cookies:
        if request.cookies.get('username') == 'admin':
            movies.pop(index)
            flash('Film erfolgreich gelöscht!', 'success')
        else:
            flash('Nur Admins dürfen Filme löschen.', 'error')
    else:
        flash('Sie müssen angemeldet sein, um einen Film zu löschen.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
