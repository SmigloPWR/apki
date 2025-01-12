from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dane aplikacji
reports = []  # Lista zgłoszeń
user_progress = {'rower': 0, 'hulajnoga': 0, 'auto': 0}  # Postęp użytkownika
user_badges = {'brązowa': False, 'srebrna': False, 'złota': False}  # Odznaki użytkownika


# Funkcja aktualizacji odznak
def update_badges():
    if user_progress['rower'] >= 10:
        user_badges['brązowa'] = True
    if user_progress['rower'] >= 10 and user_progress['auto'] >= 10:
        user_badges['srebrna'] = True
    if (
        user_progress['rower'] >= 10 and
        user_progress['auto'] >= 10 and
        user_progress['hulajnoga'] >= 10
    ):
        user_badges['złota'] = True


# Strona logowania
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == 'admin' and password == 'admin1234':
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        elif email and password:
            session['role'] = 'user'
            return redirect(url_for('dashboard'))
        else:
            flash("Nieprawidłowy login lub hasło!", "error")
    return render_template('login.html')


# Strona główna po zalogowaniu
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# Strona zgłaszania
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        vehicle_type = request.form.get('vehicle_type')
        photo = request.files.get('photo')

        if not vehicle_type or not photo:
            flash("Zgłoszenie odrzucone: brak zdjęcia lub typu pojazdu.", "error")
            return redirect(url_for('report'))

        # Dodanie zgłoszenia
        reports.append({
            'id': len(reports) + 1,
            'title': f'Zgłoszenie nr {len(reports) + 1}',
            'status': 'oczekujące',
            'vehicle_type': vehicle_type,
            'photo': True
        })

        flash("Zgłoszenie wysłane!", "success")
        return redirect(url_for('report_success'))
    return render_template('report.html')


@app.route('/report_success')
def report_success():
    return render_template('report_success.html')


# Strona „Moje zgłoszenia”
@app.route('/my_reports')
def my_reports():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    return render_template('my_reports.html', reports=reports)


# Strona „Moje odznaki”
@app.route('/badges')
def badges():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    return render_template('badges.html', progress=user_progress, badges=user_badges)


# Panel administratora
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', reports=reports)


# Akceptowanie zgłoszenia
@app.route('/accept_report/<int:report_id>', methods=['POST'])
def accept_report(report_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    for report in reports:
        if report['id'] == report_id:
            report['status'] = 'zaakceptowane'
            user_progress[report['vehicle_type']] += 1
            update_badges()
            break
    return redirect(url_for('admin_dashboard'))


# Odrzucanie zgłoszenia
@app.route('/reject_report/<int:report_id>', methods=['POST'])
def reject_report(report_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    for report in reports:
        if report['id'] == report_id:
            report['status'] = 'odrzucone'
            break
    return redirect(url_for('admin_dashboard'))


# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
