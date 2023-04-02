import csv

import pandas as pd
from twilio.rest import Client

from Data.fertilizerdic import fertilizer_dic

filename="Soil_NPK_sensor_-1_2023_03_26.csv"




crop='rice'
notification_medium='Sms'
contact='7013206067'
# time_interval='120'


def sendMsg(Message):

      contactno=+917013206067
      account_sid = "AC927097c6ffc585d6ffa4322bd090b52a"
      auth_token = "dd68b13bce1d1348742f16932e8d46cc"
      client = Client(account_sid,auth_token)
      message=client.messages.create(body=Message,from_='+15673131213',to=contactno)

    
      
  

def fertilizer_prediction_result(rows):
        
        N=int(rows[0][1])
        P=int(rows[0][2])
        K=int(rows[0][3])

        df=pd.read_csv('Data/fertilizer.csv')

        print(df.dtypes)
        
        print('fine')

        
        nval=df[df['Crop']==crop]['N'].iloc[0]
        pval=df[df['Crop']==crop]['P'].iloc[0]
        kval=df[df['Crop']==crop]['K'].iloc[0]
        # print("kval="+kval)


        n=nval-N
        p=pval-P
        k=kval-K

        # print("k="+k)

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
        
        sendMsg(fertilizer_dic[key])      



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

    fertilizer_prediction_result(rows)

    print("process csv method")

   
processCsvFile()