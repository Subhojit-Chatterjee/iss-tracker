import time
import requests
import smtplib
from datetime import datetime, timezone


MY_LAT = 25.321377
MY_LONG = 74.586952
MY_EMAIL = "subhojittest2@gmail.com"
MY_PASS = "qtrwquzfbtnkqtpt"


def iss_in_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if (MY_LONG - 5) <= longitude <= (MY_LONG + 5) and (MY_LAT - 5) <= latitude <= (MY_LAT + 5):
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    current_hour = datetime.now(timezone.utc).hour

    if sunset <= current_hour or current_hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_in_location() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="subhojitrcm@gmail.com",
                            msg="Subject: ISS Overhead\n\nLook up!")
