from flask import Flask, redirect, url_for, request, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<user>')
def profile(user):
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    return "<h1> Welcome Admin</h1>"

@app.route('/user/<user>/')
def user(user):
    return "<h1> Welcome %s </h1>" %user

@app.route('/welcome/<name>/')
def welcome(name):

    if name == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('user', user=name))


if __name__ == "__main__":
    app.run(debug=True)

