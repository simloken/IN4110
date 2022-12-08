from typing import List  # isort:skip
import re
import requests
import time
from itertools import chain
import numpy as np
import multiprocessing as mp
from bs4 import BeautifulSoup


def find_path(start: str, finish: str, threads=None) -> List[str]:
    """
    Takes two wikipedia urls and finds the path between them.
    Prints total time elapsed, number of "jumps" and the found path
    
    Arguments:
            start: str
                wikipedia url to start from
            finish: str
                wikipedia url to finish at
            threads: None or int
                threads to use as this can get computationally heavy.
                None automatically uses all available threads.
    Returns:
            path: list
                list of urls forming a path from start to finish


    """
    
    t0 = time.perf_counter()
    print(f'Pathing from:\n{start}\nto\n{finish}\n')
    
    if threads == None:
        threads = int(mp.cpu_count())
    elif type(threads) != int:
        raise ValueError('Threads must be an integer')
        
    else:
        if threads <= 0:
            raise ValueError('Threads must be greater than 0')
    
    if threads == 1:
        path = nonParaPath(start, finish)
    else:
        path = paraPath(start, finish, threads)
            
        
    assert path[0] == start
    assert path[-1] == finish
    pathExists(path)
    t1 = time.perf_counter() - t0
    print('------------------------------------')
    print('Total time elapsed: %.2fs using %i thread(s).' %(t1, threads) )
    print('------------------------------------')
    print(f'Total jumps: {len(path)-1}\nWith path:')
    for i in path:
        print(f'{i}')
    print('------------------------------------')
    return path


def URL_finder(url):
    """
    Takes a wikipedia URL and returns a list with all URLs found on that page
    
    Arguments:
            Url: str
                wikipedia url
    Returns:
            urls: list
                list of urls


    """
    
    base = url.split('/wiki/')[0]
    urlreq = requests.get(url).text
    # src finds the text between quotes of the `src` attribute
    
    #find navbox links, this increases runtime by a considerable margin and is thus left out
#    text = requests.get(url).text
#    soup = BeautifulSoup(text, 'html.parser')
#    navurls = []
#    data = soup.findAll('div',attrs={'class':'navbox'})
#    if data:
#        for div in data:
#            links = div.findAll('a')
#            for a in links:
#                if a.has_attr('href'):
#                    navurls.append(a['href'])
                    
                    
    
    #isolate such that we only get urls within the body of the given article
    bodyString = re.search(r'<div id=\"bodyContent\" class=\"vector-body\">(.*)<\/div>', urlreq, flags = re.S | re.I) #worked out in https://regex101.com/r/W76Pgf/1
    bodyString = re.sub(r'<div class=\"mw-collapsible-content\"(.*\n)*.*</div>', '', bodyString.group(1), flags = re.S | re.I) #removes cases where we have links hidden in "expand" sidebars
    html = bodyString.split('id="References"')[0].split('class="reflist"')[0] #removes any links in references as they sometimes link back to wikipedia (and thus don't get culled)
        
    
    
    a_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    href_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    href_set = set()
    for a in a_pat.findall(html):
        match = href_pat.search(a)
        if match:
            href_set.add(match.group(1))
    
    urls = list(href_set)
    
#    urls.extend(navurls)
    
    urls = list(dict.fromkeys(urls))
    
    toremove = []
    for i in urls:
        if ':' in i: #remove namespaces and links out of wikipedia
            if '/wiki/' in i: #gross implementation that ensures we don't cull
                testCase = i.split('/wiki/') #articles with a colon (ex: The Avengers: Endgame as in the assignment)
                if ':_' in testCase[-1]: #checks if we have a comma followed by a whitespace, this is not the case for namespaces
                    continue #this will however still cull articles of the form X:Y, but I am unsure if such articles exist
                             #any non-namespace should be X: Y. Maybe for movies, books etc. which are stylized as X:Y.
                    
            toremove.append(i)
            continue   
        if '/wiki/' not in i: #culls non-wikipedia pages
            toremove.append(i)
            continue
        
        if '#' in i:
            if i.split('#')[0] == url: #cull links to specific sections/div tags
                toremove.append(i)
                continue
            
        if 'Main_Page' in i: #culls links back to the main page
            toremove.append(i)
     
        
        
    
    for i in toremove:
        urls.remove(i)
      
        
    if url in urls:
        urls.remove(url)
        
        
    articles = []
    for i in urls:
        if i != url:
            articles.append(f'{base}'+f'{i}')
    
    
    
    return articles


def flatten(l):
    """
    Flattens a list
    
    Arguments:
            l: list
                list to be flattened
    Returns:
            l: list
                flattened list


    """
    return list(chain.from_iterable(l))

def splitter(i, l):
    """
    Takes a list of values and splits them into i equal lists, if possible. If not, leftover
    values are added list-wise until none are left.
    
    Arguments:
            i: int
                Number of times to split l
            l: list
                list of values to be split
    Returns:
            L: list of lists
                nested lists


    """
    L = []
    j = 0
    i = int(i)
    length = len(l)
    if length % i != 0:
        down = int(np.floor(length/i))
        diff = length-down*i
    else:
        for j in range(i):
            down = int(np.floor(length/i))
            L.append(l[j*down:(j+1)*down])
            
        return L
    for j in range(i):
        L.append(l[j*down:(j+1)*down])
     
    k = 0
    for j in l[-diff:]:
        L[k].extend([j])
        k +=1
        if k == i:
            k = 0 
    return L
  
def isReverse(urls, targetUrl, toMatch):
    """
    Takes a set of urls and checks if they lead back to the url they came from. Necessary for all urls
    found from "finish". Additionally continously checks if we have a match (this saves significant runtime)
    
    Arguments:
            urls: list
                list of urls
            targetUrl: str
                url that urls has to lead back to
            toMatch: dict
                dictionary of all urls from start
                
    Returns:
            dic: dictionary
                dictionary to be appended to all urls.
                Only returned if a match is found
            -or-
            reverse: list
                list of urls that are allowded (ie. they lead back to targetUrl)
                Only returned if a match is not found
            isFound: bool
                True if a match is found
                False else


    """
    reverse = []
    for i in urls:
        toCheck = URL_finder(i)                
        if targetUrl in toCheck: #checks if urls in i lead back to targetUrl
            match = set(toCheck).intersection(list(toMatch))
            if match != set():
                for j in list(match):
                    if i in URL_finder(j):
                        dic = {} #assigning values to retrieve (and use) if a match is found
                        dic[j] = i 
                        dic[i] = targetUrl
                        return dic, True
            reverse.append(i) #allowed values of i
    return reverse, False


def matchToPath(match, allS, allE, start, finish):
    """
    Takes the match found, starting url, final url and all urls found
    to create a path between start and finish
    
    Arguments:
            match: list
                list of all matches found
            allS: dict
                dictionary of all urls found starting from start
            allE: dict
                dictionary of all urls found starting from finish
            start: str
                initial url
            finish: str
                final url
            
    Returns:
            path: list
                list of urls forming a poth from start to finish


    """
    #print('Success!\n')
    toStart = match[0]; toFinish = match[0]
    startList = []; finishList = []
    while toStart != start: #path from match to start
        prevS = toStart; 
        try:
            allS[toStart]  
        except:
            pass
        else:
            if toStart != start:
                toStart = allS[toStart]
                
        if prevS != toStart:
            startList.append(prevS)
            
        
        
    while toFinish != finish: #path from match to finish
        prevF = toFinish
        try:
            allE[toFinish]  
        except:
            pass
        else:
            if toFinish != finish:
                toFinish = allE[toFinish]
                
        if prevF != toFinish:
            finishList.append(prevF)
            
                    
    startList.append(toStart)
    finishList.append(toFinish)     
    startList.reverse() #list has to be reversed as elements are
    startList.extend(finishList[1:]) #remove excess match element and merge to one list
    path = startList
    return path

def pathExists(path):
    """
    Takes a wikipedia URL and returns a list with all URLs found on that page
    
    Arguments:
            path: list or array-like
                list of urls


    """
    for i in range(len(path)-1):
        urls = URL_finder(path[i])
        if path[i+1] in urls:
            continue
        else:
            raise AssertionError(f'Found impossible path,\nEntry {i} {path[i]}\ndoes not contain link to\nEntry {i+1} {path[i+1]}')

def nonParaPath(start, finish):
    """
    Non-parallelized code for finding a path from start to finish.
    Is called iff threads=1
    
    Arguments:
            start: str
                wikipedia url to start from
            finish: str
                wikipedia url to finish at
    Returns:
            path: list
                list of urls forming a path from start to finish


    """
    urlS = start
    urlE = finish
    allUrlS = {}
    allUrlE = {}
    
    fromStart = 0; fromEnd = 0
    flip = True
    isFound = False
    for itr in range(20):
        if flip == False:
            toitr = urlS
            flip = True
            fromStart += 1
        elif flip == True:
            toitr = urlE
            flip = False
            fromEnd += 1
            
        tempList = []
        
        if type(toitr) == str: #for first iteration where we only have a string
            setS = URL_finder(toitr)
            if flip==False:
                setS, isFound = isReverse(setS, toitr, allUrlS) #checks if values are allowed, as we are going from start -> finish
                if isFound == True: #                           which means any urls found from path must be reversible
                    allUrlE.update(setS)
                    break
                
            tempList.append(setS)
            if isFound == True:
                break
            else:
                if flip == False: #add to all urls if no match was found
                    for j in setS: #from finish
                        allUrlE[j] = toitr
                    urlE = allUrlE
                else:
                    for j in setS: #from start
                        allUrlS[j] = toitr
                    urlS = allUrlS
        
                
        else: #for subsequent iterations
            if flip == False:
                keys = list(allUrlE.keys())
            else:
                keys = list(allUrlS.keys())
                
            for i in list(toitr):
                setS = URL_finder(i)
                if flip==False:
                    setS, isFound = isReverse(setS, i, allUrlS)
                    if isFound == True:
                        allUrlE.update(setS)
                        break
                tempList.append(setS)
                if isFound == True:
                    break
                
                else:
                    if flip == False:
                        for j in setS:
                            if j != i:
                                if j not in keys:
                                    allUrlE[j] = i

                    else:
                        for j in setS:
                            if j != i:
                                if j not in keys:
                                    allUrlS[j] = i

                        
            if isFound == True:
                break
            
            
            if flip == False:
                urlE = allUrlE
                
            else:
                urlS = allUrlS


        match = set(allUrlS).intersection(allUrlE) #if a match is found 
        if match != set():
            match = list(match)
            path = matchToPath(match, allUrlS, allUrlE, start, finish)
            break
        
        else:
            print(f'Fail!\nFrom Start: {fromStart}\nFrom End: {fromEnd}')
            continue

    
    
    if isFound == True: #if a match is found in isReverse()
        match = list(set(allUrlS).intersection(allUrlE))
        path = matchToPath(match, allUrlS, allUrlE, start, finish)
        
    return path

def paraPath(start, finish, threads):
    """
    Parallelized code for finding a path from start to finish
    
    Arguments:
            start: str
                wikipedia url to start from
            finish: str
                wikipedia url to finish at
            threads: None or int
                number of threads to use. Uses all available threads if None
    Returns:
            path: list
                list of urls forming a path from start to finish


    """

    pool=mp.Pool(threads) #declare number of threads to use
    
    urlS = start
    urlE = finish
    allUrlS = {}
    allUrlE = {}
    
    fromStart = 0; fromEnd = 0
    flip = True
    isFound = False
    for itr in range(20):
        if flip == False:
            toitr = urlS
            flip = True
            fromStart += 1
        elif flip == True:
            toitr = urlE
            flip = False
            fromEnd += 1
            
        tempList = []
        
        if type(toitr) == str:
            setS = URL_finder(toitr)
            if flip==False:
                L = splitter(threads, setS) #split urls in setS into threads lists
                sets = [pool.apply_async(isReverse, args=(x, toitr, allUrlS)) for x in L] #parallelization
                setS = []
                for k in sets:
                    if k.get()[1] == True: #if any results found a match
                        allUrlE.update(k.get()[0])
                        isFound = True
                        setS.extend(list(k.get()[0]))
                        break
                    else:
                        setS.extend(k.get()[0])
            tempList.append(setS)
            if isFound == True:
                break
            
            else:
                if flip == False:
                    for j in setS:
                        allUrlE[j] = toitr
                    urlE = allUrlE
                else:
                    for j in setS:
                        allUrlS[j] = toitr
                    urlS = allUrlS
        
                
        else:
            if flip == False:
                keys = list(allUrlE.keys())
            else:
                keys = list(allUrlS.keys())
                
            for i in list(toitr):
                setS = URL_finder(i)
                if flip==False:
                    L = splitter(threads, setS)
                    sets = [pool.apply_async(isReverse, args=(x, i, allUrlS)) for x in L]
                    setS = []
                    for k in sets:
                        if k.get()[1] == True:
                            allUrlE.update(k.get()[0])
                            isFound = True
                            setS.extend(list(k.get()[0]))
                            break
                            
                tempList.append(setS)
                if isFound == True:
                    break
                else:
                    if flip == False:
                        for j in setS:
                            if j != i:
                                if j not in keys:
                                    allUrlE[j] = i

                    else:
                        for j in setS:
                            if j != i:
                                if j not in keys:
                                    allUrlS[j] = i

                        
            if isFound == True:
                break
            
            
            if flip == False:
                urlE = allUrlE
                
            else:
                urlS = allUrlS


        match = set(allUrlS).intersection(allUrlE)
        if match != set():
            match = list(match)
            pool.close() #close multithreading, ensures we don't run out of memory in IDEs
            path = matchToPath(match, allUrlS, allUrlE, start, finish)
            break
        
        else:
            #print(f'Fail!\nFrom Start: {fromStart}\nFrom End: {fromEnd}')
            continue

    
    
    if isFound == True:
        pool.close()
        match = list(set(allUrlS).intersection(allUrlE))
        path = matchToPath(match, allUrlS, allUrlE, start, finish)
    
    return path
        
if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Bogoliubov_transformation"
    finish = "https://en.wikipedia.org/wiki/Peace"
    #find_path(start, finish, 1) #single threaded
    #find_path(start, finish, 4) #4 threads
    #find_path(start, finish, 8) #8 threads
    find_path(start, finish) #max threads
