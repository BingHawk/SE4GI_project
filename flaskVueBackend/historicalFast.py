import requests
import datetime as dt
import time
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
    print("querying month data for {}".format(city))
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

def getYearDataF(city):
    days = 365
    print("querying year data for {}".format(city))
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
                        print("missing day: {} or parameter: {}".format(currentDay, param), end="\r")
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

def getData(function,days,city):
    # print("querying moth data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 0, minute = 0) # Today the starting day of query
    endDay = startDay - dt.timedelta(days = days) #iterate untill d0 == stoptime

    res, paramUnits = function(startDay, endDay, city)

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
                avg = round(res[currentDay][param]['sum']/res[currentDay][param]['n'],4)
                time_month[param]['data'].append(avg)
            except KeyError:
                print("missing day: {} or parameter: {}".format(currentDay, param), end=("\r"))
                time_month[param]['data'].append(None)
    
    return {"time_month":time_month}

def getMonthData(city):
    print("querying month data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 0, minute = 0) # Today the starting day of query
    endDay = startDay - dt.timedelta(days = 30) #iterate untill d0 == stoptime

    res, paramUnits = queryByDayF(startDay, endDay, city)

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
                print("missing day: {} or parameter: {}".format(currentDay, param), end="\r")
                time_month[param]['data'].append(None)
    
    return {"time_month":time_month}

def getYearData(city):
    print("querying year data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 0, minute = 0) # Today the starting day of query
    endDay = startDay - dt.timedelta(days = 365) # The day that is furthest back. 

    res, paramUnits = queryByDayF(startDay, endDay, city)

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
                    print("missing day: {} or parameter: {}".format(currentDay, param), end="\r")
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

def queryByDayF2(startDay, endDay, city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    utcFormat = "%Y-%m-%dT%H:%M:%S+00:00" # Format recieved from openAQ 
    days = startDay - endDay
    
    paramUnits= {}
    res = {}
    page = 0
    iter = 0
    emptyPages = False
    numEmpty = 0
    while emptyPages == False:
        page = page+1
        d0 = startDay
        d1 = d0 - dt.timedelta(days = 1) # The day before 
        limit = 5000 # Number of results accepted per query. Fewer means better preformance but risk of missing data. 
    

        #Make list of url:s to be queried
        urls = []
        while d0 != endDay:
            d0String = d0.strftime(inFormat)+"%2B00%3A00"
            d1String = d1.strftime(inFormat)+"%2B00%3A00"
            url = f"https://api.openaq.org/v2/measurements?date_from={d1String}&date_to={d0String}&limit={limit}&page={page}&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
            urls.append(url)
            d0 = d1
            d1 = d0 - dt.timedelta(days = 1)

            # Safetybreak
        iter += 1
        if iter == 10:
            print("Error: Infinite loop.")
            break

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(requests.get, url) for url in urls]

            for future in concurrent.futures.as_completed(futures):
                r = future.result()

                resJson = r.json()

                # When an empty page is recieved, move on to next page. 
                if not resJson['results']:
                    numEmpty += 1
                    if numEmpty == days.days:
                        emptyPages = True

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
    return res, paramUnits

def queryByDayF(startDay, endDay, city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    utcFormat = "%Y-%m-%dT%H:%M:%S+00:00" # Format recieved from openAQ 



    d0 = startDay
    d1 = d0 - dt.timedelta(days = 1) # The day before 
    limit = 5000 # Number of results accepted per query. Fewer means better preformance but risk of missing data. 
    maxlimit = 5000 # The max limit the program is allowed to raise to. 5000 always works, 10'000 sometimes fails
    maxPages = 3 # Will always query this many pages. Lower means faster but data might be missed. 

    #Make list of url:s to be queried
    iter = 0
    urls = []
    while d0 != endDay:
        page = 1
        for page in range(maxPages):
            page = page+1
            d0String = d0.strftime(inFormat)+"%2B00%3A00"
            d1String = d1.strftime(inFormat)+"%2B00%3A00"
            url = f"https://api.openaq.org/v2/measurements?date_from={d1String}&date_to={d0String}&limit={limit}&page={page}&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
            urls.append(url)
        d0 = d1
        d1 = d0 - dt.timedelta(days = 1)


        # Safetybreak
        iter += 1
        if iter == 400:
            print("Error: Infinite loop.")
            break
    
    paramUnits= {}
    res = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            r = future.result()

            resJson = r.json()

            # When an empty page is recieved, move on to next page. 
            if not resJson['results']:
                continue

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
        return res, paramUnits
 
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

            # When an empty page is recieved, goes on to next day. 
            if not resJson['results']:
                break

            if resJson['meta']['found'] < limit or page == maxPages:
                getNextPage = False
            else:
                if page == 1:
                    maxPages = resJson['meta']['found']// limit + 1
                    print(maxPages)

            page = page+1

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
 
def threadingTrys():
    city = "Firenze"
    dayJumps = [10,20,30,40,50]
    for dayJump in dayJumps:
        t = dt.datetime.now()
        startDay1 = t.replace(second = 0, minute = 0) # Today the starting day of query
        endDay1 = startDay1 - dt.timedelta(days = dayJump) # The day that is furthest back. 
        
        startDay2 = startDay1 - dt.timedelta(days = dayJump) # The day that is furthest back.
        endDay2 = startDay2 - dt.timedelta(days = dayJump) # The day that is furthest back. 

        endDayT = startDay1 - dt.timedelta(days = dayJump*2) # The day that is furthest back. 

        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(queryByDayF, [startDay1, startDay2], [endDay1,endDay2], [city, city])

            for res, paramUnits in results: 
                pass

        finnish = time.perf_counter()
        t1 = finnish-start
        print(f"Task 1 finnished in {round(t1, 2)} seconds")

        start = time.perf_counter()
        res, paramUnits = queryByDayF(startDay1, endDayT, city)

        finnish = time.perf_counter()
        t2 = finnish-start
        print(f"Task 2 finnished in {round(t2, 2)} seconds")

        print(f"Ratio between task1/task2 {t1/t2}")

def threadingTestDays():
    city = "Firenze"
    dayJumps = [2,4,8]
    for dayJump in dayJumps:
        print(dayJump)
        t = dt.datetime.now()
        startDay = t.replace(second = 0, minute = 0) # Today the starting day of query

        start = time.perf_counter()
        res = getData(queryByDay, dayJump,city)
        # res, paramUnits = queryByDay(startDay, endDay, city)
        finnish = time.perf_counter()
        tO = finnish-start
        # print(f"Task O finnished in {round(tO, 2)} seconds")

        start = time.perf_counter()
        resF = getData(queryByDayF, dayJump, city)
        # resF, paramUnitsF = queryByDayF(startDay, endDay, city)
        finnish = time.perf_counter()
        t1 = finnish-start
        # print(f"Task 1 finnished in {round(t1, 2)} seconds")

        start = time.perf_counter()
        resF2 = getData(queryByDayF2, dayJump, city)
        # resF2, paramUnitsF2 = queryByDayF2(startDay, endDay, city)
        finnish = time.perf_counter()
        t2 = finnish-start
        # print(f"Task 2 finnished in {round(t2, 2)} seconds")

        start = time.perf_counter()
        #resF3 = getDataF(queryByDay, dayJump, city)
        finnish = time.perf_counter()
        t3 = finnish-start
        # print(f"Task 3 finnished in {round(t3, 2)} seconds")

        print(f"Ratio between task1/taskO {t1/tO}")
        print(f"Ratio between task2/taskO {t2/tO}")
        print(f"Ratio between task3/taskO {t3/tO}")

        # assert paramUnitsF == paramUnits, "Fast units is not same as slow result. paramUnitsF:\n{} \n res:\n{}".format(paramUnitsF,paramUnits)
        # assert paramUnitsF2 == paramUnits, "Fast units is not same as slow result. paramUnitsF2:\n{} \n res:\n{}".format(paramUnitsF2,paramUnits)
        assert resF2 == res, "Fast result is not same as slow result. resF2:\n{} \n res:\n{}".format(resF2,res)
        assert resF == res, "Fast result is not same as slow result. resF:\n{} \n res:\n{}".format(resF,res)
        # assert resF3 == res, "Fast result is not same as slow result. resF3:\n{} \n res:\n{}".format(resF3,res)


def threadingTestCity():
    cities = ['Roma', 'Firenze']

    for city in cities:
        print(city)

        start = time.perf_counter()
        res = getYearData(city)
        # res, paramUnits = queryByDay(startDay, endDay, city)
        finnish = time.perf_counter()
        tO = finnish-start
        print(f"Task O finnished in {round(tO, 2)} seconds")


        start = time.perf_counter()
        resF3 = getYearDataF(city)
        finnish = time.perf_counter()
        t3 = finnish-start
        print(f"Task 3 finnished in {round(t3, 2)} seconds")

        # print(f"Task 3 finnished in {round(t3, 2)} seconds")

        print(f"Ratio between task3/taskO {t3/tO}       ")

        # assert resF3 == res, "Fast result is not same as slow result. resF3:\n{} \n res:\n{}".format(resF3,res)



if __name__ == "__main__":
    # cities = ['Roma', 'MILANO', 'Firenze']
    # resMonth = getMonthData('MILANO')
    # print(resMonth)
    # resYear = getYearData('Firenze')
    # print(resYear)

    t = dt.datetime.now()
    startDay = t.replace(second = 59, minute = 59, hour = 23) # Today the starting day of query
    endDay = startDay - dt.timedelta(days = 1)

    # startDay2 = endDay
    # endDay2 = startDay2 - dt.timedelta(days = 1)

    # print("set one:",startDay, endDay)
    # print("set two:",startDay2, endDay2)

    # res, paramUnits = queryByDay(startDay, endDay, 'Firenze')
    # res2, paramUnits = queryByDay(startDay2, endDay2, 'Firenze')
    # resTot, paramUnits = queryByDay(startDay, endDay2, 'Firenze')

    # print(res)
    # print("\n")
    # print(res2)
    # print("\n")
    # print(resTot)
    # print("\n")

    # resMerge = {**res,**res2}

    # assert resTot == resMerge, "assert failed resTot:\n{}\nresMerge:\n{}".format(resTot,resMerge)


    # resF2, paramUnitsF2 = queryByDayF2(startDay, endDay, "Firenze")
    # print(resF2)
    # print(paramUnit)

    # resF3 = getDataF(queryByDay, 2, "Roma")
    # print(resF3)

    threadingTestCity()


    