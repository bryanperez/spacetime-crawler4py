import re
from urllib.parse import urlparse
from urllib.request import urlopen
import lxml.html
from bs4 import BeautifulSoup
import requests
from collections import Counter
from string import punctuation

def scraper(url, resp):
    '''
        Description:
        Logic:
        Citations:
       
    '''
    print("IN THE SCRAPER")
    # Gets the links that are found in the webpage (regardless of domain)
    links = extract_next_links(url, resp)
    for link in links:
        print(link)
        print('\n')
    #links = ["https://www.ics.uci.edu"]
    validLinks = [link for link in links if is_valid(link)]
    uniqueLinks = []
    [uniqueLinks.append(link) for link in validLinks if link not in uniqueLinks]
    #reportUniquePages(uniqueLinks)
    #countWords(uniqueLinks)
    # scraper then returns a new list of valid links from the aforementioned links list
    return uniqueLinks
    #return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    '''
         Description:
         Logic:
         Citations:
       
     '''

    #Implementation requred.
    print("IN THE EXTRACT_LINK")
    # Set because we just want unique url's
    linksFoundSet = []; 
    
    pageContent = urlopen(url)
    dom = lxml.html.fromstring(pageContent.read())
    print("URL: ", url)
    print("RESP: ", resp)
    
    for link in dom.xpath('//a/@href'):
        linksFoundSet.append(link)

    #print("LINKS FOUND ", linksFoundSet)

    return linksFoundSet
    #return list(linksFoundSet)
    #return list()

def is_valid(url):
    '''
        Description:
        Logic:
        Citations:
       
    '''

    try:
        validDomains = [".ics.uci.edu", ".cs.uci.edu", ".infomratics.uci.edu", ".stat.uci.edu", ".today.uci.edu/department/information_computer_sciences"]
  
        # Isolate the hostname to check if it is valid
        domain = url.split("www")[-1].split("/")[0]
        print("DOMAIN:", domain)
        # Remove fragment of url
        url = url.split('#')[0]
        print("URL:", url)
       
        parsed = urlparse(url)
       
        if parsed.scheme not in set(["http", "https"]) or domain not in validDomains:            
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def countWords(uniqueLinks):
    totalList = []
    for link in uniqueLinks:
        request = requests.get(link)
        soup = BeautifulSoup(request.content)
        text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

        text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
        c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
        total = c_div + c_p
        totalList.append(total)
    for total in totalList:
        print("TOTAL:", total)
        

def reportUniquePages(uniqueLinks):
    with open("reportFile.txt", 'a') as line:
        for item in uniqueLinks:
            line.write(item)
