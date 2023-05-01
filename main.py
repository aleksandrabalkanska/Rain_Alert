import requests
import auth
from twilio.rest import Client

WA_Endpoint = auth.WA_Endpoint
api_key = auth.api_key
account_sid = auth.account_sid
auth_token = auth.auth_token
twilio_phone = auth.twilio_phone
receiver_phone = auth.receiver_phone
city = auth.city

parameters = {
    "key": api_key,
    "q": city,
    "days": 1,
}

response = requests.get(url=WA_Endpoint, params=parameters)
response.raise_for_status()

weather_data = response.json()

will_rain = False

for hour in weather_data["forecast"]["forecastday"][0]["hour"][:12]:
    condition_code = hour["condition"]["code"]

    if condition_code > 1063:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="It's going to rain today!",
        from_=twilio_phone,
        to=receiver_phone
    )

    print(message.status)
