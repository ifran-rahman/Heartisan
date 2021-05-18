from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpRequest, request,QueryDict
import pyrebase

config = {
    "apiKey": "AIzaSyCNgewbNVZWe0Ex2H0oJVuSMgiV8PAfqvc",
    "authDomain": "test-92aa6.firebaseapp.com",
    "databaseURL": "https://test-92aa6-default-rtdb.firebaseio.com",
    "projectId": "test-92aa6",
    "storageBucket": "test-92aa6.appspot.com",
    "messagingSenderId": "1020580899643",
    "appId": "1:1020580899643:web:a859ce9cabbb673e50e51e",
    "measurementId": "G-DX88ST3VWX"
};
# Initialising database,auth and firebase for further use
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

uid=''
session_id=''
def signIn(request):
    dict = {'title': 'Login'}
    return render(request, "Login.html", context=dict)


def home(request):
    # uid=request.get(request.session['uid'])
    # session_id = user['idToken']
    # request.session['uid'] = str(session_id)

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']

    a = a[0]
    a = a['localId']
    print(a)
    userinfo = database.child(a).child("userinfo").get()

    for info in userinfo:
         infokey = info.key()

    name = database.child(a).child('userinfo').child(infokey).child('name').get().val()
    age = database.child(a).child('userinfo').child(infokey).child('age').get().val()
    gender = database.child(a).child('userinfo').child(infokey).child('Gender').get().val()
    bloodgroup = database.child(a).child('userinfo').child(infokey).child('Bloodgroup').get().val()

    ecgdates = []
    dict={}
    #Print dates of ECG tests
    allecgdatas = database.child(a).child('ecgdatas').get()


    for data in allecgdatas:
        ecgdates.append(data.key())

    print(ecgdates)
    dict= {'name':name, 'age':age, 'gender':gender, 'bloodgroup':bloodgroup}
    return render(request, "Home.html",{'title':'Home','dict':dict, 'ecgdates':ecgdates})


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

    userinfo = database.child(uid).child("userinfo").get()

    for info in userinfo:
        infokey = info.key()

    name = database.child(uid).child('userinfo').child(infokey).child('name').get().val()
    age = database.child(uid).child('userinfo').child(infokey).child('age').get().val()
    gender = database.child(uid).child('userinfo').child(infokey).child('Gender').get().val()
    bloodgroup = database.child(uid).child('userinfo').child(infokey).child('Bloodgroup').get().val()


    dict={'name':name, 'age':age, 'gender':gender, 'bloodgroup':bloodgroup}

    ecgdates = []
    #Print dates of ECG tests
    allecgdatas = database.child(uid).child('ecgdatas').get()



    for data in allecgdatas:
        ecgdates.append(data.key())

    # currentuser = authe.getInstance().getCurrentUser().getUid()
    # data=database.child(uid).child('userinfo').child(infokey).get().val()
    elapsedtime = database.child("ECG1").child("Elapsed time").get().val()
    abdomenlist = database.child("ECG1").child("Abdomen_1").get().val()
    # elapsedti1=elapsedtime.val()
    # abdomenli=abdomenlist.val()

    return render(request, "Home.html", {'title':'Login', "email": email, 'elapsedtime': elapsedtime, 'abdomenlist': abdomenlist, 'dict':dict, 'ecgdates':ecgdates})
    # data=database.child("ECG1")


def logout(request):
    try:
        auth.logout(request)
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
     data = {'name': name,'age': age, 'Gender': gender, 'Bloodgroup': bloodgroup}
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

datee=''
def line_graph(request):
    global datee
    datee=request.GET.get('date')
    print("This is date")
    print(datee)
    # datee="25 April 2021"
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']

    a = a[0]
    a = a['localId']
    print(a)
    timestamps = database.child(a).child("ecgdatas").get()
    print(timestamps)

    ecgdatas = database.child(a).child("ecgdatas").child(datee).get()
    print(ecgdatas)

    for data in ecgdatas:
        ecg = database.child(a).child("ecgdatas").child(str(datee)).child(data.key()).child("Abdomen").get().val()
        time = database.child(a).child("ecgdatas").child(str(datee)).child(data.key()).child("Time").get().val()
    values = {
        'elapsedtime': time,
        'abdomenlist': ecg,
        'title': 'Graph',
        'datee':datee,

    }

    return render(request, "graph.html", values)






def postgraph(request):
    start=request.POST.get('start')
    end=request.POST.get('end')

    global datee

    # date='25 April 2021'
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']

    a = a[0]
    a = a['localId']
    print(a)

    ecgdatas = database.child(a).child("ecgdatas").child(str(datee)).get()

    for data in ecgdatas:
        ecg = database.child(a).child("ecgdatas").child(str(datee)).child(data.key()).child("Abdomen").get().val()
        time = database.child(a).child("ecgdatas").child(str(datee)).child(data.key()).child("Time").get().val()
    start=getIndex(start, time)
    end=getIndex(end, time)

    if start < end and start > 0:
        message="Here is your requested duration."
    else:
        message="Invalid Time Duration." 
    values = {
        'message':message,
        'elapsedtime': time[start:end],
        'abdomenlist': ecg[start:end],
        'datee':datee,
        'title': 'Graph',
    }

    return render(request, "graph.html", values)


def getIndex(enteredtime, dataset):
    list = [count + 1 for count, ele in enumerate(dataset) if ele <= float(enteredtime)]
    x = 0
    for data in list:
        x = data
    return x
