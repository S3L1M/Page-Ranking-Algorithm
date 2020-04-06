from numpy import sin, cos, deg2rad
from bs4 import BeautifulSoup
import requests
import html2text
from nltk.tokenize import word_tokenize
from nltk import FreqDist

def rank(query, linksWithKey, keywords, updateFreq, lastModified, nonWorkingLinks, pageAge,
         domainAge, loadTime):
    """returns a rank value relative for each query"""
    rank=0
    rank += len(linksWithKey)

    for q in query:
        if q in keywords.keys():
            rank += 2 * sin(deg2rad(keywords[q]))
    
    rank += cos(deg2rad(updateFreq))
    rank += cos(deg2rad(lastModified))
    rank /= nonWorkingLinks+1
    rank += sin(deg2rad(pageAge/365))
    rank += sin(deg2rad(domainAge/365))
    rank += cos(deg2rad(loadTime))
    
    return rank


query = input().split(' ')

websites = ['https://www.souq.com/eg-en',
            'https://www.noon.com/egypt-en',
            'https://www.jumia.com/',
            'https://www.ebay.com/',
            'https://www.aliexpress.com/']

ranks = []

for url in websites:
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
        
    for X in query:
        X_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs and 
                               X in tag.get_text().lower())
        linksWithKey = soup.find_all(X_links)
    
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    txt = h.handle(r.text).replace(',', '').replace("'", '')
    words = word_tokenize(txt)
    keywords = FreqDist(words)
    lastModified = r.headers['last_modified'] if 'last_modified' in r.headers.keys() else 0
    pageAge = r.headers['Age'] if 'last_modified' in r.headers.keys() else 0
    
    ranks.append(rank(query, linksWithKey, keywords, 7, lastModified, 0, pageAge, 0, 0.5))

print('\n\n\n\n')
print(websites)
print(ranks)
print('\n\n')
print(websites[ranks.index(max(ranks))])
