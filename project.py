from bs4 import BeautifulSoup
import requests
import urllib
from urllib.request import Request, urlopen
import re
import os
import errno
import nltk
import string
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from unicodedata import normalize
import time

start_time = time.time()

parser = 'lxml'
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0'}      

def compile_urls(fname, webpage):
    print('in compile')
    omit = ['contact','advertise','privacy','policy','terms','writers','#',
            'dmca', 'forum','news','author','our-team']
    with open(fname, 'a+') as f:
        for link in webpage.findAll('a'):
            url = str(link.get('href'))
            if not any(word in url for word in omit) and url.startswith('http'):
                    f.write(url+'\n')          

def update_urls():
    print('in update')
    with open('urls.txt') as f:
        lines = list(set(f.read().split('\n')))
        if '' in lines:
            lines.remove('')
        for url in lines:
            req = Request(url, headers=header)
            html = urllib.request.urlopen(req)
            page = BeautifulSoup(html, parser)
            data = page.findAll('p')
            if any(word in page.title.string for word in ['Archives']):
                compile_urls('urls.txt', page)        
                 
def read_url():
    print('in read')
    with open('urls.txt') as f:
        lines = list(set(f.read().split('\n')))
        if '' in lines:
            lines.remove('')
    for url in lines:
        req = Request(url, headers=header)
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, parser)
        data = soup.findAll('p')
        omit = ['id','style']
        if not any(word in soup.title.string for word in ['Archives']):
            title ='Webpages\\' + re.sub('[/*\.\\\[,:;\]\|=?<>|]|\s{2,}'," ",soup.title.string)+'.txt'
            os.makedirs(os.path.dirname(title), exist_ok=True)
            with open(title, 'wb') as f:
                for x in data:
                    if not any(words in omit for words in x.parent.attrs):
                        f.write(x.get_text().encode('utf-8'))                 
                        
def cleanup_text():
    print('in cleanup')
    omit = stopwords.words('english')+list(string.punctuation)
    for file in os.listdir():
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
            for x in [".",',',':']:
                    text = text.replace(x, ' ')
        sentences = sent_tokenize(text)
        with open('CLEANED '+file, 'w', encoding='utf-8') as f:
            for sent in sentences:
                sent = sent.lower()
                words = word_tokenize(sent)
                for word in words:
                    if word.isalpha() and not word in omit:
                        f.write(word +' ')
            
def extractor():
    print('in extractor')
    for file in os.listdir():
        if file.startswith('CLEANED '):
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                words = word_tokenize(text)
            print('\n'+file[8:])    
            print(nltk.FreqDist(words).most_common(15))
                
def main():
    print('in main')
    starter_url = "http://www.thatvideogameblog.com/news/page/"
    for i in range(1,11):
        url = starter_url + str(i)
        r = requests.get(url)
        data = r.text
        page = BeautifulSoup(data, parser)
        compile_urls('urls.txt', page)
    print("\n--- %s seconds ---" % (time.time() - start_time))
    #update_urls()
    print("\n--- %s seconds ---" % (time.time() - start_time))
    read_url()
    print("\n--- %s seconds ---" % (time.time() - start_time))
    os.chdir('Webpages')
    cleanup_text()
    print("\n--- %s seconds ---" % (time.time() - start_time))
    extractor()
    print("\n--- %s seconds ---" % (time.time() - start_time))
               
if __name__ == '__main__':    
    main()