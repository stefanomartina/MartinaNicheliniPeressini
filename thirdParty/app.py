from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/registration")
def registration():
	return render_template('registration.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run()