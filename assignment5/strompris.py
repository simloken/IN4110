#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache
import numpy as np

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Retrieve one day worth of data.
    
    parameters:
        data (datetime.date object or None): The day to retrieve data from, if None defaults to today.
        location (str): The area to retrieve data from.
        
    returns:
        lst (list): A list containing all price data from given day and area.
    ...
    """
    if date is None:
        date = datetime.date.today().strftime("%Y/%m-%d")
    else:
        date = date.strftime("%Y/%m-%d")
    url = "https://www.hvakosterstrommen.no/api/v1/prices/%s_%s.json" %(date, location)
    r = requests.get(url).text.split('},')
    lst = []
    for i in r:
        lst.append(float(i.split(',')[0].split(':')[1]))
        
    return lst

# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "Oslo": "NO1",
    "Kristiansand": "NO2",
    "Trondheim": "NO3",
    "Tromsø": "NO4",
    "Bergen": "NO5",
    
}

color_dict = {
    "Oslo": "blue",
    "Kristiansand": "red",
    "Trondheim": "green",
    "Tromsø": "orange",
    "Bergen": "purple",
    
}
# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.values()),
) -> pd.DataFrame:
    """Retrieve data over a time period in multiple areas and consolidate to one DataFrame.
    
    parameters:
        end_date (datetime.date object or None): The date to stop at when retrieving data.
        days (int): The number of days to retrieve data from.
        locations (tuple or array-like): The locations to retrieve data from.
        
    returns:
        df (pandas.DataFrame): A consolidated DataFrame with all retrieved data.
    ...
    """
    
    if end_date is None:
        end_date = str(datetime.date.today()).split('-')
        end_date = [int(i) for i in end_date] 
        start_date = str(datetime.date.today() - datetime.timedelta(days=days)).split('-')
        start_date = [int(i) for i in start_date]
        dArray = np.arange(datetime.datetime(*start_date[:]),datetime.datetime(*end_date[:]), 
                       datetime.timedelta(days=1)).astype(datetime.datetime)
    
        
    else:
        start_date = end_date - datetime.timedelta(days=days)
        dArray = np.arange(start_date, end_date, 
                       datetime.timedelta(days=1)).astype(datetime.datetime)
    
    
    if type(locations) == str:
        tmp = []
        for i in dArray:
            tmp.append(fetch_day_prices(i, locations))
        return tmp
    tmp2 = []
    for i in locations:
        tmp = []
        for j in dArray:
            tmp.extend(fetch_day_prices(j, i))
            
        tmp2.append(tmp)
        
    
    df = pd.DataFrame(np.transpose(tmp2), columns=list(locations))
    tmp = []
    for i in dArray:
        for j in range(24):
            t = i.strftime("%Y-%m-%d").split('-')
            t = [int(x) for x in t] 
            t.append(j)
            tmp.append(datetime.datetime(*t[:]))
    
    toRemove = datetime.datetime(2022, 10, 30, 3) #daylight savings time
    if toRemove in tmp:
        j = 0
        for i in tmp:
            if i == toRemove:
                idx = j
                
            j += 1
            
        df = df.drop(idx)

    df['time'] = tmp
    
    return df

# task 5.1:


def plot_prices(df: pd.DataFrame, locations=None) -> alt.Chart:
    """Plot energy prices over time.

    parameters:
        df (pandas.DataFrame): A dataframe containing all data to plot.
        locations (array-like or None): which locations to plot.
        
    returns:
        alt.Chart (altair.Chart): A chart containing all the data from df and an average over a timespan of one day.
    """
    
    end_date = df['time'][0]
    days = int(len(df)/24)
    
    if locations == None: #default
        locations=list(LOCATION_CODES.values())
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        
    if set(locations).intersection(list(LOCATION_CODES.keys())) != set():
        l = []
        colors = []
        for i in locations:
            l.append(LOCATION_CODES[i])
            colors.append(color_dict[i])
        locations = l
     
    avgChart = plot_daily_prices(df[locations])
    
    
    #avgChart['time'] = np.arange(end_date, end_date + datetime.timedelta(days=days), datetime.timedelta(days=1)).astype(datetime.datetime)
    avgChart['time'] = df['time']
        
    df2 = fetch_prices(end_date, 7, locations).append(df).drop(['time'], axis=1) #week prior worth of data for comparisons between previous prices
    hourDiff = df2.diff(axis=0).iloc[24*7:, :] #after getting the differential, remove data outside of dataset (ie first 7 weeks)
    hourDiff = hourDiff.rename(columns={
            'NO1': 'NO1h', 'NO2': 'NO2h', 'NO3': 'NO3h', 'NO4': 'NO4h', 'NO5': 'NO5h'})
    dayDiff = df2.diff(periods=24, axis=0).iloc[24*7:, :]
    dayDiff = dayDiff.rename(columns={
            'NO1': 'NO1d', 'NO2': 'NO2d', 'NO3': 'NO3d', 'NO4': 'NO4d', 'NO5': 'NO5d'})
    weekDiff = df2.diff(periods=24*7, axis=0).iloc[24*7:, :]
    weekDiff = weekDiff.rename(columns={
            'NO1': 'NO1w', 'NO2': 'NO2w', 'NO3': 'NO3w', 'NO4': 'NO4w', 'NO5': 'NO5w'})
        
    for i in hourDiff.columns:
        df[i] = -hourDiff[i]
    for i in dayDiff.columns:
        df[i] = -dayDiff[i]
    for i in weekDiff.columns:
        df[i] = -weekDiff[i]
    
    diffLocs = []
    diffLocs.append(list(hourDiff.columns))
    diffLocs.append(list(dayDiff.columns))
    diffLocs.append(list(weekDiff.columns))
    
    
    scale = alt.Scale(domain=locations, range=colors)


    chart = alt.Chart(df).mark_line().transform_fold(
            fold=locations,
            as_=['Area', 'value']
            
            ).transform_fold(
            fold=diffLocs[0],
            as_=['Areah', 'valueh']
            
            ).transform_fold(
            fold=diffLocs[1],
            as_=['Aread', 'valued']
            
            ).transform_fold(
            fold=diffLocs[2],
            as_=['Areaw', 'valuew']
            
            ).encode(
                    x=alt.X('time:T', title='Date'), 
        y=alt.Y('value:Q', title='NOK per kWh'), 
        color= alt.Color('Area:N', scale=scale, title='Area:'),
        tooltip=[alt.Tooltip('time', title='Date'),
                 alt.Tooltip('time', title='Time', timeUnit='hours'),
                 alt.Tooltip('value:Q', title='Price', format='.2f'),
                 alt.Tooltip('valueh:Q', title='Previous Hour', format='.2f'),
                 alt.Tooltip('valued:Q', title='Previous Day', format='.2f'),
                 alt.Tooltip('valuew:Q', title='Previous Week', format='.2f')])
    
    scale = alt.Scale(domain=list(set(avgChart['Avg'])), range=['black']*len(avgChart['time']))
    avgChart['zeros'] = np.zeros(len(avgChart))
    
    
    chart2 = alt.Chart(avgChart).mark_area(opacity=.7).encode(
            x='time',
            y='zeros:Q',
            y2 = 'Avg:Q',
            color = alt.Color('Avg:Q', scale=scale, title=['Average of all', 'active areas:']))
    
    
    return (chart2 + chart).configure_legend(gradientLabelLimit=1, labelFontSize=8, gradientLength=14, gradientLabelOffset = -12
            ).configure_axisX(
                labelOffset=12,labelAngle=-30)


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Create a dataframe to use when plotting the average over a one day period.

    parameters:
        df (pandas.DataFrame): A dataframe containing all data to plot.
        
    returns:
        df (pandas.DataFrame): A new dataframe which holds the mean value of each given day.
    """
    
    df = df.copy()
    
    df['mean'] = df.mean(axis=1)
    j = 0
    sm = 0
    dailyMean = []
    for i in df['mean']:
        sm += i
        j += 1
        if j == 23:
            j = 0
            dailyMean.append(sm/24)
            sm = 0
            
    
    dailyMean = np.repeat(dailyMean, 24)
    
    return pd.DataFrame(data=dailyMean, columns=['Avg'])
        

# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    'Shower': 30,
    'Baking': 2.5,
    'Heat': 1
}


def plot_activity_prices(
        activity: str = "Shower", minutes: int = 10, location="NO1"
) -> alt.Chart:
    """Create a chart which shows prices at during the day for a given activity, location and time.

    parameters:
        activity (str): Activity to pricecheck.
        minutes (int): Number of minutes activity happens.
        location (str): Location to fetch prices from.
        
    returns:
        alt.Chart (altair.Chart): A chart containing one days worth of data for activity, location and time
    """
    
    if location not in LOCATION_CODES.values():
        location = LOCATION_CODES[location]
        
    
    
    
    df = np.array(fetch_day_prices(location=location))
    
    if minutes > 60:
        minutes = 60
        
    frac = (minutes/60)
    
    pricesDict = {
            'Shower': df*ACTIVITIES['Shower']*frac,
            'Baking': df*ACTIVITIES['Baking']*frac,
            'Heat': df*ACTIVITIES['Heat']*frac            
            }
    #round down to previous hour so as to show next 24 hours
    starttime = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    
    time = np.arange(starttime,starttime + datetime.timedelta(days=1), 
                       datetime.timedelta(hours=1)).astype(datetime.datetime)
        
    df = pd.DataFrame(np.array((pricesDict[activity], time)).T, columns=['Price', 'Time'])
    
    
    
    return alt.Chart(df).mark_line().encode(x=alt.X('Time', title='Time'),
                     y=alt.Y('Price', title='NOK per %g minutes' %(minutes)),
                     tooltip=[alt.Tooltip('Time', title='Date'),
                 alt.Tooltip('Time', title='Time', timeUnit='hours'),
                 alt.Tooltip('Price', title='Price')]).configure_axisX(
                labelOffset=12,labelAngle=-30)
    
    
    
    
    
def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
