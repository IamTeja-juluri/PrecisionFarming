import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from twilio.rest import Client
import pandas as pd
from Data.fertilizerdic import fertilizer_dic
import os


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

params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "C:\\Users\\Teja\\OneDrive\\Desktop\\Selenium Automation\\"}}
driver.execute("send_command", params)

username="cvr-heights-2022"
password="Cvrece123"
url="https://beta.thethingsmate.com/oauth/login"
filename="Soil_NPK_sensor_-1_2023_04_01.csv"


def sendMsg(Message):

    print(Message)

    account_sid = "AC927097c6ffc585d6ffa4322bd090b52a"
    auth_token = "dd68b13bce1d1348742f16932e8d46cc"
    client = Client(account_sid,auth_token)

    message=client.messages.create(
         body=Message,
         from_='+15673131213',
         to='+917013206067'
     )
    
    print("send msg")
  
  

def fertilizerPrediction(rows):
        
        N=int(rows[0][1])
        P=int(rows[0][2])
        K=int(rows[0][3])
        crop='apple'

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
        
        return fertilizer_dic[key]      



def processCsvFile():

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

    Message=fertilizerPrediction(rows)

    print("process csv method")

    sendMsg(Message)
   


def repeatTask():

    #refresh button
    driver.find_element(By.XPATH,"//*[@id='application-root']/div[2]/div/div/div[1]/div[2]/span/div/button[1]").click()
    time.sleep(5)

    before = os.listdir('./') 
     
    if(len(before)==6):
        os.remove(filename)

    #3dots
    driver.find_element(By.XPATH,"//*[@id='dashboard-container']/div/div/div[3]/div/div/div[1]/div[1]/a").click()
    time.sleep(3)

    #download npkTable
    driver.find_element(By.XPATH,"/html/body/div/div/div/ul/li[1]/a").click()
    time.sleep(8)

    print("repeat task method")

    processCsvFile()
    



def jobb():

    driver.maximize_window()

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
    time.sleep(10)

    
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
    schedule.every(10).seconds.do(repeatTask)

    while True:
        schedule.run_pending()
    
    driver.quit() 






jobb()


