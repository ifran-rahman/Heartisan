from django.shortcuts import redirect, render
from django.contrib import auth
from django.http import HttpResponse, HttpRequest, request,QueryDict
from matplotlib.pyplot import title
import pyrebase
from dataProcessor import beatcutting, getIndex
# from tensorflow.keras.models import Model
# from tensorflow.keras.models import load_model
import h5py
import pandas as pd
import numpy as np
import random

# Firebaseconfig
config = {
    'apiKey': " ",
    'authDomain': " ",
    'databaseURL': " ",
    'projectId': " ",
    'storageBucket': " ",
    'messagingSenderId': " ",
    'appId': " ",
    'measurementId': " "
};

# Initialising database,auth and firebase for further use
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

uid=''
session_id=''
def doctors_signIn(request):
    title="Log in for Doctor"
    dict = {'title': title}
    return render(request, "doctors_login.html", context=dict)


def patient_signIn(request):
    title="Log in for Patient"
    dict = {'title': title}
    return render(request, "Login2.html", context=dict)



def signIn2(request):
    dict = {'title': title}
    return render(request, "Login.html", context=dict)



# get userdata in a dictionary given UID
def getUserData(UID):
    userinfo = database.child(UID).child("userinfo").get().val()

    for info in userinfo:
            infokey = info

    name = database.child(UID).child('userinfo').child(infokey).child('name').get().val()
    age = database.child(UID).child('userinfo').child(infokey).child('age').get().val()
    gender = database.child(UID).child('userinfo').child(infokey).child('Gender').get().val()
    bloodgroup = database.child(UID).child('userinfo').child(infokey).child('Bloodgroup').get().val()
    try:
        last_condition = database.child(UID).child('userinfo').child(infokey).child('last_condition').get().val()
    except:
        print("No prediction yet")
    if gender == 'male':
        image = 'https://firebasestorage.googleapis.com/v0/b/ecg-nodemcu.appspot.com/o/malepatient.png?alt=media&token=9eec4c25-76b1-40db-993c-fac68acb6d37'
    else:
        image = 'https://firebasestorage.googleapis.com/v0/b/ecg-nodemcu.appspot.com/o/femalepatient.png?alt=media&token=93c4d19a-2d72-4dee-b2d4-3e2a08346553'
    userData = {'name': name, 'age': age, 'gender': gender, 'bloodgroup': bloodgroup, 'image':image, 'last_condition':last_condition}
    return userData

def home(request):

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print(a)
    userinfo = database.child(a).child("userinfo").get()

    for info in userinfo:
         infokey = info.key()

    ecgdates = []
    #Print dates of ECG tests
    allecgdatas = database.child(a).child('ecgdatas').get()


    for data in allecgdatas:
        ecgdates.append(data.key())

    dict = getUserData(a)

    return render(request, "Home.html",{'title':'Home','dict':dict, 'ecgdates':ecgdates})

def getDoctorsData(UID):
    a = UID
    userinfo = database.child(UID).child("userinfo").get().val()

    userinfo = database.child('doctors').child(a).child("userinfo").get().val()
    print(userinfo)
    for info in userinfo:
         infokey = info

    name = database.child('doctors').child(a).child('userinfo').child(infokey).child('name').get().val()
    age = database.child('doctors').child(a).child('userinfo').child(infokey).child('age').get().val()
    gender = database.child('doctors').child(a).child('userinfo').child(infokey).child('Gender').get().val()
    bloodgroup = database.child('doctors').child(a).child('userinfo').child(infokey).child('Bloodgroup').get().val()
    if gender == 'male':
        image = 'https://firebasestorage.googleapis.com/v0/b/ecg-nodemcu.appspot.com/o/maledoctor.png?alt=media&token=2bf6a99f-0da1-47ac-a6da-b27fc57845e0'
    else:
        image = 'https://firebasestorage.googleapis.com/v0/b/ecg-nodemcu.appspot.com/o/femaledoctor.png?alt=media&token=b30eae9b-447e-41bc-83f2-cc2fe0d01999'
    doctorsdata = {'name': name, 'age': age, 'gender': gender, 'bloodgroup': bloodgroup, 'image': image}

    return doctorsdata

def DoctorsHome(request):

    idtoken= request.session['uid']
    # print("IDTOKEN:",idtoken)
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    # print(a)

    reports = database.child('Dataset').get().val()

    report_dict = {}
    
    for data in reports:
        verification = database.child('Dataset').child(str(data)).child('verified').get().val()
        report_dict[data] = verification
        # print(verification)

    dict= getDoctorsData(a) 
    return render(request, "doctors_home.html",{'title':'Home','dict':dict,'reports':report_dict})

def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')

    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, pasw)

    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        return render(request, "Login.html", {"message": message})

    uid=user['localId']
    session_id = user['idToken']

    request.session['uid'] = str(session_id)

    dict = getUserData(uid)

    ecgdates = []
    #Print dates of ECG tests
    allecgdatas = database.child(uid).child('ecgdatas').get()



    for data in allecgdatas:
        ecgdates.append(data.key())


    elapsedtime = database.child("ECG1").child("Elapsed time").get().val()
    ecglist = database.child("ECG1").child("Abdomen_1").get().val()
 

    return render(request, "Home.html", {'title':'Login', "email": email, 'elapsedtime': elapsedtime, 'ecglist': ecglist, 'dict':dict, 'ecgdates':ecgdates})

def DoctorsPostSignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')

    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, pasw)

    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        return render(request, "Login.html", {"message": message})

    uid=user['localId']
    session_id = user['idToken']

    request.session['uid'] = str(session_id)


    dict = getDoctorsData(uid)

    reports = database.child('Dataset').get().val()

    report_dict = {}
    verified_reports = {}
    for data in reports:
        verification = database.child('Dataset').child(str(data)).child('verified').get().val()
        if verification == 'True':
            report_dict[data] = verification
        else:
            verified_reports[data] = verification
        reports_length = {'len':len(report_dict)}
    return render(request, "doctors_home.html", {'title':'Login', "email": email, 'dict':dict, 'reports':report_dict, 'verified_reports':verified_reports, 'reports_length':reports_length})

def logout(request):
    try:
        auth.logout(request)
        return redirect('signIn')
    except:
        pass
    return render(request, "Login.html",{"tilte":"Login"})


def signup(request):
    dict = {'title': 'Signup'}
    return render(request, "Registration.html", context=dict)


def signUp(request):
    dict = {'title': 'Signup'}
    return render(request, "Registration.html", context=dict)

def postsignUp(request):
     name = request.POST.get('name')
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     paswrepeat=request.POST.get("pass-repeat")
     age = request.POST.get('age')
     gender = request.POST.get('gender')
     bloodgroup = request.POST.get('bloodgroup')
     uid=''
     if passs==paswrepeat:
         try:
             # creating a user with the given email and password
             user = authe.create_user_with_email_and_password(email, passs)
             uid = user['localId']
             idtoken = request.session['uid']

         except:
             print(uid)
     data = {'name': name,'age': age, 'Gender': gender, 'bloodgroup': bloodgroup}
     database.child(uid).child("userinfo").push(data)
     return render(request, "Login.html")



def reset(request):
    dict = {'title': 'Reset Page'}
    return render(request, "Reset.html", context=dict)


def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is succesfully sent"
        return render(request, "Reset.html", {"msg": message})
    except:
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "Reset.html", {"msg": message})
def getReport(id):
    report = database.child('Dataset').get().val()
    return report

report=''
def doctors_graph(request):
    global report
    report = str(request.GET.get('report'))
    # print("This is id: ", report)
    # ecg = database.child('Dataset').get().val()

    ecg = database.child('Dataset').child(report).child('ecg').get().val()

    heart_condition = database.child('Dataset').child(report).child('heart_condition').get().val()

    indices = [*range(0, 187, 1)]

    heart_conditions = ['Everything Seems Normal!','Supraventricular ectopic beat detected.','Ventricular ectopic beat detected.',
    'Fusion beat detected.','Unknown beat detected.']

    if (heart_condition[0] == 0):
        heart_condition = "Heart Condition: Everything Seems Normal!"
    elif (heart_condition[0] == 1):
        heart_condition = "Heart Condition: Supraventricular ectopic beat detected."
    elif (heart_condition[0] == 2):
        heart_condition = "Heart Condition: Ventricular ectopic beat detected."
    elif (heart_condition[0] == 3):
        heart_condition = "Heart Condition: Fusion beat detected."
    else:
        heart_condition = "Heart Condition: Unknown beat detected."

    values = {
            'elapsedtime': indices,
            'ecglist': ecg,
            'title': 'Graph',
            'date':report,
            'heart_condition':heart_condition,
            'heart_conditions':heart_conditions
        }

    return render(request, "doctor_graph.html", values)

def verify_prediction(request):
    validate = str(request.GET.get('validate'))

    if (validate == "Everything Seems Normal!"):
        heart_condition = 0
    elif (validate == "Supraventricular ectopic beat detected."):
        heart_condition = 1
    elif (validate == "Ventricular ectopic beat detected."):
        heart_condition = 2
    elif (validate == "Fusion beat detected."):
        heart_condition = 3
    else:
        heart_condition = 4

    # val = []
    # val = val.append(heart_condition)
    database.child('Dataset').child(report).child('heart_condition').set([heart_condition])
    database.child('Dataset').child(report).child('verified').set('True')

    return redirect('DoctorsHome')


date=''
def line_graph(request):
    global date
    date=request.GET.get('date')
    # print("This is date")
    # print(date)
    # date="25 April 2021"
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']    #What is a?

    a = a[0]          #What is a[0]???
    a = a['localId']  #a is to be changed to "UID"
    # print(a)

    ecgdatas = database.child(a).child("ecgdatas").child(date).get()
    # print(ecgdatas)

    for data in ecgdatas:
        ecg = database.child(a).child("ecgdatas").child(str(date)).child(data.key()).child("Abdomen").get().val()
        time = database.child(a).child("ecgdatas").child(str(date)).child(data.key()).child("Time").get().val()

    values = {
            'elapsedtime': time,
            'ecglist': ecg,
            'title': 'Graph',
            'date':date
        }

    return render(request, "graph.html", values)


def postgraph(request):
    start=request.POST.get('start')
    end=request.POST.get('end')

    global date

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']

    a = a[0]
    a = a['localId']

    ecgdatas = database.child(a).child("ecgdatas").child(str(date)).get()

    for data in ecgdatas:
        ecg = database.child(a).child("ecgdatas").child(str(date)).child(data.key()).child("Abdomen").get().val()
        time = database.child(a).child("ecgdatas").child(str(date)).child(data.key()).child("Time").get().val()
    start=getIndex(start, time)
    end=getIndex(end, time)

    if start < end and start > 0:
        message="Here is your requested duration."
    else:
        message="Invalid Time Duration."

    values = {
        'message':message,
        'elapsedtime': time[start:end],
        'ecglist': ecg[start:end],
        'date':date,
        'title': 'Graph',}


    return render(request, "graph.html", values)

# Python code to generate
# random indeces given a list's length
def getBeatIndices(beats_list_len):
    # Function to generate
    # and append them
    # start = starting range,
    # end = ending range
    # num = number of
    # elements needs to be appended
    def Rand(start, end, num):
        res = []
        for j in range(num):
            num = random.randint(start, end)

            # if a number already exists in the result list, choose a new number
            while(num in res):
                num = random.randint(start, end)
            res.append(num)

        return res

    # choose radnomly 5 numbers. num must be smaller than beat_len
    num = 5
    if (num > beats_list_len):
        raise Exception("Beats list's length must be greater than number of chosen beats")

    start = 1
    end = beats_list_len - 1

    return Rand(start, end, num)

# classify and return prediction of a heart beat
def getPrediction(beat_t):
    model = load_model('E:/CSE (299)-Junior Design/ECG/django-firebaseauth/Demo/SimpleArrythmiaClassffier.h5')
    predictions = model.predict(beat_t)
    rounded_predictions = np.argmax(predictions, axis= 1)
    return rounded_predictions

global reports 
reports = []

def prediction_graph(request):
    global date

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']

    a = a[0]
    a = a['localId']

    ecgdatas = database.child(a).child("ecgdatas").child(date).get()

    for data in ecgdatas:
        ecg = database.child(a).child("ecgdatas").child(str(date)).child(data.key()).child("Abdomen").get().val()
        time = database.child(a).child("ecgdatas").child(str(date)).child(data.key()).child("Time").get().val()

    beats=beatcutting(ecg)

    # Generate random beat indices
    beats_len = len(beats)
    beat_indices = getBeatIndices(beats_len)

    # generate 5 reports randomly and store them in reports list. 
    # if user wishes to validate push the whole list to dataset database otherwise use it only to show 
    # classification results

    # gather the user's data
    userdata = getUserData(a)
    age = userdata['age']
    sex = userdata['gender']

    for i in beat_indices:
        beat_t = beats[i]
        beat_t = beat_t.tolist()
        heart_condition = getPrediction(beat_t)
        report_dict = {'age': age, 'sex': sex, 'ecg': beat_t , 'heart_condition': heart_condition, 'verified': 'False'}
        reports.append(report_dict)
        

    # # Take the 2nd beat to diagnose
    # beats1=beats[1].tolist()
    # beats[1]= pd.DataFrame(beats[1])
    # beat_t = pd.DataFrame(beats[1]).transpose().to_numpy()
    # print(beats[1].shape)
    # rounded_predictions = getPrediction(beat_t)
    # print(rounded_predictions)
    rounded_predictions = reports[1]['heart_condition']

    for i in rounded_predictions:
        rounded_predictions=i

    if (rounded_predictions == 0):
        predicted_result = "Heart Condition: Everything Seems Normal!"
    elif (rounded_predictions == 1):
        predicted_result = "Heart Condition: Supraventricular ectopic beat detected."
    elif (rounded_predictions == 2):
        predicted_result = "Heart Condition: Ventricular ectopic beat detected."
    elif (rounded_predictions == 3):
        predicted_result = "Heart Condition: Fusion beat detected."
    else:
        predicted_result = "Heart Condition: Unknown beat detected."

    values = {
            'elapsedtime': time,
            'ecglist': ecg,
            'title': 'Graph',
            'date': date,
            'predicted_result':predicted_result,
        }

    userinfo = database.child(a).child("userinfo").get().val()

    for info in userinfo:
            infokey = info

    database.child(a).child("userinfo").child(infokey).child('last_condition').set(predicted_result)  

    return render(request, "graph2.html", values)



# push a report to Dataset database
def PushReport(report_dict):
    print("Report dict", report_dict)
    database.child('Dataset').push(report_dict)


def validation(request):
    # when user press confirm button, we will push the data to database
    list(map(PushReport, reports))
    return render(request, "Home.html")


def doctor_portal(request):
    return render(request, "doctors_home.html")