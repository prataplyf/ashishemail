from flask import Flask, render_template, request, url_for
import smtplib # for send message to mail
from random import randint # to generate random number
import re # for email validation
import pymongo # for connect with database
from pymongo import MongoClient



myclient = MongoClient("mongodb+srv://prataplyf:ashish1234@mongoheroku-rwgat.mongodb.net/test?retryWrites=true&w=majority")

mydb = myclient.test
mycol = mydb["emails"]


app = Flask(__name__)

#otp = -1
# email = ''
randotp = randint(1000, 9999)   # Random 4 digit OTP Generator
otp = randotp

@app.route('/')
def home():
    return render_template('home.html')
 
@app.route('/verify',methods = ['POST', 'GET'])
def result():
    global email, otp
    if request.method == 'POST':
        verify = request.form
        email = request.form.get('email')
        #otp = request.form.get('otp')
        # if email in [temp['email'] for temp in mycol.find({}, {"_id":0, "email":1})]:
        #     global msg  # alreay verified message
        #     msg = "Email Already Verified"
        #     return render_template('status.html', result = email, message=msg)
        # else:
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("vacancykey123@gmail.com", "@vacancyKey1")                
        otpmessage = "Your OTP " + str(otp)
        s.sendmail("vacancykey123@gmail.com", email, otpmessage)
        print("sent mail")
            
        #mycol.insert_one({ "email": email})
        print("email entered!")
        s.quit()
        return render_template('verify.html', result = verify )
   

@app.route('/status', methods = ['POST','GET'])
def status():
    if request.method == 'POST':
        sentotp = int(request.form.get('otp'))
        semail = email
        if sentotp == otp:
            mycol.insert_one({ "email": email})
            msg = "Email Verified"
            return render_template('status.html', email= semail, message = msg)
        else:
            msg = "Wrong OTP, Please check again!"
            return render_template("status.html", message = msg)


if __name__ == '__main__':
   app.run(debug = True)