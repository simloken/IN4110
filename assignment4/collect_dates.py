import re
from typing import Tuple
import numpy as np
## -- Task 3 (IN3110 optional, IN4110 required) -- ##


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """
    
    days = np.linspace(1,31,31, dtype=np.int64)
    days = [str(x) for x in days]
    for i in range(len(days)): #adds zero-padded 1-9
        j = zero_pad(days[i])
        if j != days[i]:
            days.append(j)
    
    month_names = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    
    
    #what follows is (perhaps) some of the ugliest code I've ever written, apologies in advance
    #i've since discovered that this could probably be written as [0-31], [0-12] etc., or something like that. Might fix later, although this works.
    monthsNum = ((str(days[0:12][::-1])+f'{days[31:]}').strip('[').strip(']').replace(',', '|')#PS: We reverse the order such that we avoid odd cases where
    ).replace(' ', '').replace("'", '').replace('[', '').replace(']', '|')#we'd match to 1 when we were suppose to match to 10,11 or 12
    
    days = str(days[::-1]).strip('[').strip(']').replace(',', '|').replace(' ', '').replace("'", '') #same applies here, we also reverse
    
    month_names = str(month_names).strip('[').strip(']').replace(',', '|').replace(' ', '').replace("'", '')
          
    years = str(np.linspace(1000, 2029, 1030, dtype=np.int64).tolist()).strip('[').strip(']').replace(',', '|').replace(' ', '')

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = years
    # month should accept month names or month numbers
    month = month_names+'|'+monthsNum
    # day should be a number, which may or may not be zero-padded
    day = days

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return zero_pad(s)

    # Convert to number as string
    
    month_names = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    
    k = 0
    for i in month_names:
        k += 1
        if i.lower() == s.lower():
            return zero_pad(str(k))
            


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    
    if len(n) == 1:
        return '0' + n
    else:
        return n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    
    year, month, day = get_date_patterns()


    # Date on format DD/MM/YYYY
    DMY = re.findall(r'({})\W+({})\W+({})'.format(day,month,year), text, flags = re.I| re.S)

    # Date on format MM/DD/YYYY
    MDY = re.findall(r'({})\W+({})\W+({})'.format(month,day,year), text, flags = re.I| re.S)


    #day = str(day.split('|')[::-1]).strip('[').strip(']').replace(',', '|').replace(' ', '').replace("'", '')
    # Date on format YYYY/MM/DD and ISO format
    YMD = re.findall(r'({})\W+({})\W+({})'.format(year,month,day), text, flags = re.I| re.S) #ISO and YMD in one

    # list with all supported formats
    dates = []
    
    for i in DMY:
        dates.append('{}/{}/{}'.format(i[2], convert_month(i[1]), zero_pad(i[0])))
    for i in MDY:
        dates.append('{}/{}/{}'.format(i[2], convert_month(i[0]), zero_pad(i[1])))
    for i in YMD:
        dates.append('{}/{}/{}'.format(i[0], convert_month(i[1]), zero_pad(i[2])))
        
    
    
    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        f = open(f'{output}'+'.txt', 'w', encoding="utf-8")
        for i in dates:
            f.write(f'{i} \n')
        f.close()
        return

    return dates

