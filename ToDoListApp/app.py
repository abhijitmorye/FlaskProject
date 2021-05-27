from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

projectdir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(projectdir, 'mydatabase.db'))

app = Flask(__name__)
app.secret_key = 'todolistapp'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserData(db.Model):

    __tablename__ = 'UserData'
    name = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(100), nullable=False,
                         primary_key=True, unique=True)
    phn_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='UserData', lazy=True)


class Task(db.Model):
    __tablename__ = 'task'
    taskid = db.Column(db.Integer, primary_key=True, unique=True)
    taskname = db.Column(db.String(100))
    taskpriority = db.Column(db.Integer)
    taskdescription = db.Column(db.String(100))
    taskcreator_id = db.Column(
        db.String(100), db.ForeignKey('UserData.email_id'))
    taskstatus = db.Column(db.String(100))


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
        user = UserData(name=name, email_id=email_id,
                        phn_number=phn_number, password=password)
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
            session['response'] = user.email_id
            print(session['response'])
            return redirect(url_for('profile'))
        else:
            return render_template('loginfresh.html', unkonwn=True)
    else:
        return render_template('loginfresh.html', unkonwn=True)


@app.route('/profile')
def profile():
    if 'response' in session:
        email_id = session['response']
        user = UserData.query.filter_by(email_id=email_id).first()
        tasks = Task.query.filter_by(taskcreator_id=user.email_id).all()
        for task in tasks:
            print(task.taskstatus)
        return render_template('profile.html', user=user, tasks=tasks)


@app.route('/tasksubmit', methods=['POST'])
def taskSubmit():
    if 'response' in session:
        email_id = session['response']
        user = UserData.query.filter_by(email_id=email_id).first()
        taskname = request.form['taskname']
        taskpriority = request.form['taskpriority']
        taskdescription = request.form['taskdescription']
        taskstatus = request.form['taskstatus']
        taskcreator_id = request.form['taskcreator_id']

        task = Task(taskname=taskname, taskpriority=taskpriority,
                    taskdescription=taskdescription, taskstatus=taskstatus, taskcreator_id=taskcreator_id)

        db.session.add(task)
        tasks = Task.query.filter_by(taskcreator_id=taskcreator_id).all()
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('/loginfresh'))


@app.route('/deletetask/<int:taskid>')
def taskdelete(taskid):
    if 'response' in session:
        Task.query.filter_by(taskid=taskid).delete()
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('profile'))


@app.route('/logout')
def logout():

    if 'response' in session:
        session.pop('response', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(debug=True)
