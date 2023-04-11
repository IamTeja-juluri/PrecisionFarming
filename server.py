from flask import Flask, render_template, request, Markup
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
from Data.fertilizerDicUi import fertilizer_dic_ui
from Data.fertilizerDicMessage import fertilizer_dic_msg
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from twilio.rest import Client
import os
import datetime



# Create a new instance of the Chrome browser

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_experimental_option("prefs",{"download.default_directory":"C:\\Users\\Teja\\OneDrive\\Desktop\\Web Development\\Python Projects\\Farming"})

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

options.add_argument('--headless')
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "C:\\Users\\Teja\\OneDrive\\Desktop\\Web Development\\Python Projects\\Farming"}}
driver.execute("send_command", params)

username="cvr-heights-2022"
password="Cvrece123"
url="https://beta.thethingsmate.com/oauth/login"

year=datetime.date.today().year
month=datetime.date.today().month
day=datetime.date.today().day

if(month<10):
    month='0'+str(month)

if(day<10):
    day='0'+str(day)

filename="Soil_NPK_sensor_-1_"+str(year)+'_'+str(month)+'_'+str(day)+'.csv'

xg_model_path = 'models/XGBoost.pkl'
xg_model = pickle.load(
    open(xg_model_path, 'rb'))


dt_model_path= 'models/DecisionTree.pkl'
dt_model= pickle.load(
    open(dt_model_path, 'rb'))


lr_model_path = 'models/LogisticRegression.pkl'
lr_model= pickle.load(
    open(lr_model_path, 'rb'))


nb_model_path= 'models/NBClassifier.pkl'
nb_model= pickle.load(
    open(nb_model_path, 'rb'))


rf_model_path = 'models/RandomForest.pkl'
rf_model = pickle.load(
    open(rf_model_path, 'rb'))


svm_model_path = 'models/SVMClassifier.pkl'
svm_model = pickle.load(
    open(svm_model_path, 'rb'))


app = Flask(__name__)

crops=["apple","banana","blackgram","chickpea","coconut","coffee","cotton","grapes","jute","kidneybeans","lentil","maize","mango","mothbeans","mungbean","muskmelon","orange","papaya","pigeonpeas","pomegranate","rice","watermelon"]


def sendMsg(Message,contact,medium):
      
       account_sid ='AC843be320f9a1c6ecde0e97ca35f3821f'
       auth_token = '71ae86894ccf5781bed87c5a0b2da4c6'
       client = Client(account_sid,auth_token)
       print(Message) 
      
       if(medium=='Sms'):
          message=client.messages.create(body=Message,from_='+15074739185',to='+91'+contact) 
       else:
          message=client.messages.create(body=Message,from_='whatsapp:+14155238886',to='whatsapp:+91'+contact) 

                    

def fertilizer_prediction_result(rows,crop_name):
        
        N=int(rows[0][1])
        P=int(rows[0][2])
        K=int(rows[0][3])
        crop=str(crop_name)
        df=pd.read_csv('Data/fertilizer.csv')
        
        nval=df[df['Crop']==crop]['N'].iloc[0]
        pval=df[df['Crop']==crop]['P'].iloc[0]
        kval=df[df['Crop']==crop]['K'].iloc[0]

        n=nval-N
        p=pval-P
        k=kval-K

        temp={abs(n):"N",abs(p):"P",abs(k):"K"}
        max_value=temp[max(temp.keys())]
        if max_value == "N":
            if n<0:
                key="NHigh"
            else:
                key="NLow"
        elif max_value=="P":
            if p<0:
                key="PHigh"
            else:
                key="PLow"
        else:
            if k<0:
                key="KHigh" 
            else:
                key="KLow"

        print("fertilizer prediction method")
        
        return key


def processCsvFile(crop_name):

     # initializing the titles and rows list
    fields = []
    rows = []

    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        # extracting field names through first row
        fields = next(csvreader)
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

     # printing the field names
    print('Field names are:' + ', '.join(field for field in fields))


    n=rows[0][1]
    p=rows[0][2]
    k=rows[0][3]

    print(n,p,k)

    print("process csv method")

    return fertilizer_prediction_result(rows,crop_name)
   

def repeatTask(crop_name,contact,medium):

    #refresh button
    driver.find_element(By.XPATH,"//span[contains(text(),'Refresh')]").click()
    time.sleep(5)

    li = os.listdir('./') 

    for i in li:
        if(i.find("Soil")!=-1):
             os.remove(i)  

    #3dots
    driver.find_element(By.XPATH,"//*[@id='dashboard-container']/div/div/div[3]/div/div/div[1]/div[1]/a").click()
    time.sleep(3)

    #download npkTable
    driver.find_element(By.XPATH,"/html/body/div/div/div/ul/li[1]/a").click()
    time.sleep(8)

    print("repeat task method")

    key=processCsvFile(crop_name)
    sendMsg(fertilizer_dic_msg[key],contact,medium)

def automate_TTN():

    driver.maximize_window()

    # Navigate to the URL of the website
    driver.get(url)

    #Sending Keys
    driver.find_element(By.XPATH,"//input[contains(@id,'user_id')]").send_keys(username)
    driver.find_element(By.XPATH,"//input[contains(@id,'password')]").send_keys(password) 
    time.sleep(5)


    #clicks login
    driver.find_element(By.XPATH,"//span[contains(text(),'Login')]").click()
    time.sleep(5)

    
    #clicks console
    driver.find_element(By.XPATH,"//a[contains(@class,'_8TIz4+gU66 _1h5on2Eq5J')]").click()
    time.sleep(5)

    
    #clicks Application Server
    driver.find_element(By.XPATH,"//span[contains(text(),'Application Server')]").click()
    time.sleep(5)


def job(crop_name,contact,time_interval,medium):

    automate_TTN()

    #clicks cvr-smart-agriculture
    driver.find_element(By.XPATH,"//a[contains(text(),'CVR Smart Agriculture')]").click()
    time.sleep(5)

    #reload page
    driver.get("https://beta.thethingsmate.com/console/app/dashboards/576-cvr-smart-agriculture")
    time.sleep(5)

    print("job method")
    repeatTask(crop_name,contact,medium)
    schedule.every(int(time_interval)).seconds.do(repeatTask,crop_name=crop_name,contact=contact,medium=medium)

    while True:
        schedule.run_pending()
    
    driver.quit() 


def fetch_file_from_TTN():

    automate_TTN()

    #clicks cvr-smart-agriculture
    driver.find_element(By.XPATH,"//a[contains(text(),'CVR Smart Agriculture')]").click()
    time.sleep(5)

    #reload page
    driver.get("https://beta.thethingsmate.com/console/app/dashboards/576-cvr-smart-agriculture")
    time.sleep(5)

    #refresh button
    driver.find_element(By.XPATH,"//span[contains(text(),'Refresh')]").click()
    time.sleep(5)

    li = os.listdir('./') 

    for i in li:
        if(i.find("EC")!=-1):
             os.remove(i)  

    #3dots
    driver.find_element(By.XPATH,"//*[@id='dashboard-container']/div/div/div[1]/div/div/div[1]/div[1]/a").click()
    time.sleep(3)

    #download ec and water moisture Table
    driver.find_element(By.XPATH,"/html/body/div/div/div/ul/li[1]/a").click()
    time.sleep(8)

    # driver.quit()



def predict_time(area_in,flowrate):
 
   file_name="EC_SENSOR_2_"+str(year)+'_'+str(month)+'_'+str(day)+'.csv'
   with open("C:\\Users\\Teja\\OneDrive\\Desktop\\Web Development\\Python Projects\\Farming\\"+file_name, 'r') as file:
    csvreader = csv.reader(file)

    next(csvreader)
   
    for row in csvreader:
        current_moisture = float(row[1])
        print(f"Current Moisture content in the soil: {current_moisture}")
        desired_range1 = 20
        desired_range2 = 28
        flowRate = flowrate
        areaInAcres = area_in
        area = areaInAcres * 4047
        depth = 5.00

        if desired_range1 < current_moisture < desired_range2:
            print("Field is in ideal condition ")
            break
        elif current_moisture < desired_range1:
            vol_field = area * depth
            water_content_req = ((desired_range1 - current_moisture) / 100) * vol_field
            water_content_req = float(water_content_req)
            x = water_content_req / flowRate
            time = round(x) + 2
            time = str(time)
            print("Run the motor for " + time + " minutes")
            break
        else:
            print("Turn off the motor, you have watered enough")
            break

    return time         
    

def promptPumpController():

    driver.find_element(By.XPATH,"//span[contains(text(),'Dashboards')]").click()
    time.sleep(5)
   
    #clicks pump controller
    driver.find_element(By.XPATH,"//a[contains(text(),'Pump controller')]").click()
    time.sleep(5)

    #reload page
    driver.get("https://beta.thethingsmate.com/console/app/dashboards/680-pump-controller")
    time.sleep(5)

    #refresh page
    driver.find_element(By.XPATH,"//span[contains(text(),'Refresh')]").click()
    time.sleep(5)


def turnOnPump(contact,medium):

    promptPumpController()
    driver.find_element(By.XPATH,"//span[contains(text(),'Turn ON')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH,"//span[contains(text(),'Yes')]").click()
    sendMsg("Pump Controller is Turned ON",contact,medium)
    print("Pump Turned ON")
    time.sleep(5)


def turnOffPump(contact,medium):

    driver.find_element(By.XPATH,"//span[contains(text(),'Turn OFF')]").click()
    time.sleep(5)
    driver.find_element(By.XPATH,"(//span[contains(text(),'Yes')])[2]").click()
    time.sleep(5)
    sendMsg("Pump Controller is Turned OFF",contact,medium)
    driver.quit()
    print("Pump Turned Off")


@ app.route('/crop-recommend')
def crop_recommend():
    return render_template('crop.html')


@ app.route('/')
def fertilizer_recommend():
    return render_template('fertilizer.html')

@app.route('/pumpcontroller')
def pump_controller():
    return render_template('pumpcontroller.html')
    

@ app.route('/crop-predict', methods=['POST','GET'])
def cropPrediction():
    
    if request.method == 'POST':
        N = float(request.form['nitrogen'])
        P = float(request.form['phosphorous'])
        K = float(request.form['potassium'])
        ph = float(request.form['pH'])
        rainfall=float(request.form['rainfall'])
        temperature=float(request.form['temperature'])
        humidity=float(request.form['humidity'])
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        algo=request.form['algo']

        if(algo=="RF"):
            crop_recommendation_model=rf_model
        elif(algo=="DT"):
            crop_recommendation_model=dt_model
        elif(algo=="LR"):
            crop_recommendation_model=lr_model
        elif(algo=="NB"):
            crop_recommendation_model=nb_model
        elif(algo=="SVM"):
            crop_recommendation_model=svm_model
        else:
            crop_recommendation_model=xg_model                 

        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]

        if(crop_recommendation_model==xg_model):
            x=crops[final_prediction]
        else:
            x=final_prediction    

    return render_template('crop.html',message="Recommended Crop is "+x)


@ app.route('/fertilizer-predict', methods=['POST'])
def fertilizerPrediction():

    if request.method == 'POST':
       
        crop_name=request.form['crops']
        notification_medium=request.form['notification_medium']
        contact=request.form['contact']
        time_interval=request.form['crop_status']
        job(crop_name,contact,time_interval,notification_medium)      
        response = Markup(str(fertilizer_dic_ui['KLow']))  

    return render_template('fertilizer.html',message=response)


@ app.route('/trigger_pump_controller',methods=['POST'])
def pumpcontroller():

    if request.method == 'POST':
        area=float(request.form['area'])
        flowrate=float(request.form['flowrate'])
        medium=request.form['notification_medium']
        contact=request.form['contact']
        option=request.form['pump_controller_action']
        fetch_file_from_TTN()
        calculated_time=predict_time(area,flowrate)
        if(option=='Yes'):
            turnOnPump(contact,medium)
            # time.sleep(int(calculated_time))
            time.sleep(10)
            turnOffPump(contact,medium)
    return render_template('pumpcontroller.html',message="Pump controller turned is on for "+calculated_time+"minutes")    

 
if __name__ == '__main__':
    app.debug=True
    app.run()


























