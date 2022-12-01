# Heartisan: An Incremental Learning Based Arrhythmia Detection, Data Collection, and Monitoring System.

an ECG monitoring, data collection and annotation tool with an integrated incremental learning-based model upgradation system. <br />
## **Abstract**<br />
Cardiac disease is the leading cause of death worldwide, which is why the importance of early heart disease prediction is rising daily. Patient data from modern ECG systems can be utilized to improve such machine-learning models. Here, a system has been proposed that aids in early arrhythmia prediction using a convolutional neural network and continuously improves the model using incremental learning utilizing patient data from a web application. The web app comes with a patient and a doctor’s portal. Patients can view heart conditions and send ECG beats and predictions for verification. Whereas the doctor’s portal is used to annotate the model’s falsely predicted heartbeats. The system continuously updates the model using newly annotated data following an incremental learning approach.The proposed incremental learning strategy was simulated using the MIT BIH dataset, and the approach  demonstrated a promising result as the overall accuracy and AUC improved as well as the F1 score of individual classes showed a notable shift. The system is expected to contribute to building a novel large arrhythmia dataset in an efficient strategy, as well as provide patients with a heart condition monitoring system employing a highly accurate arrhythmia classifier in the long run. 

## **Features**<br />
In this work, it was hypothesized that with the help of incremental learning, an ECG monitoring system could be used to efficiently create a generalized arrhythmia detection dataset and continually update an arrhythmia detection model via new patient data. Therefore a novel system was proposed that works as an ECG monitoring, data collection and annotation tool with an integrated incremental learning-based model upgradation system. Patients can view ECG signals and arrhythmia prediction; they can send reports, which consist of their processed and extracted ECG heartbeats labeled by a CNN-based arrhythmia prediction model. Using the doctor’s portal, a professional doctor or expert must analyze the reports to re-annotate the falsely annotated heartbeats. The system then uses scheduled incremental learning to train the pre-trained model using old and new data to upgrade it to a better version.
The key features of our work are listed as follows, 
1. The proposed ECG monitoring web app is equipped with a patient’s portal, a doctor’s portal, and a convolutional neural network so patients can get early arrhythmia prediction and send their diagnosed reports (processed heartbeats labeled by the model) for further analysis. The doctor's portal of the web app allows professionals to label falsely annotated reports conveniently. 
2. The system can collect the verified heartbeats from the web app to create a new balanced, generalized dataset and train the pre-trained model using old and new data following incremental learning methods on a scheduled basis. 
3. We simulated the proposed incremental learning method using the MIT BIH dataset. The dataset was divided into two portions, assuming the first as the primary and the rest as a newly collected dataset. The model's overall accuracy improved, particularly the F1 score on classes with fewer signals showed a noticeable advancement (4% and 8%). The primary model could correctly annotate more than 98% of the new dataset. During training, the new model converged in only half of the epochs as the primary model.

## **System**<br />
The system is built using Django and Firebase is used as the database.

<img alt="Alt text" src="/images/system_diagram.png">

## **Database**<br />
Firebase Realtime Database is used to store data. Firebase In the ”Realtime Database”, we can store data in JSON format. The structure of our database is illustrated in figure 4. 
<img alt="Alt text" src="/images/Database.jpg">

## **Data Process**<br />
The arrhythmia classification model classifies arrhythmia from heartbeat. It is necessary to extract beats from ECG signals. For inferences, beats get extracted from ECG signals. 
                                                
<img alt="Alt text" src="/images/dp_fullsignal.png">
<img alt="Alt text" src="/images/dp_heartbeatsignal.png">

## **Application**
<img title="Patient's portal" alt="Alt text" src="/images/patients-portal-dashboard.png">
<img title="ECG Signal visualization page" alt="Alt text" src="/images/patients-portal-viewsignal.png">
<img title="Doctor's portal" alt="Alt text" src="/images/doctors-portal-dashboard.png">
<img title="Report visualization page" alt="Alt text" src="/images/doctors-portal-viewsignal.png">

## **How to run?**<br />
* git clone https://github.com/ifran-rahman/ECG_Monitoring_System.git  # clone
* Change the firebase config in view.py # can be found on firebase console's web app settings
<img alt="Alt text" src="/images/firebaseconfig.png">

* pip install -r requirements.txt  # install
* cd Demo
* py manage.py runserver # start server
* Create a doctor's account manually from firebase 
* Create an account in the database according to the image below and replace the UID
<img alt="Alt text" src="/images/doctors-auth.png">

* Create a patient's account from the website
* Push data to the patient's node.

Alternatively for testing purpose, edit the given sample database "db_json.json" and import in firebase-realtime database.
* Create a sample doctor account in firebase.
* Replace the doctor's UID in the db_json.json file.
* Create a sample patient account in firebase.
* Replace the patient's UID in the db_json.json file.
* Import the file in firebase-realtime database

To push data from hardware,
* Use user credentials to get access
* Push data in list format. There should be two lists. One consists of ECG values, another consists of seconds where each second presents an ECG value <br/>
ecg = [0.7732789441406522, 0.6836692935784979, 0.5320130856048167, 0.3407086606118426] <br/>
timeframe = [0, 0.001, 0.002,0.003, 0.004]

**Contributors**

[![](https://github.com/Anan-Ghosh.png?size=50)](https://github.com/Anan-Ghosh)
[![](https://github.com/Spectre118.png?size=50)](https://github.com/Spectre118)
[![](https://github.com/ifran-rahman.png?size=50)](https://github.com/ifran-rahman)
[![](https://github.com/yearat.png?size=50)](https://github.com/yearat) 
