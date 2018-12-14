
import pandas as pd
import requests
import numpy as np
import math
from forex_python.converter import CurrencyRates

url = "https://api.manheim.com/oauth2/token.oauth2”

payload = “grant_type=client_credentials”
headers = {
   ‘authorization’: “Basic eTZqdDh2Nnc1MmJrZzQyMm40a3A5Mzd0OnVRRXBEZmJEanI=“,
   ‘content-type’: “application/x-www-form-urlencoded”,
   ‘cache-control’: “no-cache”,
   ‘Postman-Token’: “026cd8be-a3ba-4517-ba82-633f2c7f1fdd”
}

response = requests.request(“POST”, url, data=payload, headers=headers)

token = ‘’

for val in response.json().values():
   token = token+' ’+val
token = token[1:]


def mmr(vin, odo, grade, trim):
   print(‘oldGrade’, grade)
   grade = float(grade)
   grade = grade * 10
   grade = int(grade)
   print(‘newGrade’, grade)
   url = “https://api.manheim.com/valuations/vin/“+vin+“?country=US&odometer=” + \
       str(odo)+“&region=ne&grade=” + str(grade) + \
       “&include=retail,historical,forecast”
   payload = “”
   headers = {
       ‘cache-control’: “no-cache”,
       ‘Postman-Token’: “0a8a0256-c4cb-41b9-aec8-b88817d93244",
       ‘authorization’: token
   }

   response = requests.request(“GET”, url, data=payload, headers=headers)

   carList = response.json()
   print(carList)
   try:

       all_cars = carList[‘items’]

       if carList[‘count’] > 1:
           for i in all_cars:
               temp = i[‘description’][‘trim’]
               if temp.lower().endswith(trim.lower()):
                   carList = i
       else:
           carList = carList[‘items’][0]

       car_id = carList[‘href’]
       start = car_id.find(‘id/‘) + 3
       end = car_id.find(‘?’)
       car_id = car_id[start:end]
       print(carList[‘adjustedPricing’][‘wholesale’][‘average’])

       url2 = “https://api.manheim.com/valuation-samples/id/“+car_id+“?country=US&region=NE”
       response2 = requests.request(
           “GET”, url2, data=payload, headers=headers)

       car_samples = response2.json()
       car_samples = car_samples[‘items’]
       car_count = len(car_samples)
       total_miles = []
       total_price = []
       total_grade = []
       for i in car_samples:
           try:
               total_price.append(i[‘purchasePrice’])
               total_miles.append(i[‘vehicleDetails’][‘odometer’])
               total_grade.append(int(i[‘vehicleDetails’][‘grade’]))
           except:
               1

       avg_price = np.median(total_price)
       avg_miles = np.mean(total_miles)
       avg_grade = np.mean(total_grade)

       cost_miles = avg_price / avg_miles
       cost_grade = avg_price/avg_grade

       car_price = avg_price

       if (odo - avg_miles > 0):
           car_price = car_price - \
               ((math.log(odo, avg_miles))*(odo-avg_miles)*0.1)
       else:
           car_price = car_price - \
               ((math.log(avg_miles, odo))*(odo-avg_miles)*0.1)

       if(grade - avg_grade > 0):
           car_price = car_price + \
               ((math.log((grade), avg_grade))*(grade-avg_grade)*100)
       else:
           car_price = car_price + \
               ((math.log(avg_grade, grade))*(grade-avg_grade)*100)

       c = CurrencyRates()
       current_rate = c.get_rate(‘USD’, ‘CAD’)
       print(“Avg Price in USD: “, avg_price, “Our MMR in USD: “,
             car_price, “Our MMR in CAD: “, car_price*current_rate)
       return(carList[‘adjustedPricing’][‘wholesale’][‘average’], car_id, car_count, car_price, car_price*current_rate)
   except:
       return(0, 0, 0, 0)

 vin = ‘2FMPK4J85GBB00877’
 odo = 63704
 odo = int(odo*0.621371)
 grade = 42
 #color = ‘BLACK’
 trim = ‘lariat’

 print(mmr(vin, odo, grade, trim))