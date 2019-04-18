import numpy as np
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, Markup, escape

# Create an engine for the  database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement 
Station = Base.classes.station 

session=Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation") 
def precipitation(): 
   
    query_results = session.query(Measurement.date, Measurement.prcp).all()
        
      #Convert the query results to a Dictionary using date as the key and prcp as the value. 
    prcp_measurements = [] 
    for result in query_results:
        date_precipitation = {} 
        date_precipitation[result.date] = result.prcp 
        prcp_measurements.append(date_precipitation) 
  
      #Return the JSON representation of your dictionary. 
    return jsonify(prcp_measurements) 

@app.route("/api/v1.0/stations")
def station_list():

    query2_results = session.query(Station.station).all()

    return jsonify(query2_results)

@app.route("/api/v1.0/tobs")
def temp_date():

    query3_results = session.query(Measurement.tobs, Measurement.date).\
          filter(Measurement.date>='2016-08-23',Measurement.date <='2017-08-23').all() 

    temps = [] 
    for temp in query3_results:
        date_temp = {} 
        date_temp["date"] = Measurement.date 
        date_temp["tobs"] = Measurement.tobs
        temps.append(date_temp)     
    
    
    return jsonify(query3_results)

@app.route("/api/v1.0/start")
def start():

    query4_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>='2016-08-23')
      
    start_temps = []   
    for tmin, tmax, tavg in query4_results:
        temps = {}
        temps["Lowest Temperature"] = tmin
        temps["Average Temperature"] = tavg
        temps["Max Temperature"] = tmax
        start_temps.append(temps)
    
    return jsonify(start_temps)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    start = '2016-08-23'
    end = '207-08-23'

    query5_results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end)

    startend_temps = []
    for tmin, tavg, tmax in query5_results:
        setemps = {}
        setemps["Lowest Temperature"] = tmin
        setemps["Average Temperature"] = tavg
        setemps["Max Temperature"] = tmax
        startend_temps.append(setemps)

    return jsonify(startend_temps)

if __name__ == '__main__':
    app.run(debug=True)

 