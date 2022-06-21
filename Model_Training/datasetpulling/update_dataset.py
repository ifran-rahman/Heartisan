import pyrebase
import pandas as pd

firebaseConfig = {
    'apiKey': "AIzaSyDyBOw4iG5FGfbor2YqDOF9QkX5Mv9XEmA",
    'authDomain': "ecg-nodemcu.firebaseapp.com",
    'databaseURL': "https://ecg-nodemcu-default-rtdb.firebaseio.com",
    'projectId': "ecg-nodemcu",
    'storageBucket': "ecg-nodemcu.appspot.com",
    'messagingSenderId': "45897358746",
    'appId': "1:45897358746:web:7ea053cf5b6bd22993ee23",
    'measurementId': "G-74D3MKZXL3"
  };

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()


def get_dataset():
  # import data from old dataset
  dataset = pd.read_csv('datasetpulling/mitbih_train.csv')

  # import reports from firebase
  reports = database.child("Dataset").get().val()

  for i in reports:
      # append beats which are already verifed, to the new dataset
      if reports[i]['verified'] == 'True':
          # make a row of data
          beat = []
          # get ecg data and insert in row list
          beat = reports[i]['ecg']
          heart_condition = reports[i]['heart_condition'][0]
          # append heart condition to the row
          beat.append(heart_condition)

          print('beat', beat)
          dataset.loc[len(dataset)] = beat

  return dataset
