import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

#URL of the item on Amazon you want to buy
AMAZON_URL = "AMAZON URL"
#Price you are waiting for the device to fall below
BUY_PRICE = <NEEDS TO BE A NUMBER>

SMTP_ADDRESS = os.environ["SMTP_ADDRESS"]
MY_EMAIl = os.environ["EMAIL_ADDRESS"]
PASSWORD = os.environ["EMAIL_PASSWORD"]

#Get's info in your language
#info from https://myhttpheader.com/
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(AMAZON_URL, headers=headers)
page = response.text

soup = BeautifulSoup(page, "html.parser")
price = soup.find(class_="a-offscreen")
# print(price)

clean_price = float(price.getText().replace("$", ""))
# print(clean_price)

title = soup.find(id="productTitle").get_text().strip()
# print(title)

if clean_price < BUY_PRICE:
    contents = f"{title} is on sale for {clean_price}!"

    with smtplib.SMTP(SMTP_ADDRESS) as connection:
        connection.starttls()
        connection.login(MY_EMAIl, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIl,
                            to_addrs=MY_EMAIl,
                            msg=f"Subject:Amazon price Alert~\n\n{contents}\n{AMAZON_URL}".encode("utf-8")
        )
