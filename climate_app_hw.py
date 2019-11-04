import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all routes that are available"""
    return(
        f"Available Roues:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"Put the start date in 'YYYY-MM-DD' format<br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"Put the START and END dates in 'YYYY-MM-DD/YYYY-MM-DD' format<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    rain_last_year = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date.between('2016-08-24', '2017-08-23')).\
        order_by(Measurement.date).all()

    return jsonify(dict(rain_last_year))

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station, Station.name).all()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    temp_last_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-08-24', '2017-08-23')).\
            order_by(Measurement.date).all()

    return jsonify(temp_last_year)

@app.route("/api/v1.0/<start>")
def start_time(start):
    date_temp_summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    for temp in date_temp_summary:
        summary = {"Minimum Temp":date_temp_summary[0][0],"Average Temp":date_temp_summary[0][1],
        "Maximum Temp ":date_temp_summary[0][2]}

    return jsonify(summary)

@app.route("/api/v1.0/<start>/<end>")
def start_end_time(start, end):
    daterange_temp_summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    for temp in daterange_temp_summary:
        summary = {"Minimum Temp":daterange_temp_summary[0][0],"Average Temp":daterange_temp_summary[0][1],
        "Maximum Temp ":daterange_temp_summary[0][2]}

    return jsonify(summary)


if __name__ == "__main__":
    app.run(debug=True)