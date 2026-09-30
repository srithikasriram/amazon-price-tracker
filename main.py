from bs4 import BeautifulSoup
import requests
import smtplib
import os

EMAIL = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
HEADERS = headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36", # Mimics a real browser
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive"
}

item_name = str(input("What is the name of the item? "))
price_limit = float(input("What is the maximum price you are willing to pay for it? "))
URL = str(input("Paste the Amazon URL here. ")).strip()

response = requests.get(URL, headers=HEADERS)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")
price_str = soup.find( class_= "a-price-whole").getText()
price_dec = soup.find( class_= "a-price-fraction").getText()
price = float(price_str+price_dec)

if price < price_limit:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject: PRICE DROP \n\n Buy the {item_name} now. The price is ${price}")
