# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Welcome to the Honolulu, Hawaii Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation data for the last 12 months<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the last 12 months from the most active station<br/>"
        f"/api/v1.0/start - Temperature statistics from a specific start date (yyyy-mm-dd)<br/>"
        f"/api/v1.0/start/end - Temperature statistics for a date range (yyyy-mm-dd/yyyy-mm-dd)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the last 12 months of precipitation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the results to a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)   
    # Retrieve a list of all station names
    station_data = session.query(Station.station, Station.name).all()
    station_list = [{"Station ID": station[0], "Station Name": station[1]} for station in station_data]

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date one year ago from the most recent date in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = most_recent_date[0]
    one_year_ago = (dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)).date()

    # Find the most active station
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_active_station = station_activity[0]

    # Query temperature observations for the most active station in the last year
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station, Measurement.date >= one_year_ago).all()

    # Create a list of dictionaries for the temperature data
    temperature_list = []
    for date, tobs in temperature_data:
        temperature_dict = {
            "Date": date,
            "Temperature": tobs
        }
        temperature_list.append(temperature_dict)
        # Create a dictionary response that includes station info and temperature data
    response = {
        "Most Active Station": most_active_station,
        "Temperature Observations": temperature_list
    }
    return jsonify(response)



@app.route('/api/v1.0/<start>')
def temperature_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the start date provided in the URL to a datetime object
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    # Query the database to calculate temperature statistics for dates greater than or equal to the start date
    temperature_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

    if not temperature_stats:
        return jsonify({"error": "No data found for the given start date."}), 404

    # Return the temperature statistics as JSON
    return jsonify({
        "Start Date": start_date.strftime('%Y-%m-%d'),
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    })

@app.route('/api/v1.0/<start>/<end>')
def temperature_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the start and end dates provided in the URL to datetime objects
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    # Query the database to calculate temperature statistics for a date range
    temperature_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    if not temperature_stats:
        return jsonify({"error": "No data found for the given date range."}), 404

    # Return the temperature statistics as JSON
    return jsonify({
        "Start Date": start_date.strftime('%Y-%m-%d'),
        "End Date": end_date.strftime('%Y-%m-%d'),
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    })

if __name__ == '__main__':
    app.run(debug=True)
