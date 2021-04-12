from django.shortcuts import render
import pyrebase


config = {
    'apiKey': "AIzaSyBmbA3rMRI5nol0vIyMsDeDSNTCFoOWrwk",
    'authDomain': "test1-80f19.firebaseapp.com",
    'databaseURL': "https://test1-80f19-default-rtdb.firebaseio.com",
    'projectId': "test1-80f19",
    'storageBucket': "test1-80f19.appspot.com",
    'messagingSenderId': "825466536050",
    'appId': "1:825466536050:web:ca8cdf627c31f265eb02eb",
    'measurementId': "G-3252KZVCX3"
  };
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

def signIn(request):
    dict = { 'title':'Login'}
    return render(request,"Login.html",context=dict)
def home(request):
    dict = { 'title':'Home'}
    return render(request,"Home.html",context=dict)

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)

    elapsedtime = database.child("ECG1").child("Elapsed time").get().val()
    abdomenlist = database.child("ECG1").child("Abdomen_1").get().val()
    #elapsedti1=elapsedtime.val()
    #abdomenli=abdomenlist.val()


    return render(request,"Home.html",{"email":email,'elapsedtime':elapsedtime,'abdomenlist':abdomenlist})
    #data=database.child("ECG1")

    #values={'data':data}
    #return render(request,"graph.html",values)

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")

def signup(request):
    dict={'title':'Signup'}
    return render(request,"Registration.html",context=dict)
def signUp(request):
    dict = { 'title':'Signup'}
    return render(request,"Registration.html",context=dict)

def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html")
     return render(request,"Login.html")

def reset(request):
    dict={'title':'Reset Page'}
    return render(request,"Reset.html",context=dict)


def postReset(request):
	email = request.POST.get('email')
	try:
		authe.send_password_reset_email(email)
		message = "A email to reset password is succesfully sent"
		return render(request, "Reset.html", {"msg":message})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "Reset.html", {"msg":message})


def line_graph(request):
    elapsedtime = database.child("ECG1").child("Elapsed time").get().val()
    abdomenlist = database.child("ECG1").child("Abdomen_1").get().val()

    # data = runner.objects.all()
    values = {
        'elapsedtime': elapsedtime,
        'abdomenlist': abdomenlist,
    }

    return render(request, "graph.html", values)
    # return render(request,"graph.html",{'elapsedtime':elapsedtime,'abdomenlist':abdomenlist})
