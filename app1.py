from flask import Flask,render_template,request,redirect,session
import numpy as np
import re
from flask_sqlalchemy import SQLAlchemy
import pickle
from mysql.connector import connect
from flask_mail import Mail, Message
app1=Flask(__name__)
new_model=pickle.load(open(r"C:\Users\Kartik\PycharmProjects\heart_disease\trained_model.sav","rb"))


@app1.route('/')
def homepage():
        # return render_template("index1.html")
    return render_template("index2.html")


@app1.route('/predict')
def predict():
    # connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
    # cur=connection.cursor()
    age=request.args.get("age")
    sex=request.args.get("sex")
    cp=request.args.get("cp")
    trestbps=request.args.get("trestbps")
    chol=request.args.get("chol")
    fbs=request.args.get("fbs")
    restecg=request.args.get("restecg")
    thalach=request.args.get("thalach")
    exang=request.args.get("exang")
    oldpeak=request.args.get("oldpeak")
    slope=request.args.get("slope")
    ca=request.args.get("ca")
    thal=request.args.get("thal")
    
    input_data = tuple(map(int,(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)))
    # change the input data to a numpy array
    input_data_as_numpy_array= np.asarray(input_data)

    # reshape the numpy array as we are predicting for only on instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    print(input_data_reshaped)

    prediction = new_model.predict(input_data_reshaped)
    print(prediction)
            
    if prediction[0]==0:
        return render_template("index2.html",output='The Person Does not have a Heart Disease')
    return render_template("index2.html",output='The Person have a Heart Disease')


app1.run()