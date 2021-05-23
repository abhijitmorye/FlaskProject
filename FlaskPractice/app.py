from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    user = "Abhijit"
    return render_template('index.html', user=user)

@app.route('/welcome/admin')
def admin():
    return "<h1> Welcome Admin</h1>"

@app.route('/homepage/<user>')
def homepage(user):

    if user == 'admin':
        return redirect(url_for('admin'))
    else:
        return render_template('homepage.html', user=user)

    




if __name__ == '__main__':
    app.run(debug = True)
