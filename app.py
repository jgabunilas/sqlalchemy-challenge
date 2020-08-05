# Climate App for SQLAlchemy Challenge
## Written by Jason Gabunilas

# import dependencies for Flask
from flask import Flask, jsonify

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
        )

@app.route("/api/v1.0/precipitation")
def precip():
        # Create our session (link) from Python to the DB
        session = Session(engine)

        # Query all precipitation data by date
        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > dt.date(2016, 8, 23)).all()

        session.close()

        # Convert the results to a dictionary
        # Initialize the empty dictionary
        precip_data = {}
        for result in results:
                if result[1] == None:
                        pass
                elif result[0] not in precip_data:
                        precip_data[result[0]] = []
                        precip_data[result[0]].append(result[1])
                else:
                        precip_data[result[0]].append(result[1])
        
        return jsonify(precip_data)


if __name__ == "__main__":
    app.run(debug=True)