from flask import Flask, render_template, request
import numpy as np
import math
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
car= pd.read_csv("Car details v3.csv")
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        name=request.form['name']
        year=int(request.form['year']) 
        year =float((year - 2005) / (2020 - 2005) )
        km_driven=float(request.form['km_driven'])
        km_driven=float((km_driven - 1000) / (195000 - 1000))
        mileage=float(request.form['mileage'])
        mileage=float((mileage - 12.0) / (28.4 - 12.0))
        engine=float(request.form['engine'])
        engine=float((engine - 793) / (1896 - 793))
        max_power=float(request.form['max_power'])
        max_power=float((max_power-34.2) / (138.1 -34.2))
        seats=0.0
        transmission=request.form['transmission']
        if(transmission=='manual'):
            manual=1
        elif(transmission=='automatic'):
            manual=0
        seller_type=request.form['seller_type']
        if(seller_type=='individual'):
            individual=1
            trust_dealer=0
        elif(seller_type=='dealer'):
            individual=0
            trust_dealer=0
        elif(seller_type=='trustmark dealer'):
            individual=0
            trust_dealer=1
        fuel=request.form['fuel']
        if(fuel=='diesel'):
            diesel=1
            lpg=0
            petrol=0
        elif(fuel=='lpg'):
            diesel=0
            lpg=1
            petrol=0
        elif(fuel=='petrol'):
            diesel=0
            lpg=0
            petrol=1
        elif(fuel=='cng'):
            diesel=0
            lpg=0
            petrol=0
        owner=request.form['owner']
        if(owner=='first'):
            second=0
            third=0
            fourth=0
            test=0
        elif(owner=='second'):
           second=1
           third=0
           fourth=0
           test=0
        elif(owner=='third'):
            second=0
            third=1
            fourth=0
            test=0
        elif(owner=='fourth'):
            second=0
            third=0
            fourth=1
            test=0
        elif(owner=='test'):
            second=0
            third=0
            fourth=0
            test=1
        prediction=model.predict([[year,km_driven,mileage,engine,max_power,seats,
        manual,individual,trust_dealer,diesel,lpg,petrol,fourth,second,test,third]])
        prediction=(prediction*(1227000-45000)+45000)
        if(prediction<0):
            prediction=prediction*-1
        output=round(prediction[0],2)
        return render_template("index.html",prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)