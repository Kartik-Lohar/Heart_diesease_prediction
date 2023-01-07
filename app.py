from flask import Flask,render_template,request,redirect,session
import numpy as np
import re
from flask_sqlalchemy import SQLAlchemy
import pickle
from mysql.connector import connect
from flask_mail import Mail, Message
app=Flask(__name__)
new_model=pickle.load(open(r"C:\Users\Kartik\PycharmProjects\heart_disease\trained_model.sav","rb"))

app.secret_key = 'ghjhjhq/213763fbf'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='kartikpanchal1409@gmail.com',
    MAIL_PASSWORD='01Kartik23'
)
db = SQLAlchemy(app)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kartik14@localhost/kartik'
heart = db.Table('heart', db.metadata, autoload=True, autoload_with=db.engine)
heart_attribute = db.Table('heart_attribute', db.metadata, autoload=True, autoload_with=db.engine)
heart_disease_message=""
@app.route('/')
def homepage():
    if 'userid' in session:
        return render_template("index1.html")
    return render_template("index.html")


@app.route('/predict')
def predict():
    connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
    cur=connection.cursor()
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
    global heart_disease_message
    heart_disease_message=""
    if 'userid' in session:
        id=session["userid"]
        if (prediction[0]== 0):
            heart_disease_message='The Person does not have a Heart Disease'
            query = "insert into heart_attribute values({},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(*input_data,prediction[0],id)
            connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
            cur=connection.cursor()
            cur.exceute(query)
            connection.commit()
            return render_template("index.html",output='The Person does not have a Heart Disease')
        else:
            query = "insert into heart_attribute values({},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(*input_data,prediction[0],id)
            connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
            cur=connection.cursor()
            cur.exceute(query)
            connection.commit()
            heart_disease_message='The Person have a Heart Disease'
            return render_template("index.html",output='The Person have a Heart Disease')
    else:
        if (prediction[0]== 0):
            heart_disease_message='The Person does not have a Heart Disease'
            query = "insert into heart_attribute (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,result) values({},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(*input_data,prediction[0])
            connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
            cur=connection.cursor()
            cur.execute(query)
            connection.commit()
            return render_template("index.html",output='The Person does not have a Heart Disease')
        else:
            query = "insert into heart_attribute (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,result) values({},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(*input_data,prediction[0])
            connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
            cur=connection.cursor()
            cur.execute(query)
            connection.commit()
            heart_disease_message='The Person have a Heart Disease'
            return render_template("index.html",output='The Person have a Heart Disease')


@app.route('/SignUp')
def SignUp():
    if 'userid' in session:
        return redirect('/home')
    else:
        return render_template('SignUp.html')


@app.route('/register')
def register():
    email = request.args.get('email')
    username = request.args.get('uname')
    pwd = request.args.get('pwd')
    if email == None or username == None or pwd == None:
        return render_template('SignUp.html', error1="Please fill all details")
    email_check = re.fullmatch("^([a-z\d\._-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$", email)
    if email_check is None:
        return render_template('SignUp.html',
                               error1="Please enter valid mail id or it should be in lowercase letters instead of uppercase")
    psw_check = re.fullmatch("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", pwd)
    if psw_check is None:
        return render_template("SignUp.html", error1="Password should be of required format")
    username_check = re.fullmatch("[a-zA-Z_\s]{5,20}", username)
    if username_check is None:
        return render_template("Signup.html", error1="Name should be between 5 to 20 letters without any digits and special symbol except (_)")
    connection = connect(host="localhost", database="kartik", user="root", password="kartik14")
    cur = connection.cursor()
    #result_mail = "select * from heart where email={}".format(email)
    result_mail = db.session.query(heart).filter_by(email=email).one_or_none()
    # cur.execute(result_mail)
    # result = cur.fetchone()
    if result_mail is None:
        # insert_query = "insert into heart(email,username,password) values('{}','{}','{}')".format(
        #     email,
        #     username,
        #     pwd)
        insert_query = heart.insert().values(email=email, username=username, password=pwd)
        db.session.execute(insert_query)
        db.session.commit()
        #cur = connection.cursor()
        #cur.execute(insert_query)
        #connection.commit()
        return redirect('/Login')
    else:
        return render_template('SignUp.html', error="MailId already exist")


@app.route('/Login')
def Login():
    if 'userid' in session:
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/checkLoginIn')
def checkLogIn():
    email = request.args.get('email')
    password = request.args.get('pwd')
    if email == None or password == None:
        return render_template('login.html', error="Please Fill all Details")
    # connection = connect(host="localhost", database="kartik", user="root", password="kartik14")
    # cur = connection.cursor()
    print(email)
    #email=str(email)
    result_mail = db.session.query(heart).filter_by(email=email).one_or_none()
    # result_mail = "select * from heart where email={email}".format(email=email)
    # cur.execute(result_mail)
    # result = cur.fetchone()
    #print(result)
    if result_mail is None:
        return render_template('login.html', error='you are not registered')
    else:
        if password == result_mail[5]:
            session['email'] = email
            session['userid'] = result_mail[0]
            # return render_template('UserHome.html')
            #mail(email,result_mail[0])
            return redirect('/')
        else:
            return render_template('Login.html', error='your password is not correct')

def mail(email,id):
    connection=connect(host='localhost', database='kartik', user='root', password='kartik14')
    mail_query="select * from heart_attributes where created_by={}".format(id)
    cur=connection.cursor()
    body = heart_disease_message + "\n Your heart details are: "
    #email = session["email"]
    msg = Message(subject='Forget Password Email', sender='kaps4332@gmail.com',
                  recipients=[email], body=body,html=render_template("updateUrl.html"))
    msg.cc = ['kartik12@gmail.com']
    mail.send(msg)

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return render_template('login.html')

app.run()