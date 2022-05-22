import requests
from datetime import datetime
from twilio.rest import Client
import time

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_END_POINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "3CTJ3CF50JTPPBJN"

NEWS_END_POINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "61a55dccead94cd6948dd751a842785b"

#  TODO - 1 Extract close price from API generated
#   calculate percentage difference for yesterday and day before yesterday
#   STEP 1: Use https://www.alphavantage.co
#   When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
stock_response = requests.get(url=STOCK_END_POINT, params=parameters)
stock_data = stock_response.json()
res = list(stock_data["Time Series (Daily)"].items())
yesterday_close = float(res[0][1]["4. close"])
previous_day_close = float(res[1][1]["4. close"])
# Percentage of decrease = |769.5900 - 728.0000|/769.5900 = 41.59/769.5900 = 0.054041762496914 = 5.4041762496914%
percentage = round((abs(yesterday_close - previous_day_close) / yesterday_close) * 100)

#  TODO - 2 Extract articles about tesla for three last days from techcrunch domain
#   STEP 2: Use https://newsapi.org
#   Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

today = datetime.now()
YESTERDAY = f"{today.year}-{today.month}-{today.day - 2}"
TWO_DAY_BEFORE_YESTERDAY = f"{today.year}-{today.month}-{today.day - 4}"

news_parameters = {
    "q": COMPANY_NAME,
    "from": TWO_DAY_BEFORE_YESTERDAY,
    "to": YESTERDAY,
    "domains": "techcrunch.com",
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": NEWS_API_KEY,
}

news_response = requests.get(url=NEWS_END_POINT, params=news_parameters)
news_report = news_response.json()
articles = news_report["articles"]


#  TODO - 3 Send SMS twilio
#   loop through the message and news_list created
#   STEP 3: Use https://www.twilio.com
#   Send a seperate message with the percentage change and each article's title and description to your phone number.

account_sid = "ACe96dae203aa3443275c0f123e645e3bf"
auth_token = "65e6e653e6e504de8059a14b58214d70"
stock_subject = ""
if percentage >= 5:
    if yesterday_close > previous_day_close:
        stock_subject = f"TSLA : 🔺 {percentage}%"

    elif previous_day_close > yesterday_close:
        stock_subject = f"TSLA : 🔻 {percentage}%"


    client = Client(account_sid, auth_token)

    for i in range(len(articles)):
        message = client.messages \
            .create(
            body=f"{stock_subject}\nArticle.no: {i + 1}\nHeadline: {articles[i]['title']}\n"
                 f"Brief: {articles[i]['description']}",
            from_='+19036627947',
            to='+919952783610')
        time.sleep(10)

