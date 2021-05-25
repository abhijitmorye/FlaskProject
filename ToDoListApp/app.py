from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

projectdir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(projectdir,'mydatabase.db'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class UserData(db.Model):

    name = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(100), nullable=False, primary_key=True, unique=True)
    phn_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html', existing=False)

@app.route('/registersubmit', methods=['POST'])
def registersubmit():
    name = request.form['name']
    email_id = request.form['email_id']
    phn_number = request.form['phn_number']
    password = request.form['password']

    existing_user = UserData.query.filter_by(email_id=email_id).first()
    
    if existing_user is None:
        user = UserData(name=name, email_id=email_id, phn_number=phn_number, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('register.html', existing=True)

@app.route('/loginfresh')
def loginfresh():
    users = UserData.query.all()

    for user in users:
        print(user.email_id)
        print(user.password)

    return render_template('loginfresh.html')


@app.route('/loginsubmit', methods=['POST'])
def loginsubmit():
    email_id = request.form['email_id']
    password = request.form['password']
    user = UserData.query.filter_by(email_id=email_id).first()
    if user is not None:
        if password == user.password:
             return redirect(url_for('index'))
        else:
            return render_template('loginfresh.html', unkonwn=True)
    else:
        return render_template('loginfresh.html', unkonwn=True)

       

    


if __name__ == "__main__":
    app.run(debug=True)

