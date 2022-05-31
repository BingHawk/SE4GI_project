import requests
import datetime as dt

# t = dt.datetime.now()
# now = t.replace(second = 0, minute = 0)
# oneMonthAgo = now - dt.timedelta(days = 30)
# oneYearAgo  = now - dt.timedelta(days = 365)

# dateformat = "%Y-%m-%dT%H:%M:%S"
# print(now.strftime(dateformat)+"+00:00")
# print(oneMonthAgo.strftime(dateformat)+"+00:00")
# print(now.strftime(dateformat)+"+00:00")

cities = ['Roma', 'Milano', 'Firenze']

def getMonthData(city):
    dateformat = "%Y-%m-%dT%H%%3A%M%%3A%S"
    t = dt.datetime.now()
    now = t.replace(second = 0, minute = 0)
    oneMonthAgo = now - dt.timedelta(days = 30)

    nowString = now.strftime(dateformat)+"%2B00%3A00"
    monthString = oneMonthAgo.strftime(dateformat)+"%2B00%3A00"

    url = f"https://api.openaq.org/v2/measurements?date_from={monthString}&date_to={nowString}&limit=1000&page=1&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"

    r = requests.get(url)

    resJson = r.json()
    pass

url2 = "https://api.openaq.org/v2/measurements?date_from=2022-04-01T00%3A00%3A00%2B00%3A00&date_to=2022-05-31T08%3A10%3A00%2B00%3A00&limit=100&page=1&offset=0&sort=desc&radius=1000&city=Roma&order_by=datetime"


getMonthData('Roma')