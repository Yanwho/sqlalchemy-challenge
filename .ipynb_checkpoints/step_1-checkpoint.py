## import required modules
# matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
from pprint import pprint
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date

## Begin Code
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Create our session (link) from Python to the DB
session = Session(bind=engine)
session
# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect = True)
# We can view all of the classes that automap found
base.classes.keys()
# Save references to each table
measurement = base.classes.measurement
station = base.classes.station
session = Session(bind=engine)

# Precipitation Analysis
# Design a query to retrieve the last 12 months of precipitation data.

# Select only the date and prcp values.

# Load the query results into a Pandas DataFrame and set the index to the date column.

# Sort the DataFrame values by date.

# Plot the results using the DataFrame plot method.

# Use Pandas to print the summary statistics for the precipitation data.