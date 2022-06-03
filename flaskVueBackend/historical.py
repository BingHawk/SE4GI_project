from decimal import DivisionByZero
from flask import jsonify
import requests
import datetime as dt
import concurrent.futures


# t = dt.datetime.now()
# now = t.replace(second = 0, minute = 0)
# oneMonthAgo = now - dt.timedelta(days = 30)
# oneYearAgo  = now - dt.timedelta(days = 365)

# dateformat = "%Y-%m-%dT%H:%M:%S"
# print(now.strftime(dateformat)+"+00:00")
# print(oneMonthAgo.strftime(dateformat)+"+00:00")
# print(now.strftime(dateformat)+"+00:00")

def getMonthDataF(city):
    days = 30
    print("querying moth data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 59, minute = 59, hour=23) # end of today the starting day of query
    # endDay = startDay - dt.timedelta(days = days) #iterate untill d0 == stoptime

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(days):
            endDay = startDay - dt.timedelta(days = 1)
            f = executor.submit(queryByDay, startDay, endDay, city)
            futures.append(f)
            startDay = endDay
        res = {}
        paramUnits = {}
        for future in concurrent.futures.as_completed(futures):

            resDay, paramUnitsDay = future.result()
            res.update(resDay)
            paramUnits.update(paramUnitsDay)

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

            currentDay = endDay.replace(hour=0,minute=0,second=0,microsecond=0)# + dt.timedelta(days = 1)
            while currentDay != endDay.replace(hour=0,second=0,minute=0,microsecond=0) + dt.timedelta(days = days):
                currentDay = currentDay + dt.timedelta(days = 1)
                try:
                    avg = round(res[currentDay][param]['sum']/res[currentDay][param]['n'],4)
                    time_month[param]['data'].append(avg)
                except KeyError:
                    print("missing day: {} or parameter: {}".format(currentDay, param), end=("\r"))
                    time_month[param]['data'].append(None)
        
        return {"time_month":time_month}

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
    utcFormat = "%Y-%m-%dT%H:%M:%S+00:00" # Format recieved from openAQ 

    d0 = startDay
    d1 = d0 - dt.timedelta(days = 1) # The day before 
    limit = 5000 # Number of results accepted per query. Fewer means better preformance but risk of missing data. 

    iter = 0
    paramUnits= {}
    res = {}

    maxPages = 10
    while d0 != endDay: # Looping until every day of the month is done
        print("Querying day {}".format(iter+1),end="\r")
        page = 1
        getNextPage = True
        while getNextPage: #Looping though paginations
            d0String = d0.strftime(inFormat)+"%2B00%3A00"
            d1String = d1.strftime(inFormat)+"%2B00%3A00"
            url = f"https://api.openaq.org/v2/measurements?date_from={d1String}&date_to={d0String}&limit={limit}&page={page}&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
            # print(url)

            r = requests.get(url)
            resJson = r.json()
            if resJson['meta']['found'] < limit or page == maxPages:
                getNextPage = False
            else:
                if page == 1:
                    maxPages = resJson['meta']['found']// limit + 1
                    print(maxPages)

            page = page+1

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
                day = dt.datetime.strptime(result['date']['utc'],utcFormat).replace(hour=0,minute=0,second=0)

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
    resMonth = getMonthData('Roma')
    resMonth = getMonthDataF('Roma')

    print(resMonth)
    # resYear = getYearData('Firenze')
    # print(resYear)
