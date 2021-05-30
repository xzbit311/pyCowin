import  requests
from datetime import datetime

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot1894498260:AAHAucbm8v5_ALyPpUnr2HVrfWE1Ue0XXs0/sendMessage?chat_id=@COWIN_BPL_INFO&text="
#groupid = "__groupid__"

def fetch_data_from_cowin(district_id):
  query_params = "?district_id={}&date={}".format(district_id,today_date)
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  final_url = base_cowin_url + query_params
  response = requests.get(final_url,headers=headers)
  extract_availability_data(response)
  #print(response)

def extract_availability_data(response):
  response_json = response.json()
  for center in response_json["centers"]:
    for session in center["sessions"]:
      if (session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 18):
        message = "Name: {},\nAddress: {},\nSlots: {}, Minimum Age: {}".format(center["name"],center["address"],
                                                                                session["available_capacity_dose1"],
                                                                                session["min_age_limit"])
        send_message_telegram(message)

def send_message_telegram(message):
  #final_telegram_url = api_url_telegram.replace("__groupid__", groupid)
  final_telegram_url = api_url_telegram + message
  response = requests.get(final_telegram_url)
  print(response)

if __name__ == "__main__":
  fetch_data_from_cowin(312)
