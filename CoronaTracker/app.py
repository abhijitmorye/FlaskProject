from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import datetime
import json


app = Flask(__name__)

rapid_api_key = ""
rapidapi_host = "covid-19-tracking.p.rapidapi.com"
today = str(datetime.datetime.now()).split(' ')[0]

# factor {

#     ""
# }


@app.route('/')
def index():
    resp = requests.get('https://covid-19-tracking.p.rapidapi.com/v1',
                        headers={'x-rapidapi-key': rapid_api_key,
                                 'x-rapidapi-host': rapidapi_host})
    coronaData = json.loads(resp.text)
    data = coronaData[0]
    # data = {'Active Cases_text': '+25,664', 'Country_text': 'World', 'Last Update': '2021-06-29 07:23', 'New Cases_text': '+17,497',
    #         'New Deaths_text': '+259', 'Total Cases_text': '182,204,682', 'Total Deaths_text': '3,945,728', 'Total Recovered_text': '166,766,167'}

    total_cases = int(data['Total Cases_text'].replace(',', ''))
    total = len(str(total_cases))
    if total == 7 or total == 6:
        total_cases = int(total_cases / 100000)
        data['Total Cases_text'] = str(total_cases) + "lacs"
        # print(str(total_cases) + "lacs")
    if total >= 8:
        total_cases = int(total_cases / 10000000)
        data['Total Cases_text'] = str(total_cases) + "Cr"

    total_rec_cases = int(data['Total Recovered_text'].replace(',', ''))
    total = len(str(total_rec_cases))
    if total == 7 or total == 6:
        total_rec_cases = int(total_rec_cases / 100000)
        data['Total Recovered_text'] = str(total_rec_cases) + "lacs"
    if total >= 8:
        total_rec_cases = int(total_rec_cases / 10000000)
        data['Total Recovered_text'] = str(total_rec_cases) + "Cr"

    total_death_cases = int(data['Total Deaths_text'].replace(',', ''))
    total = len(str(total_death_cases))
    if total == 7 or total == 6:
        total_death_cases = int(total_death_cases / 100000)
        data['Total Deaths_text'] = str(total_death_cases) + "lacs"
    if total >= 8:
        total_death_cases = int(total_cases / 10000000)
        data['Total Deaths_text'] = str(total_death_cases) + "Cr"

    topfiveData = coronaData[1:6]
    for countryData in topfiveData:
        total_cases = int(countryData['Total Cases_text'].replace(',', ''))
        total = len(str(total_cases))
        if total == 7 or total == 6:
            total_cases = int(total_cases / 100000)
            countryData['Total Cases_text'] = str(total_cases) + "lacs"
        # print(str(total_cases) + "lacs")
        if total >= 8:
            total_cases = int(total_cases / 10000000)
            countryData['Total Cases_text'] = str(total_cases) + "Cr"

        total_rec_cases = int(
            countryData['Total Recovered_text'].replace(',', ''))
        total = len(str(total_rec_cases))
        if total == 7 or total == 6:
            total_rec_cases = int(total_rec_cases / 100000)
            countryData['Total Recovered_text'] = str(total_rec_cases) + "lacs"
        if total >= 8:
            total_rec_cases = int(total_rec_cases / 10000000)
            countryData['Total Recovered_text'] = str(total_rec_cases) + "Cr"

        total_death_cases = int(
            countryData['Total Deaths_text'].replace(',', ''))
        total = len(str(total_death_cases))
        if total == 7 or total == 6:
            total_death_cases = int(total_death_cases / 100000)
            countryData['Total Deaths_text'] = str(total_death_cases) + "lacs"
        if total >= 8:
            total_death_cases = int(total_cases / 10000000)
            countryData['Total Deaths_text'] = str(total_death_cases) + "Cr"

    return render_template('index.html', data=data, topfiveData=topfiveData, flag=False, searchCountryData='')


@app.route('/search', methods=['POST'])
def getDataByCountry():
    country_name = request.form['country']
    searchResp = requests.get('https://covid-19-tracking.p.rapidapi.com/v1/{}'.format(country_name),
                              headers={'x-rapidapi-key': rapid_api_key,
                                       'x-rapidapi-host': rapidapi_host})
    searchCountryData = json.loads(searchResp.text)
    total_cases = int(searchCountryData['Total Cases_text'].replace(',', ''))
    total = len(str(total_cases))
    if total == 7 or total == 6:
        total_cases = int(total_cases / 100000)
        searchCountryData['Total Cases_text'] = str(total_cases) + "lacs"
        # print(str(total_cases) + "lacs")
    if total >= 8:
        total_cases = int(total_cases / 10000000)
        searchCountryData['Total Cases_text'] = str(total_cases) + "Cr"

    total_rec_cases = int(
        searchCountryData['Total Recovered_text'].replace(',', ''))
    total = len(str(total_rec_cases))
    if total == 7 or total == 6:
        total_rec_cases = int(total_rec_cases / 100000)
        searchCountryData['Total Recovered_text'] = str(
            total_rec_cases) + "lacs"
    if total >= 8:
        total_rec_cases = int(total_rec_cases / 10000000)
        searchCountryData['Total Recovered_text'] = str(total_rec_cases) + "Cr"

    total_death_cases = int(
        searchCountryData['Total Deaths_text'].replace(',', ''))
    total = len(str(total_death_cases))
    if total == 7 or total == 6:
        total_death_cases = int(total_death_cases / 100000)
        searchCountryData['Total Deaths_text'] = str(
            total_death_cases) + "lacs"
    if total >= 8:
        total_death_cases = int(total_cases / 10000000)
        searchCountryData['Total Deaths_text'] = str(total_death_cases) + "Cr"

    resp = requests.get('https://covid-19-tracking.p.rapidapi.com/v1',
                        headers={'x-rapidapi-key': rapid_api_key,
                                 'x-rapidapi-host': rapidapi_host})
    coronaData = json.loads(resp.text)
    data = coronaData[0]
    # data = {'Active Cases_text': '+25,664', 'Country_text': 'World', 'Last Update': '2021-06-29 07:23', 'New Cases_text': '+17,497',
    #         'New Deaths_text': '+259', 'Total Cases_text': '182,204,682', 'Total Deaths_text': '3,945,728', 'Total Recovered_text': '166,766,167'}

    total_cases = int(data['Total Cases_text'].replace(',', ''))
    total = len(str(total_cases))
    if total == 7 or total == 6:
        total_cases = int(total_cases / 100000)
        data['Total Cases_text'] = str(total_cases) + "lacs"
        # print(str(total_cases) + "lacs")
    if total >= 8:
        total_cases = int(total_cases / 10000000)
        data['Total Cases_text'] = str(total_cases) + "Cr"

    total_rec_cases = int(data['Total Recovered_text'].replace(',', ''))
    total = len(str(total_rec_cases))
    if total == 7 or total == 6:
        total_rec_cases = int(total_rec_cases / 100000)
        data['Total Recovered_text'] = str(total_rec_cases) + "lacs"
    if total >= 8:
        total_rec_cases = int(total_rec_cases / 10000000)
        data['Total Recovered_text'] = str(total_rec_cases) + "Cr"

    total_death_cases = int(data['Total Deaths_text'].replace(',', ''))
    total = len(str(total_death_cases))
    if total == 7 or total == 6:
        total_death_cases = int(total_death_cases / 100000)
        data['Total Deaths_text'] = str(total_death_cases) + "lacs"
    if total >= 8:
        total_death_cases = int(total_cases / 10000000)
        data['Total Deaths_text'] = str(total_death_cases) + "Cr"

    topfiveData = coronaData[1:6]
    for countryData in topfiveData:
        total_cases = int(countryData['Total Cases_text'].replace(',', ''))
        total = len(str(total_cases))
        if total == 7 or total == 6:
            total_cases = int(total_cases / 100000)
            countryData['Total Cases_text'] = str(total_cases) + "lacs"
        # print(str(total_cases) + "lacs")
        if total >= 8:
            total_cases = int(total_cases / 10000000)
            countryData['Total Cases_text'] = str(total_cases) + "Cr"

        total_rec_cases = int(
            countryData['Total Recovered_text'].replace(',', ''))
        total = len(str(total_rec_cases))
        if total == 7 or total == 6:
            total_rec_cases = int(total_rec_cases / 100000)
            countryData['Total Recovered_text'] = str(total_rec_cases) + "lacs"
        if total >= 8:
            total_rec_cases = int(total_rec_cases / 10000000)
            countryData['Total Recovered_text'] = str(total_rec_cases) + "Cr"

        total_death_cases = int(
            countryData['Total Deaths_text'].replace(',', ''))
        total = len(str(total_death_cases))
        if total == 7 or total == 6:
            total_death_cases = int(total_death_cases / 100000)
            countryData['Total Deaths_text'] = str(total_death_cases) + "lacs"
        if total >= 8:
            total_death_cases = int(total_cases / 10000000)
            countryData['Total Deaths_text'] = str(total_death_cases) + "Cr"

    return render_template('index.html',  data=data, topfiveData=topfiveData, flag=True, searchCountryData=searchCountryData)


if __name__ == '__main__':
    app.run(debug=True)
