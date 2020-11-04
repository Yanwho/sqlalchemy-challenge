#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().run_line_magic('matplotlib', 'inline')
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

# SELECT DATEADD(month, -2, '2017/08/25') AS DateAdd;
# Design a query to retrieve the last 12 months of precipitation data and plot the results

# result = session.query(func.strftime("%Y-%m-%d",measurement.date).all()
# # Calculate the date 1 year ago from the last data point in the database

# # Perform a query to retrieve the data and precipitation scores

# # Save the query results as a Pandas DataFrame and set the index to the date column

# # Sort the dataframe by date

# # Use Pandas Plotting with Matplotlib to plot the data


# In[29]:


last_date = session.query(func.max(measurement.date)).first()[0]
print("The last day data was collected was: " + last_date)


# In[12]:


type(last_date)


# In[13]:


date_time_obj = dt.datetime.strptime(last_date, '%Y-%m-%d')
date_time_obj


# In[14]:


type(date_time_obj)
# convert this one to datetime.delta for te


# In[15]:


type(dt.timedelta(days=365))


# In[28]:


one_year_ago = date_time_obj - timedelta(days=365)
print("The last year of data collection began: " + str(one_year_ago))


# In[31]:


one_year_ago_query = session.query(measurement).filter(measurement.date >= one_year_ago,  measurement.date <= last_date)
one_year_ago_query


# In[42]:


last_year_df = pd.read_sql(one_year_ago_query.statement, one_year_ago_query.session.bind)
print("This dataframe includes the last year of data via multiple session queries : ")
last_year_df


# In[41]:


prcp_data_df = pd.read_sql("SELECT * FROM measurement WHERE date > '2016-08-23'", con=engine)
print("This dataframe includes the last year of data from via single line query: ")
prcp_data_df


# In[40]:


# Use Pandas to calcualte the summary statistics for the precipitation data
prcp_summary = prcp_data_df[["prcp"]].describe()
print("The summary of precip data from the last year is: ") 
prcp_summary


# In[21]:


# Design a query to show how many stations are available in this dataset?
station_count = session.query(station).count()
station_count


# In[44]:


# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
activity_count = (session.query(measurement.id, measurement.station, measurement.date, measurement.prcp, measurement.tobs, func.count(measurement.date)).group_by(measurement.station).order_by(func.count(measurement.date).desc()).all())
print("This is the activity count: ")
pprint(activity_count)


# In[23]:


activity_count_2 = session.query(measurement.id, measurement.station, measurement.date, measurement.prcp, measurement.tobs)
print(activity_count_2)


# In[24]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?


# In[25]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram


# ## Bonus Challenge Assignment

# In[26]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# In[ ]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.


# In[ ]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


# In[ ]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


# In[ ]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")


# In[ ]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# In[ ]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


# In[ ]:


# Plot the daily normals as an area plot with `stacked=False`

