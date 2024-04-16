from flask import Flask,render_template,request,session, url_for, redirect ,flash,jsonify
import warnings
import pymysql
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

import random
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 


app = Flask(__name__)

app.config['UPLOAD_FOLDER1'] = 'static/Users'
app.config['UPLOAD_FOLDER'] = 'static/doctor'
app.config['UPLOAD_FOLDER2'] = 'static/upload'
app.config['UPLOAD_FOLDER3'] = 'static/diseasedetect'
app.secret_key = 'any random string'
model = load_model('VGGSKin.hp5')

####################################################################################################################
                                               #Mail Person Code
#####################################################################################################################pass:ynlnfxmpwvtxolst
def sendemailtouser(usermail,message):   
    fromaddr = "info.mycitypedia@gmail.com"
    toaddr = message
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = " MYCITYPEDIA.COM"
  
    # string to store the body of the mail 
    body = message
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "lscxhzdihdxrutzr") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit()
    
##################################   Mail to patient #########################################################################




####################################################################################################################
                                               #database Connection
####################################################################################################################

def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="brainpathology")
    return connection

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        
                  
con = dbConnection()
cursor = con.cursor()
####################################################################################################################

####################################################################################################################
                                                   #main page code...
####################################################################################################################




@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html')


####################################################################################################################
                                                #DoctorSide
####################################################################################################################
@app.route('/doctor')
def doctor():
    return render_template('doctor.html') 

@app.route('/homeadmin')
def homeadmin():
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM userregisters')
    result = cursor.fetchall()
    print(result)
    return render_template('homeadmin.html',result=result) 

@app.route('/serviceadmin')
def serviceadmin():
    doctorname=session['user']
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM patientsrequest WHERE Doctorname = %s ',(doctorname))
    result = cursor.fetchall()
    print(result)
    
    return render_template('serviceadmin.html',result=result)


@app.route('/checkdisease/<id1>',methods=['POST','GET'])
def checkdisease(id1):
    print(id1)
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM patientsrequest WHERE Patient_Id = %s ',(id1))
    data = cursor.fetchone()
    print(data)
    if request.method == "POST":
       print("===============================================")
       file = request.files['file']
       usermail = request.form.get("email")
       name = request.form.get("name")
       
       print(usermail)
       print(name)
       filename = secure_filename(file.filename)
       print(filename)
       file.save(os.path.join(app.config['UPLOAD_FOLDER3'], filename))
       img = cv2.imread("static/diseasedetect/"+str(filename))
          

       image_size=224
       #img = cv2.imread(path1+"//"+i)
       path="static/diseasedetect/"+"//"+str(filename)
       img = image.load_img(path, target_size=(image_size, image_size))
       x = image.img_to_array(img)
       print(type(x))
       img_4d=x.reshape(1,224,224,3)
     
       predictions = model.predict(img_4d)
       print(predictions)
       pred=np.argmax(predictions[0])
       print("===============================================")
       print(pred)
       print("===============================================")
       dict1 = {0:'glioma_tumor',1:'meningioma_tumor',2:'no_tumor',3:'pituitary_tumor'}
       op=dict1[pred]
       print(op)
      
       if op == "glioma_tumor":
            final_prediction = "glioma tumor"
       elif op == "meningioma_tumor":
            final_prediction = "meningioma tumor"
       elif op == "no_tumor":
            final_prediction = "no tumor"
       elif op == "pituitary_tumor":
            final_prediction = "pituitary tumor"
       else:
            final_prediction = "Unknown"
       
       message = "The brain tumor is classified as " + final_prediction
       
  
       con = dbConnection()
       cursor = con.cursor()
       sql1 = "UPDATE patientsrequest SET disease = %s WHERE Patient_name = %s  AND Patient_Emailid = %s ;"
       val1 = (message, name ,usermail)
       cursor.execute(sql1,val1)
       con.commit()
       
       # sendemailtouser(usermail,message)
       
       
       
       user_dict = {
            "message": message,
            "final_prediction": final_prediction,
            "Image_path": path
        }
       
       return jsonify(user_dict)
        

      
       print("===============================================")
    
    return render_template('checkdisease.html',data=data)



    


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        Email = request.form.get("email")
        Password = request.form.get("password1")
        print(Password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM doctordetails WHERE email = %s AND password = %s', (Email, Password))
        print(result_count)
        
        if result_count == 1:
            res = cursor.fetchone()
            print(res)
            session['user'] = res[1]
            session['uid'] = res[0]
            session['image'] = res[6]
            # Successful login logic
            # return jsonify({'message': 'Login successful', 'user_id': res[0]})
            return "success"
        else:
            # Failed login logic
            # return jsonify({'message': 'Login failed'})
            return "fail"

        con.close()
    


@app.route('/register',methods=['POST'])
def register():
    
    print("ouy")
    if request.method =='POST':
        print("in record")
        details = request.form
      
        Username = details['Username']
        email = details['Email']
        Mobile = details['phone'] 
        type1 = details['type'] 
        Password = details['password']
        uploadimg = request.files['file']
        
        
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM doctordetails WHERE email = %s', (email))
        res = cursor.fetchone()
      
        
        filename_secure = secure_filename(uploadimg.filename)
        uploadimg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
        filenamepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_secure)
        
        if not res:
            sql = "INSERT INTO doctordetails(username, email, phone, specialist, password, filename) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Username, email, Mobile, type1, Password,filenamepath)
            cursor.execute(sql, val)
            con.commit()
            message = "Registration USER successfully added by USER side. Username: " + Username
            return jsonify({'message': message})
            message = "Already available"
            
        else:
            message = "Registration USER not  added by USER side. Username: " + Username
            dbClose()
          
            return jsonify({'message': message})

####################################################################################################################





####################################################################################################################
                                             #userside
####################################################################################################################
@app.route('/user')
def user():
    return render_template('user.html') 

@app.route('/homeusers')
def homeusers():
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM doctordetails')
    result = cursor.fetchall()
    print(result)
    
    return render_template('homeusers.html',result2=result) 

@app.route('/patientresult')
def patientresult():
    userimage=session['image1']
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM patientsrequest WHERE userimage = %s ',(userimage))
    result = cursor.fetchall()
    print(result)
    return render_template('patientresult.html',result=result)



@app.route('/serviceusers')
def serviceusers():
    return render_template('serviceusers.html')

@app.route('/appointment')
def appointment():
    # user1=session['user1']
    # image1=session['image1']
    
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT username FROM doctordetails')
    result = cursor.fetchall()
    print(result)
    
    return render_template('appointment.html',result=result)


@app.route('/login1',methods=['POST','GET'])
def login1():
    if request.method == 'POST':
        Email = request.form.get("Email")
        Password = request.form.get("password1")
        print(Email)
        print(Password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userregisters WHERE Email = %s AND Password = %s', (Email, Password))
        print(result_count)
        
        if result_count == 1:
            res = cursor.fetchone()
            print(res)
            session['user1'] = res[1]
            session['uidmail'] = res[2]
            session['image1'] = res[5]
            # Successful login logic
            # return jsonify({'message': 'Login successful', 'user_id': res[0]})
            return "success"
        else:
            # Failed login logic
            # return jsonify({'message': 'Login failed'})
            return "fail"

        con.close()
    


@app.route('/register1',methods=['POST'])
def register1():
    
    print("ouy")
    if request.method =='POST':
        print("in record")
        details = request.form
      
        Username = details['Username']
        email = details['Email']
        Mobile = details['phone'] 
        Password = details['password']
        uploadimg = request.files['file']
        
        
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM userregisters WHERE Email = %s', (email))
        res = cursor.fetchone()
      
        
        filename_secure = secure_filename(uploadimg.filename)
        uploadimg.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename_secure))
        filenamepath = os.path.join(app.config['UPLOAD_FOLDER1'], filename_secure)
        
        if not res:
            sql = "INSERT INTO userregisters(Username, Email, Mobile, Password, Profile_Img) VALUES (%s, %s, %s, %s, %s)"
            val = (Username, email, Mobile, Password, filenamepath)
            cursor.execute(sql, val)
            con.commit()
    
            message = "Registration USER successfully added by USER side. Username: " + Username
            # return redirect(url_for('index'))
            return jsonify({'message': message})
            message = "Already available"
            
        else:
            message = "Registration USER not  added by USER side. Username: " + Username
            dbClose()
            # return redirect(url_for('index'))
            return jsonify({'message': message})



@app.route('/request1',methods=['POST','GET'])
def request1():
    print("request1")
    if request.method =='POST':
        print("in record")
        details = request.form
        Username = details['name']
        email = details['email']
        date = details['date'] 
        doctorname = details['doctorname'] 
        message = details['message']
        symptoms =details.getlist('symptoms[]')
        uploadimg = request.files['file']
        print("Username",Username)
        print("symptoms",symptoms)
        print("doctorname",doctorname)
        image1=session['image1']
        print(image1)
        
        # Convert the list to a string, separated by commas or another delimiter
        symptoms_str = ','.join(symptoms)
        
        # return jsonify({'message': "hhhhhhhhhhhhhhhhhhhhhhhhhh"})
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM patientsrequest WHERE Patient_Emailid = %s', (email))
        res = cursor.fetchone()
      
        filename_secure = secure_filename(uploadimg.filename)
        uploadimg.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename_secure))
        filenamepath = os.path.join(app.config['UPLOAD_FOLDER2'], filename_secure)
        
        if not res:
            sql = "INSERT INTO patientsrequest(Patient_name, Patient_Emailid, Date, Doctorname, BrainTumorimage, massage,symptoms,userimage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (Username, email, date, doctorname, filenamepath,message,symptoms_str,image1)
            cursor.execute(sql, val)
            con.commit()
            message = "your request was successfully delivered to the doctor. Username: " + Username
            return jsonify({'message': message})
            message = "Already available"
            
        else:
            message = "Already available. Username: " + Username
            dbClose()
          
            return jsonify({'message': message})
####################################################################################################################

 
if __name__ == "__main__":
    # app.run(debug=True)
    app.run("0.0.0.0")