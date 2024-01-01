
#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'

'''
Define the database model
that is used to store
the temperature.
'''

db = SQLAlchemy(app)
class Weather(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    temperature = db.Column(db.Integer, nullable=False)
    
'''
Helper function to get temperature
using API
'''

def get_temperature():
    response = requests.get("https://weatherdbi.herokuapp.com/data/weather/boulder")
    return response.json()["currentConditions"]["temp"]["c"]


'''
In main we first get the current temperature and then
create a new object that we can add to the database.
'''
if __name__ == "__main__":
    current_temperature = get_temperature()
    new_entry = Weather(temperature=current_temperature)
    db.session.add(new_entry)
    db.session.commit()
