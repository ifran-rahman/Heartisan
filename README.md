# Heartisan: ECG Data Monitoring and Arrhythmia Prediction Through Continuous Learning from Patient Data.

An end to end system to monitor individual patient's ECG results and predict Arrhythmia through continuous learning from patient data

**Abstract**<br />
Remote health monitoring system is one of the most crucial medical innovations. Especially the importance of such systems was seen during the covid pandemic. With cardiac disease being the leading cause of death worldwide, the importance of remote ECG monitoring and early heart disease prediction systems is rising day by day. Here, a web based system is proposed that could enable real-time monitoring of individuals with chronic conditions as well as aid in early arrhythmia prediction using machine learning methods. A portable ECG machine can be easily connected to the user-friendly web based application. The app allows patients to effortlessly record, store, and monitor ECG graphs as well as obtain arrhythmia predictions. It comes with a custom graph viewing mode. Patients can share their data with any doctor, any time. This will cut down on the distance between patients and doctors significantly. Additionally, it provides a semi-supervised system for doctor verified arrhythmia data collection and autonomous model upgradation. The system is hoped to bring cardiac patients and doctors closer as well as support patients with an advanced AI system for early disease prediction. It is also expected that such a system will contribute in building novel arrhythmia datasets for researchers. 

**Features**<br />
A solution such as this, will reduce the distance between patients and doctors and offers an automated data collection and model upgradation process. The user-friendly web application can be easily connected to a portable ECG machine. Patients can comfortably record, store, and monitor ECG graphs as well as get arrhythmia predictions using the application. They can view full signal or crop and view based on a timeframe. Signals get stored based on dates. Existing portable systems that can predict arrhythmia tend to be expensive. In contrast, this application is a low-cost solution. Using the patient's email and an access key, they can immediately share their data with their doctor. Being a web application makes it highly accessible. Users can access their data using a web browser anytime from anywhere on earth. Moreover, as it is a very open and straightforward solution, patients can share their data with any doctor they want. Thus, a doctor can easily view a patient's heart condition and history. This will significantly reduce the distance between patients and doctors. In addition to the monitoring service, the application offers an automated data collection and model upgradation system. Patients can diagnose and push their ECG reports for verification. Assigned cardiac doctors can log in to a separate "doctor's portal" and verify all the pushed ECG heartbeats. Once a week, the standard dataset automatically merges with the new doctor-verified dataset, and the model gets trained. If the result improves, the model gets replaced. This way, the system can help build a novel ECG dataset and update its arrhythmia classification model continuously.

**System**<br />
The system is built using Django and Firebase is used as the database.

<img alt="Alt text" src="/images/system_diagram.png">

**Data Base**<br />
Firebase Realtime Database is used to store data. Firebase In the ”Realtime Database”, we can store data in JSON format. The structure of our database is illustrated in figure 4. 
<img alt="Alt text" src="/images/Database.jpg">

**Data Process**<br />
The arrhythmia classification model classifies arrhythmia from heartbeat. It is necessary to extract beats from ECG signals. For inferences, beats get extracted from ECG signals. 
                                                
<img alt="Alt text" src="/images/dp_fullsignal.png">
<img alt="Alt text" src="/images/dp_heartbeatsignal.png">

**Application**
<img title="Patient's portal" alt="Alt text" src="/images/patients-portal-dashboard.png">
<img title="ECG Signal visualization page" alt="Alt text" src="/images/patients-portal-viewsignal.png">
<img title="Doctor's portal" alt="Alt text" src="/images/doctors-portal-dashboard.png">
<img title="Report visualization page" alt="Alt text" src="/images/doctors-portal-viewsignal.png">

**How to run?**<br />
* git clone https://github.com/ifran-rahman/ECG_Monitoring_System.git  # clone
* cd Demo
* pip install -r requirements.txt  # instal
* py manage.py runserver # start server

**Contributors**

[![](https://github.com/Anan-Ghosh.png?size=50)](https://github.com/Anan-Ghosh)
[![](https://github.com/Spectre118.png?size=50)](https://github.com/Spectre118)
[![](https://github.com/ifran-rahman.png?size=50)](https://github.com/ifran-rahman)
[![](https://github.com/yearat.png?size=50)](https://github.com/yearat) 
