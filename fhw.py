import numpy as np
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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
        # f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start_date>/<end_date>"
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
        date_temp= {} 
        date_temp["date"] = Measurement.date 
        date_temp["tobs"] = Measurement.tobs
        temps.append(temps)     
    
    
    return jsonify(query3_results)

@app.route("/api/v1.0/<start>")
def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2018, 8, 9)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


# @app.route("/api/v1.0/<start_date>/", defaults = {'end_date': None})
# @app.route("/api/v1.0/<start_date>/<end_date>/")
# def temp_lookup(start_date,end_date):
# 	try:
# 		# check if start_date and end_date are entered in the correct date format
# 		start_date = '2016-08-23'
# 		if end_date:
# 			end_date ='2017-08-23'
# 		# when end_date is not provided, query the data with date greater or equal to start_date
# 		if end_date is None:
# 			result = {}
# 			min = session.query(Measurement.date,func.min(Measurement.tobs))\
# 			    .filter(Measurement.date >= start_date).all()
# 			max = session.query(Measurement.date,func.max(Measurement.tobs))\
# 			    .filter(Measurement.date >= start_date).all()    
# 			avg = session.query(Measurement.date,func.avg(Measurement.tobs))\
# 			    .filter(Measurement.date >= start_date).all()    
			    
# 			result['TMIN'] = min[0][1]
# 			result['TMAX'] = max[0][1]
# 			result['TAVG'] = avg[0][1]

# 			return jsonify(result)
# 		# when end_date is provided, query the data between start_date and end_date, both inclusive
# 		result = {}
# 		min = session.query(Measurement.date,func.min(Measurement.tobs))\
# 		    .filter(Measurement.date >= start_date)\
# 		    .filter(Measurement.date <= end_date).all()
# 		max = session.query(Measurement.date,func.max(Measurement.tobs))\
# 		    .filter(Measurement.date >= start_date)\
# 		    .filter(Measurement.date <= end_date).all()  
# 		avg = session.query(Measurement.date,func.avg(Measurement.tobs))\
# 		    .filter(Measurement.date >= start_date)\
# 		    .filter(Measurement.date <= end_date).all()   
		    
# 		result['TMIN'] = min[0][1]
# 		result['TMAX'] = max[0][1]
# 		result['TAVG'] = avg[0][1]
# 		return jsonify(result)
# 	# if start_date or end_date not entered in the correct date format, show reminder for correct format
# 	except ValueError:
# 		return 'Please enter date in YYYY-MM-DD format'   

# @app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")



# def return_weather(start, end=None):
#     if end is None:
#         end = get_most_recent_date()

#     weather_from_to = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),
#                                      func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).\
#         filter(Measurement.date <= end).all()

#     list_data = []
#     for record in  weather_from_to:
#         list_data.append({'TMIN': record[0],
#                      'TAVG': record[1],
#                      'TMAX': record[2]})

#     return jsonify(list_data)
# def temps_in_range():
#     query4_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs), Measurement.date).\
#           filter(Measurement.date>='2016-08-23',Measurement.date <='2017-08-23').all() 

#     result = {}
# 		min = session.query(Measurement.date,func.min(Measurement.tobs))\
# 		    .filter(Measurement.date>='2016-08-23',Measurement.date <='2017-08-23').\
# 		max = session.query(Measurement.date,func.max(Measurement.tobs))\
# 		    .filter(Measurement.date>='2016-08-23',Measurement.date <='2017-08-23').\
# 		avg = session.query(Measurement.date,func.avg(Measurement.tobs)).\
# 		    .filter(Measurement.date>='2016-08-23',Measurement.date <='2017-08-23').all() 
		    
# 		result['TMIN'] = min[0][1]
# 		result['TMAX'] = max[0][1]
# 		result['TAVG'] = avg[0][1]
# 		return jsonify(result) 


if __name__ == '__main__':
    app.run(debug=True)

   #.filter(Measurement.date>search_start_date,Measurement.date <= search_end_date).all() 
         #Query for the dates and precipitation from 3 years to 2 years ago. 
    
    # today = dt.date.today() 
    # search_end_date = today - dt.timedelta(days = 365) 
    # search_start_date = search_end_date -dt.timedelta(days = 365) 
     
    #   #convert datetime objects to strings 
    # search_start_date = search_start_date.strftime("%Y-%m-%d") 
    # search_end_date = search_end_date.strftime("%Y-%m-%d") 