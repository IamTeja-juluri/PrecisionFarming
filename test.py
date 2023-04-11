import csv
import datetime

year=datetime.date.today().year
month=datetime.date.today().month
day=datetime.date.today().day

if(month<10):
    month='0'+str(month)

if(day<10):
    day='0'+str(day)

file_name="EC_SENSOR_2_"+str(year)+'_'+str(month)+'_'+str(day)+'.csv'


with open("C:\\Users\\Teja\\OneDrive\\Desktop\\Web Development\\Python Projects\\Farming\\"+file_name, 'r') as file:
    csvreader = csv.reader(file)

    next(csvreader)

    repeat = True
    for row in csvreader:
        if(repeat!=True):
           break
        current_moisture = float(row[1])
        print(f"Current Moisture content in the soil: {current_moisture}")
        desired_range1 = 20
        desired_range2 = 28
        flowRate = float(input("Enter flow rate of the motor in litres/minute "))
        areaInAcres = float(input("Enter field Area in acres "))
        area = areaInAcres * 4047
        depth = float(input("Enter depth of the field(approx) "))

        if desired_range1 < current_moisture < desired_range2:
            print("Field is in ideal condition ")
        elif current_moisture < desired_range1:
            vol_field = area * depth
            water_content_req = ((desired_range1 - current_moisture) / 100) * vol_field
            water_content_req = float(water_content_req)
            x = water_content_req / flowRate
            time = round(x) + 2
            time = str(time)

            print("Run the motor for " + time + " minutes")
        else:
            print("Turn off the motor, you have watered enough")
     