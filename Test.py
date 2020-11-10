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


engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={"check_same_thread": False})


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
# station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(bind=engine)
# session


# # Exploratory Climate Analysis

# In[10]:


cmd = """SELECT date
FROM measurement
"""
# print(pd.read_sql(cmd, con=engine))



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
        last_date = session.query(func.max(measurement.date)).first()[0]
        date_time_obj = dt.datetime.strptime(last_date, '%Y-%m-%d')
        one_year_ago = date_time_obj - timedelta(days=365)
        one_year_ago_query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago,  measurement.date <= last_date).all()
        precip = list(np.ravel(one_year_ago_query))
        
        return jsonify(precip=precip)
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
        
# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
	
# Return a JSON list of stations from the dataset.
        station_count = str(session.query(station).count())
        
        return ("There are: " + " " + station_count + " " + "stations.")

# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
	
    # """These are the dates and temperature observations of the most active station for the last year of data
    # JSON list of temperature observations (TOBS) for the previous year"""
# most_active_last12_1 = 
        last_date_tobs = session.query(func.max(measurement.date)).first()[0]
        date_time_obj_tobs = dt.datetime.strptime(last_date_tobs, '%Y-%m-%d')
        one_year_ago_tobs = date_time_obj_tobs - timedelta(days=365)
        most_active_last12 = session.query(measurement.tobs, measurement.date).filter(measurement.station == 'USC00519281').filter(measurement.date >= one_year_ago_tobs,  measurement.date <= last_date_tobs).all()
        # most_active_last12_1_df = pd.DataFrame(most_active_last12, columns=["date", "temp"])
        temps = list(np.ravel(most_active_last12))
        
        return jsonify(temps=temps)  
    # )
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

# /api/v1.0/<start> 
@app.route("/api/v1.0/<start>")
def start_date(start):
        start_date = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).all()

        return jsonify(start_date=start_date)
# When g    iven the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.