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
# options.add_experimental_option("prefs",{"download.default_directory":"C:\\Users\\Teja\\OneDrive\\Desktop\\Selenium Automation\\"})

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

filename="Soil_NPK_sensor_-1_"+str(year)+'_'+month+'_'+day+'.csv'
# Loading crop recommendation model

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

notification_medium=''
time_interval=''

def sendMsg(Message,contact):

      contactno='+91'+contact
      print("sending msg")
      account_sid = "AC927097c6ffc585d6ffa4322bd090b52a" 
      auth_token = "ac338ef290f6b1ed53a3dacb79e55dc5"
      client = Client(account_sid,auth_token)
      message=client.messages.create(body=Message,from_='+15673131213',to=contactno)
     
  		

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
   

def repeatTask():

    #refresh button
    driver.find_element(By.XPATH,"//*[@id='application-root']/div[2]/div/div/div[1]/div[2]/span/div/button[1]").click()
    time.sleep(5)

    before = os.listdir('./') 
     
    if(len(before)==9):
        os.remove(filename)

    #3dots
    driver.find_element(By.XPATH,"//*[@id='dashboard-container']/div/div/div[3]/div/div/div[1]/div[1]/a").click()
    time.sleep(3)

    #download npkTable
    driver.find_element(By.XPATH,"/html/body/div/div/div/ul/li[1]/a").click()
    time.sleep(8)

    print("repeat task method")

    

def job():

    # driver.maximize_window()

    # Navigate to the URL of the website
    driver.get(url)

    #Sending Keys
    driver.find_element(By.XPATH,"//input[@id='user_id']").send_keys(username)
    driver.find_element(By.XPATH,"//input[@id='password']").send_keys(password) 
    time.sleep(5)


    #clicks login
    driver.find_element(By.XPATH,"//button[@class='_1h5on2Eq5J E2kP6n1yfv']").click()
    time.sleep(5)

    
    #clicks console
    driver.find_element(By.XPATH,"//span[@class='wTOG3ofQ0S']").click()
    time.sleep(5)

    
    #clicks Application Server
    driver.find_element(By.XPATH,"//div[@class='rlCIwsujpJ']").click()
    time.sleep(5)

    #clicks cvr-smart-agriculture
    driver.find_element(By.XPATH,"//*[@id='application-root']/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[8]/td[1]/a").click()
    time.sleep(5)

    #reload page
    driver.get("https://beta.thethingsmate.com/console/app/dashboards/576-cvr-smart-agriculture")
    time.sleep(5)

    print("job method")
    repeatTask()
    # schedule.every(int(time_interval)).seconds.do(repeatTask)

    # while True:
    #     schedule.run_pending()
    
    driver.quit() 



@ app.route('/fertilizer-predict', methods=['POST'])
def fertilizerPrediction():

    if request.method == 'POST':
       
        crop_name=request.form['crops']
        notification_medium=request.form['notification_medium']
        contact=request.form['contact']
        time_interval=request.form['crop_status']

        print("crop=",type(crop_name))
        print("n_m="+notification_medium)
        print("contact="+contact)
        print("time="+time_interval)
        job()    
        key=processCsvFile(crop_name)
        sendMsg(fertilizer_dic_msg[key],contact)   
        response = Markup(str(fertilizer_dic_ui[key]))  

    return render_template('fertilizer.html',message=response)


@ app.route('/crop-recommend')
def crop_recommend():
    return render_template('crop.html')


@ app.route('/fertilizer-recommend')
def fertilizer_recommend():
    return render_template('fertilizer.html')
    
    


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




# @ app.route('/fertilizer-predict', methods=['POST'])
# def fertilizerPrediction():

#     if request.method == 'POST':
#         N = float(request.form['nitrogen'])
#         P = float(request.form['phosphorous'])
#         K = float(request.form['potassium'])
#         crop=request.form['crops']

#         df = pd.read_csv('Data/fertilizer.csv')
#         nval = df[df['Crop'] == crop]['N'].iloc[0]
#         pval= df[df['Crop'] == crop]['P'].iloc[0]
#         kval= df[df['Crop'] == crop]['K'].iloc[0]

#         n = nval - N
#         p = pval - P
#         k = kval - K

#         temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
#         max_value = temp[max(temp.keys())]
#         if max_value == "N":
#             if n<0:
#                 key="NHigh"
#             else:
#                 key="NLow"
#         elif max_value=="P":
#             if p<0:
#                 key="PHigh"
#             else:
#                 key="PLow"
#         else:
#             if k<0:
#                 key="KHigh" 
#             else:
#                 key="KLow"

#         response = Markup(str(fertilizer_dic[key]))                               
        
       

#     return render_template('fertilizer.html',message=response)


 
if __name__ == '__main__':
    app.debug=True
    app.run()