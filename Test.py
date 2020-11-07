# %matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt
from datetime import datetime, timedelta
from pprint import pprint


# # Reflect Tables into SQLAlchemy ORM

# In[4]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date


# In[5]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[6]:


# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect = True)


# In[7]:


# We can view all of the classes that automap found
base.classes.keys()
# https://www.learnpython.org/en/Classes_and_Objects   (understand difference between object and classes)


# In[8]:


# Save references to each table
measurement = base.classes.measurement
station = base.classes.station
station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(bind=engine)
session


# # Exploratory Climate Analysis

# In[10]:


cmd = """SELECT date
FROM measurement
"""
print(pd.read_sql(cmd, con=engine))



## Flask API
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
app = Flask(__name__)

# /
# Home page.
# List all routes that are available.
@app.route("/")
def main():
	return (
        """These are the available routes.<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/start<br/>
        /api/v1.0/start/end<br/>""")




# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
	one_year_ago_query = session.query(measurement).filter(measurement.date >= one_year_ago,  measurement.date <= last_date)return "Convert the query results to a dictionary using date as the key and prcp as the value"
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
        
# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
	return "These are the 9 stations"
# Return a JSON list of stations from the dataset.


# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
	
    # """These are the dates and temperature observations of the most active station for the last year of data
    # JSON list of temperature observations (TOBS) for the previous year"""
# most_active_last12_1 = 
        last_date = session.query(func.max(measurement.date)).first()[0]
        date_time_obj = dt.datetime.strptime(last_date, '%Y-%m-%d')
        one_year_ago = date_time_obj - timedelta(days=365)
        most_active_last12 = session.query(measurement.tobs, measurement.date).filter(measurement.station == 'USC00519281').filter(measurement.date >= one_year_ago,  measurement.date <= last_date).all()
        # most_active_last12_1_df = pd.DataFrame(most_active_last12, columns=["date", "temp"])
        temps = list(np.ravel(most_active_last12))
        
        return jsonify(temps=temps)  
    # )
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

# /api/v1.0/<start> 
@app.route("/api/v1.0/<start>")
def start(start):
	return (
        """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date<bd/>
        Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.""")
# When g    iven the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
	return (
        """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive<bd/>
        Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.""")
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.



# Hints
# You will need to join the station and measurement tables for some of the queries.

# Use Flask jsonify to convert your API data into a valid JSON response object.


if __name__ == "__main__":
	app.run(debug=True)

