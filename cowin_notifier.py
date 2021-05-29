from twilio.rest import Client



import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time
import json

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client("ACb6b2b347c412cfe076b48ea33addb06e","5xxx")

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+918073489119'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
age = 24
pincodes = []
num_days = 5

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
# print(actual)
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
# print(actual_dates[0])
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format("269", actual_dates[0])

result1 = requests.get(URL, headers=header)
response_json = result1.json()
# print(json.dumps(response_json,indent=1))
for center in response_json["sessions"]:
    pincodes.append(center["pincode"])
# exit(0)
while True:
    counter = 0   
    body=""
    for pincode in pincodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            
            
            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                #print(json.dumps(response_json,indent=1))
                # exit(0)
                if response_json["centers"]:
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity_dose1"] >0  ) :
                                    print("heres"+str(session["available_capacity_dose1"]))
                                    body="Vaccine available\n"
                                    body+="Pincode: " + str(pincode)+"\nAvailable on: {}".format(given_date)+"\n"+center["name"]+"\n"+center["block_name"]+"\n Price: "+center["fee_type"]+"\n Availablity : "+str( session["available_capacity"]+session["available_capacity_dose1"] )
                                    print('Pincode: ' + str(pincode))
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                        body+=" \nVaccine type: "+session["vaccine"]+"\n"
                                    print("\n")
                                    counter = counter + 1
            else:
                print("No Response!")
                
    if counter:
        mixer.init()
        mixer.music.load('D:\Cowin\sound_dingdong.wav')
        mixer.music.play()
        
        print("Vaccine available")
        # print(body)
        client.messages.create(body=body,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
    else:
        print("Vaccine not Available")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
mixer.init()
mixer.music.load('D:\Cowin\sound_dingdong.wav')
mixer.music.play()
print("Search Completed")



