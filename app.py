# Climate App for SQLAlchemy Challenge
## Written by Jason Gabunilas

# import dependencies for Flask
from flask import Flask, jsonify, escape

# import dependencies for SQLAlchemy, numpy, and datetime
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
        return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/{escape('<start>')} (please enter start date in the following format: YYYY-MM-DD)<br/>"
        f"/api/v1.0/{escape('<start>')}/{escape('<end>')}<br/> (please enter start and end dates in the following format: YYYY-MM-DD)"        
        )

@app.route("/api/v1.0/precipitation")
def precip():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        # Query all precipitation data by date, filtering by the last year
        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016, 8, 23)).all()

        # Close the connection session to the database
        session.close()

        # Convert the query results to a dictionary
        # Initialize the empty dictionary
        precip_data = {}

        # The results is a list of tuples, each tuple containing the measurement date at [0] and prcp at [1]. Iterate through each tuple in a for loop.
        for result in results:
                # If the current tuple contains a null value for precipitation, skip it
                if result[1] == None:
                        pass
                # If the current date is not currently a dey in the dictionary, add the key, initialize it to an empty list, then append the precipitation value to that list
                elif result[0] not in precip_data:
                        precip_data[result[0]] = []
                        precip_data[result[0]].append(result[1])
                # If the current date already exists as a key in the dictionary, append the precipitation to the list associated with that
                else:
                        precip_data[result[0]].append(result[1])
        
        return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def station():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        # Query all precipitation data by date, filtering by the last year
        station_results = session.query(Measurement.station).all()

        # Close the connection session to the database
        session.close()

        # Convert the query results to a dictionary
        # Initialize an empty list of stations
        stations_list = []

        for result in station_results:
                if result[0] not in stations_list:
                        stations_list.append(result[0])

        return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        # Query all precipitation data by date, filtering by the last year's worth of data
        temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= dt.date(2016, 8, 23)).all()

        # Close the connection session to the database
        session.close()

        # Convert the query results to a dictionary
        # Initialize an empty list of temperatures
        # temp_list = []
        # for result in temp_results:
        #         temp_list.append(result[1])

        return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
def min_avg_max_start(start):
        # Create our session (link) from Python to the DB
        session = Session(engine)

        # Query the temperature data, filtering by the start date provided in the URL
        results = session.query(Measurement.tobs).filter(Measurement.date >= start).all()

        # Initialize empty temperaturse list
        temps_in_range = []

        # Iterate through the query results and append each temperature to the list
        for result in results:
                temps_in_range.append(result[0])
        
        # Calculate the min, avg, and max temperatures in that date range
        min_temp = min(temps_in_range)
        avg_temp = (sum(temps_in_range) / len(temps_in_range))
        max_temp = max(temps_in_range)

        return f"From the date starting {start} through 2017-08-23, <br/> the minimum recorded temperature was {min_temp}, <br/> the average recorded temperature was {avg_temp:.01f}, <br/> and the maximum recorded temperature was {max_temp}."

@app.route("/api/v1.0/<start>/<end>")
def min_avg_max_start_end(start, end):
        # Create our session (link) from Python to the DB
        session = Session(engine)

        # Query the temperature data, filtering by the start and end dates provided in the URL
        results = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        # Initialize empty temperaturse list
        temps_in_range = []

        # Iterate through the query results and append each temperature to the list
        for result in results:
                temps_in_range.append(result[0])
        
        # Calculate the min, avg, and max temperatures in that date range
        min_temp = min(temps_in_range)
        avg_temp = (sum(temps_in_range) / len(temps_in_range))
        max_temp = max(temps_in_range)

        return f"From the date starting {start} through {end}, <br/> the minimum recorded temperature was {min_temp}, <br/> the average recorded temperature was {avg_temp:.01f}, <br/> and the maximum recorded temperature was {max_temp}."

if __name__ == "__main__":
    app.run(debug=True)