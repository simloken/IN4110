import re
from urllib.parse import urljoin
from requesting_urls import get_html

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)
    
    html = get_html(html)
    
    # src finds the text between quotes of the `src` attribute
    

    #isolate such that we only get urls within the body of the given article
    bodyString = re.search(r'<div id=\"bodyContent\" class=\"vector-body\">(.*)<\/div>', html, flags = re.S | re.I) #worked out in https://regex101.com/r/W76Pgf/1
    html = bodyString.group(1)
        
    a_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    href_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    href_set = set()
    for a in a_pat.findall(html):
        match = href_pat.search(a)
        if match:
            href_set.add(match.group(1))
    
    urls = href_set
    # 1. find all the anchor tags, then
    # 2. find the urls href attributes

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        f = open(f'{output}'+'.txt', 'w', encoding="utf-8")
        for i in urls:
            f.write(f'{i} \n')
        f.close()
        return

    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    
    base = html.split('/wiki/')[0]
    
    
    
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
    
    for i in toremove:
        urls.remove(i)
        
        
    articles = set()
    for i in urls:
        articles.add(f'{base}'+f'{i}')

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        f = open(f'{output}'+'.txt', 'w', encoding="utf-8")
        for i in articles:
            f.write(f'{i} \n')
        f.close()
        return
    
    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    
    html = get_html(html)
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
