import numpy as np

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

app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def index():
    routes = ["/api/v1.0/precipitation","/api/v1.0/stations","/api/v1.0/tobs","/api/v1.0/<start>","/api/v1.0/<start>/<end>"]
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement).where(Measurement.date >= '2016-08-23').all()
    session.close()
    dates = []
    precipitation = []
    
    for row in results:
        dates.append(row.date)
        precipitation.append(row.prcp)

    precipitation_dates = {dates[i]: precipitation[i] for i in range(len(dates))}
    return jsonify(precipitation_dates)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_count = session.query(Measurement.station).distinct()
    session.close()
    stations = []
    for station in station_count:
        stations.append(station.station)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs = session.query(Measurement.tobs, Measurement.date).where(Measurement.station == 'USC00519281').where(Measurement.date >= '2016-08-23')
    session.close()
    date = []
    tobs_list = []
    for row in tobs:
        date.append(row.date)
        tobs_list.append(row.tobs)
    tobs_dates = {date[i]: tobs_list[i] for i in range(len(date))}
    return jsonify(tobs_dates)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    measured_temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).where(Measurement.station == 'USC00519281').where(Measurement.date >= start)
    session.close()
    temp_values = []
    temp_quality = ["Minimum Temp", "Maximum Temp", "Average Temp"]
    for temp in measured_temp:
        temp_values.append(temp[0])
        temp_values.append(temp[1])
        temp_values.append(temp[2])
    temp_return = {temp_quality[i]: temp_values[i] for i in range(len(temp_quality))}
    return jsonify(temp_return)

@app.route("/api/v1.0/<start>/<end>")
def temp_date(start,end):
    session = Session(engine)
    measured_temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).where(Measurement.station == 'USC00519281').where(Measurement.date >= start).where(Measurement.date <= end)
    session.close()
    temp_values = []
    temp_quality = ["Minimum Temp", "Maximum Temp", "Average Temp"]
    for temp in measured_temp:
        temp_values.append(temp[0])
        temp_values.append(temp[1])
        temp_values.append(temp[2])
    temp_return = {temp_quality[i]: temp_values[i] for i in range(len(temp_quality))}
    return jsonify(temp_return)




# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
