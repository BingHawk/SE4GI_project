from decimal import DivisionByZero
from flask import jsonify
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


def getMonthData(city):
    print("querying moth data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 0, minute = 0) # Today the starting day of query
    endDay = startDay - dt.timedelta(days = 30) #iterate untill d0 == stoptime

    res, paramUnits = queryByDay(startDay, endDay, city)

    # Desired JSON scheme
    #  {
    # "time_month": {
    #     particle1: {
    #         "data": [day1, day2, ... day30],
    #         "unit":unit
    #         },
    #     particle2: {
    #         "data": [day1, day2, ... day30],
    #         "unit": unit
    #         }
    # }
    time_month = {}
    for param in paramUnits.keys():
        time_month[param] = {"data": [], "unit": paramUnits[param]}

        currentDay = endDay.replace(hour=0,minute=0,microsecond=0)
        while currentDay != startDay.replace(hour=0,minute=0,microsecond=0):
            currentDay = currentDay + dt.timedelta(days = 1)
            try:
                avg = res[currentDay][param]['sum']/res[currentDay][param]['n']
                time_month[param]['data'].append(avg)
            except KeyError:
                print("missing day: {} or parameter: {}".format(currentDay, param))
                time_month[param]['data'].append(None)
    
    return {"time_month":time_month}

def getYearData(city):
    print("querying year data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 0, minute = 0) # Today the starting day of query
    endDay = startDay - dt.timedelta(days = 365) # The day that is furthest back. 

    res, paramUnits = queryByDay(startDay, endDay, city)

    # Desired JSON scheme
    #     {
    # "time_year": {
    #     particle1: {
    #         "data": [week1, week2, ... week52],
    #         "unit":unit
    #         },
    #     particle2: {
    #         "data": [week1, week2, ... week52],
    #         "unit": unit
    #         }
    # }
    time_year = {}
    for param in paramUnits.keys():
        time_year[param] = {"data": [], "unit": paramUnits[param]}

        currentDay = endDay.replace(hour=0,minute=0,microsecond=0)
        currentWeek = currentDay.isocalendar().week
        weekSum = 0
        weekN = 0
        while currentDay != startDay.replace(hour=0,minute=0,microsecond=0):
            currentDay = currentDay + dt.timedelta(days = 1)
            lastWeek = currentWeek
            currentWeek = currentDay.isocalendar().week
            if lastWeek == currentWeek:
                # still in same week, just add upp the numbers
                try:
                    weekSum += res[currentDay][param]['sum']
                    weekN += res[currentDay][param]['n']
                except KeyError:
                    print("missing day: {} or parameter: {}".format(currentDay, param))
                    continue
                pass
            else: 
                # new week has started, add last weeks average to data
                try: 
                    avg = weekSum / weekN
                    time_year[param]['data'].append(avg)
                except ZeroDivisionError:
                    #No meassurements in this week.
                    time_year[param]['data'].append(None)
                try:
                    # Reset week counts
                    weekSum = res[currentDay][param]['sum']
                    weekN = res[currentDay][param]['n']
                except KeyError:
                    print("missing day: {} or parameter: {}".format(currentDay, param))
                    weekSum = 0
                    weekN = 0
                pass
        try: 
            avg = weekSum / weekN
            time_year[param]['data'].append(avg)
        except ZeroDivisionError:
            #No meassurements in this week.
            time_year[param]['data'].append(None)
        

    return {"time_year":time_year}

def queryByDay(startDay, endDay, city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    summerFormat = "%Y-%m-%dT%H:%M:%S+02:00" # Format recieved from openAQ 
    winterFormat = "%Y-%m-%dT%H:%M:%S+01:00" # Format recieved from openAQ 


    d0 = startDay
    d1 = d0 - dt.timedelta(days = 1) # The day before 
    limit = 1000 # Number of results accepted per query. Fewer means better preformance but risk of missing data. 
    maxlimit = 5000 # The max limit the program is allowed to raise to. 5000 always works, 10'000 sometimes fails

    iter = 0
    paramUnits= {}
    res = {}
    while d0 != endDay: # Looping until every day of the month is done
        print("Querying day {}".format(iter+1),end="\r")
        page = 1
        while True: #Looping though paginations
            d0String = d0.strftime(inFormat)+"%2B00%3A00"
            d1String = d1.strftime(inFormat)+"%2B00%3A00"
            url = f"https://api.openaq.org/v2/measurements?date_from={d1String}&date_to={d0String}&limit={limit}&page={page}&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
            page = page+1

            r = requests.get(url)
            resJson = r.json()

            # informing about limit issues if present.
            if resJson['meta']['found'] > limit and limit < maxlimit:
                print("WARNING: The limit is lower than number of results, some results are lost")
                print("\tLimit: {}, Number of results: {}".format(limit, resJson['meta']['found']))
                if resJson['meta']['found'] < maxlimit:
                    print("\tRasing limit to {}".format(resJson['meta']['found']))
                    limit = resJson['meta']['found']
                else:
                    print("\tRasing limit to {}".format(maxlimit))
                    print("\tCannot raise limit more, at maxlimit")
                    limit = maxlimit

            # When an empty page is recieved, goes on to next day. 
            if not resJson['results']:
                break

            # Target format: 
            # res = {
            #     dateTime: {
            #         param1: {n: int, sum: float}
            #         param2:{n: int, sum: float}
            #         ...
            #         },{
            #         day2 = datetime,
            #         param1: {n: int, sum: float}
            #         param2:{n: int, sum: float}
            #         ...
            #        }, 
            #    }
            # }
            for result in resJson['results']:
                try:
                    day = dt.datetime.strptime(result['date']['local'],summerFormat).replace(hour=0,minute=0,second=0)
                except ValueError:
                    day = dt.datetime.strptime(result['date']['local'],winterFormat).replace(hour=0,minute=0,second=0)


                if day not in res.keys():
                    res[day] = {}

                param = result['parameter']
                if param in res[day]:
                    res[day][param]['n'] += 1
                    res[day][param]['sum'] += result['value']
                else:
                    res[day][param] = {'n':1,'sum':result['value']}
                
                if param not in paramUnits:
                    paramUnits[param] = result['unit']
        
        # Advance date counters
        d0 = d1
        d1 = d0 - dt.timedelta(days = 1)

        # Safetybreak
        iter += 1
        if iter == 400:
            print("Error: Infinite loop.")
            break
        
    return res, paramUnits


if __name__ == "__main__":
    cities = ['Roma', 'MILANO', 'Firenze']
    resMonth = getMonthData('MILANO')
    print(resMonth)
    # resYear = getYearData('Firenze')
    # print(resYear)
