import pandas as pd
import numpy as np
from flask import Flask,render_template,request,redirect
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.distance import great_circle
import pickle

# making flask app
app = Flask(__name__)

# making random forest classifier model

def valuePredict(col_list):
    loaded_model = pickle.load(open("model.pkl","rb"))
    predictedValue = loaded_model.predict(col_list)
    return predictedValue

# routing home page of model
@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():
    
    if request.method=="POST":
        fullName = request.form['fullName']
        gender = request.form['gender']
        if gender=='Male':
            gender = 1
        else:
            gender = 0
        custType = request.form['cust-type']
        if custType=='disloyal Customer':
            custType=1
        else:
            custType=0
        age = request.form['age']
        travelType = request.form['travel-type']
        if travelType=='Personal Travel':
            travelType=1
        else:
            travelType=0
        custClass = request.form['cust-class']
        if custClass=='Eco Plus':
            custClass_eco_plus=1
            custClass_eco = 0
        elif custClass=='Business':
            custClass_eco=0
            custClass_eco_plus=0
        else:
            custClass_eco=1
            custClass_eco_plus=0
        source = request.form['source']
        destination = request.form['destination']
        city_list = [source,destination]
        longitude = []
        latitude = []
        for city in city_list:
            geolocator = Nominatim(user_agent="Airline Passenger Satisfaction Predictor")
            city = geolocator.geocode(city,timeout=10000)
            latitude.append(city.latitude)
            longitude.append(city.longitude)
          
        source_city = (latitude[0],longitude[0]) 
        destination_city = (latitude[1],longitude[1])


        flightDistance = geodesic(source_city, destination_city).km
        # if flightDistance<1000:
        #     flightDistance = great_circle(source_city,destination_city).miles
        wifiService = request.form['wifi-service']
        departureArrivalTimeConvinient = request.form['datc']
        easeOfOnlineBooking = request.form['eoob']
        gateLocation = request.form['gate-loc']
        foodDrink = request.form['food_drink']
        onlineBoarding = request.form['online_boarding']
        seatComfort = request.form['seat_comfort']
        inflightEntertainment = request.form['inflight_entertainment']
        onboardService = request.form['onboard_service']
        legRoomService = request.form['leg_room_service']
        baggageHandling = request.form['baggage_handling']
        checkinService = request.form['checkin_service']
        inflightService = request.form['inflight_service']
        cleanliness = request.form['cleanliness']
        departureDelayInMin = request.form['departure_delay_in_minutes']
        arrivalDelayInMin = request.form['arrival_delay_in_minutes']
        col_list = [[age,flightDistance,wifiService,departureArrivalTimeConvinient,easeOfOnlineBooking,gateLocation,foodDrink,onlineBoarding,seatComfort,inflightEntertainment,onboardService,legRoomService,baggageHandling,checkinService,inflightService,cleanliness,departureDelayInMin,arrivalDelayInMin,custClass_eco,custClass_eco_plus,travelType,custType,gender]]
        predictedValue = valuePredict(col_list)
        if predictedValue==0:
            result = "Customer Is Not Satisfied"
        else:
            result = "Customer Is Satisfied"
        return render_template('predict.html',predict = result)

@app.route("/",methods=['GET'])
def returnHome():
    if request.method=='GET':
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)