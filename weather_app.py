import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False) 

Base = automap_base()

Base.prepare(engine, reflect=True)

Base.classes.keys()


Measurement= Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)

@app.route("/")
def Homepage():
    """List all the api routes."""
    return (
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"/api/v1.0/temp/<start><br/>" 
    ) 



@app.route("/api/v1.0/percipitation")
def percipitation():
    
    session = Session(engine)
    
    """Returning date as key and prcp as value"""
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    #all_prcp = {date: results[0] for results in results}
    all_prcp = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)



    #all_prcp[[results[0] for results in results]] = [results[1] for results in results]
    
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def station():
    
    session = Session(engine)
    
    """Returning date as key and prcp as value"""
    
    results = session.query(Measurement.station).all()
    
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    """Returning most active station"""
    
    previous_year_start = '2016-08-20'

    previous_year_end = '2016-08-30'

    results = session.query(Measurement.tobs).filter(Measurement.date >= previous_year_start)\
        .filter(Measurement.station == 'USC00519397').all()

    
    
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/start/end")
def calc_temps(start_date=None, end_date=None):


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    temps = list(np.ravel(results))


    return jsonify(temps)

    


    if end_date not in calc_temps:

        
       
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start_date).all()

        temps = list(np.ravel(results))

        return jsonify(temps)

    


    
        
    
if __name__ == "__main__":
    app.run(debug=True)

