from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import json
import datetime

proj_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(proj_dir, 'mydatabase.db'))
app = Flask(__name__)
api_key = '0a11c784d3d00762354e1ad0735bab12'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


class HistoricData(db.Model):

    __tablename__ = 'HistoricData'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cityname = db.Column(db.String(100))
    default_date = str(datetime.datetime.now()).split()
    date = db.Column(db.String(100), default=default_date[0])
    temparature = db.Column(db.String(100))
    min_temparature = db.Column(db.String(100))
    max_temparature = db.Column(db.String(100))
    humidity = db.Column(db.String(100))


@app.route('/')
def index():
    return render_template('index.html', ResultExists=False)


@app.route('/search', methods=['POST'])
def serach():

    city = request.form['city']
    resp = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, api_key))
    result = json.loads(resp.text)
    print(result['name'])

    cityname = result['name']
    temparature = result['main']['temp']
    min_temparature = result['main']['temp_min']
    max_temparature = result['main']['temp_max']
    humidity = result['main']['humidity']

    cityExists = HistoricData.query.filter_by(cityname=cityname).first()
    todayDate = str(datetime.datetime.now()).split()

    if cityExists is not None:
        if cityExists.date == todayDate:
            pass
        else:
            newTemp = HistoricData(cityname=cityname, temparature=temparature,
                                   min_temparature=min_temparature, max_temparature=max_temparature, humidity=humidity)
        db.session.add(newTemp)
        db.session.commit()
    else:
        newTemp = HistoricData(cityname=cityname, temparature=temparature,
                               min_temparature=min_temparature, max_temparature=max_temparature, humidity=humidity)
        db.session.add(newTemp)
        db.session.commit()

    context = {
        'city_name': result['name'],
        'temp': result['main']['temp'],
        'weather': result['weather'][0]['main'],
        'weather_desc': result['weather'][0]['description'],
        'temp_min': result['main']['temp_min'],
        'temp_max': result['main']['temp_max'],
        'humidity': result['main']['humidity']
    }
    return render_template('index.html', ResultExists=True, context=context)


if __name__ == "__main__":
    app.run(debug=True)
