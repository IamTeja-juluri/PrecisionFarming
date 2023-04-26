import csv
import datetime

year=datetime.date.today().year
month=datetime.date.today().month
day=datetime.date.today().day

if(month<10):
    month='0'+str(month)

if(day<10):
    day='0'+str(day)


def predict_time(area_in,flowrate):
 
    filename="EC_SENSOR_2_"+str(year)+'_'+str(month)+'_'+str(day)+'.csv'

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

    x=len(rows)
    current_moisture = float(rows[2][1])
    print(f"Current Moisture content in the soil: {current_moisture}")
    desired_range1 = 20
    desired_range2 = 28
    flowRate = flowrate
    areaInAcres = area_in
    area = areaInAcres * 4047
    depth = 1.5

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
    return time        
   
predict_time(50,10)   