from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Strona logowania
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Logowanie - uproszczone (możesz dodać weryfikację)
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Strona rejestracji
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if password != repeat_password:
            return "Hasła nie są zgodne!", 400
        # Zarejestrowano - przekierowanie do logowania
        return redirect(url_for('login'))
    return render_template('register.html')

# Strona główna po zalogowaniu
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Strona zgłaszania
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Pobieranie danych z formularza
        vehicle_type = request.form.get('vehicle_type')
        photo = request.files.get('photo')

        if not vehicle_type:
            return "Nie wybrano typu pojazdu!", 400

        if not photo:
            return "Nie przesłano zdjęcia!", 400

        # Tutaj można dodać zapis danych, np. do bazy

        # Przekierowanie do strony sukcesu
        return redirect(url_for('report_success'))
    return render_template('report.html')

@app.route('/report_success')
def report_success():
    return render_template('report_success.html')


# Strona "Moje odznaki"
@app.route('/badges')
def badges():
    return render_template('badges.html')

if __name__ == '__main__':
    app.run(debug=True)
