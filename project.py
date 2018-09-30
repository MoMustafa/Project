# =============================================================================
# Mohammad Mustafa NLP Chatbot 
# =============================================================================

from bs4 import BeautifulSoup
import requests
import urllib
from urllib.request import Request
import re
import os
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import time

start_time = time.time()

parser = 'lxml'
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0'} 
omit = ['contact','advertise','privacy','policy','terms','writers','#','dmca', 'forum','news','author','our-team']
urlfile = 'urls.txt'
starter_url = "http://www.thatvideogameblog.com/news/page/"
pages = 8
important = 1

def compile_urls(webpage):
    with open(urlfile, 'a+') as f:
        for link in webpage.findAll('a'):
            url = str(link.get('href'))
            if not any(word in url for word in omit) and url.startswith('http'):
                f.write(url+'\n') 

def clean_urls():
    sites = []
    with open(urlfile, 'r') as f:
        for line in f:
            sites.append(line)
    sites = list(set(sites))
    with open('urls.txt', 'w') as f:
        for line in sites:
            f.write(line)

def read_urls():
    with open(urlfile, 'r') as f:
        for line in f:
            print("--- %s seconds ---" % (time.time() - start_time))
            req = Request(line, headers=header)
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html, parser)
            data = soup.findAll('p')
            omit = ['id','style']
            if not any(word in soup.title.string for word in ['Archives']):
                title ='Webpages\\' + re.sub('[^\w]+|\s{2,}'," ",soup.title.string)+'.txt'
                os.makedirs(os.path.dirname(title), exist_ok=True)
            with open(title, 'wb') as f:
                for x in data:
                    if not any(words in omit for words in x.parent.attrs):
                        f.write(x.get_text().encode('utf-8')) 
            if os.stat(title).st_size == 0:
                os.remove(title)

def clean_text():
    for file in os.listdir():
        with open(file, 'r', encoding='utf-8') as f, open('CLEANED '+file, 'w', encoding='utf-8') as c:
            text = f.read().lower()
            sentences = sent_tokenize(text)
            for sent in sentences:
                sent = re.sub('[\W]+|(\w*)\d+(.)',' ', sent)
                sent = re.sub('\s{1,}',' ', sent)
                c.write(sent+'\n')
                
def extractor():
    omit = stopwords.words('english')
    d = {}
    for file in os.scandir():
        if file.name.startswith('CLEANED'):
            words = []
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    for word in word_tokenize(line):
                        if word not in omit:
                            words.append(word)
            common = important * len(nltk.FreqDist(words))
            dist = nltk.FreqDist(words).most_common(int(common))
            for k,v in dist:
                d[k] = v+d[k] if k in d else v
    return d

def demo(vocab):
    top = sorted(vocab.items(), key = lambda x: x[1], reverse=True)
    print('Top 40 Dictionary Terms')
    for i in range(0,80):
            print("%-15s: %i" %(top[i][0],top[i][1]))
    
    terms=['game','gaming','experience','series','available','story', 'play', 'new', 'character','display'] 
    print('\nManually selected Top 10 Terms')
    for term in terms:
        print(term)
        
def main():
    for i in range(1,pages):
        url = starter_url + str(i)
        r = requests.get(url)
        data = r.text
        page = BeautifulSoup(data, parser)
        compile_urls(page)
    clean_urls()
    read_urls()
    os.chdir('Webpages')
    clean_text()
    vocab = extractor()
    demo(vocab)
    
    
    
    
if __name__ == '__main__':    
    main()    