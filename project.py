# =============================================================================
# Project - NLP Chatbot Phase I
# Mohammad Mustafa
# msm151030
# 
# DOCUMENTATION
# 
# main()
#     Uses the Beautiful Soup library to read several pages (determined by the
#     'pages' variable) starting from the assigned starter_url.
#     For each webpage, calles the compile_urls() function
#     Then clean_urls() is called to remove duplicate links.
#     Then read_urls() is called to go through the list of retrieved webpage links
#     and reads and documents them. 
#     Then the clean_text() method removes numerals, special characters, 
#     newlines etc. from the files and writes a new file.
#     The extractor() method is then called and returns a dictonary of the 
#     vocabulary extracted from the knowledge base of cleaned files.
#     
# compile_urls()
#     Opens/creates the designated file for storing retrieved urls and reads
#     through each html document and writes the urls contained within the 
#     anchor tags.
#     
# clean_urls()
#     reads the list of urls and appends the url to a list. By converting the
#     list to a set and then back to a list removes any duplicates and the 
#     new list is overwrritten on the .txt file of urls
#     
# read_urls()
#     Opens each url in the .txt file of urls. Reads the text contained within
#     the paragraph tags of the html document and a new .txt file is written 
#     for each webpage containing the text read from that webpage. Text is only
#     written to a new file if it does not fall under any of the omitted
#     catagories. If the new .txt file is empty, it is deleted.
#     
# clean_text()
#     Opens each of the files written by read_urls() reads the text and 
#     lowercases it. Then it tokenizes the lines using the sent_tokenize nltk 
#     method. Numerals, special characters, newlines and extra whitespaces are 
#     removed from the sentences using Regular Expressions. The cleaned up 
#     sentences are written to a new file with the 'CLEANED' suffix in its title  
# 
# extractor()
#     For each 'CLEANED' file in the knowledge base directory, it reads each 
#     line and word_tokenizes it. If the word is not a stopword, it is appended 
#     to a list. After reading all the files, the FreqDist() nltk function 
#     generates a frequency distribution of all the words. 
#     What percentage of the common words are included in the distribution is
#     determined by the 'important' variable. 
#     A dictionary is created from the frequency distribution and returned.
#     
# demo()
#     takes the 'vocab' dictionary returned by the extractor() from main and
#     sorts it by word frequency. It then prints the top 40 words in the
#     dictionary to the console. Then it prints my handpicked list of 10 terms.
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

parser = 'lxml'
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0'} 
omit = ['contact','advertise','privacy','policy','terms','writers','#','dmca', 'forum','news','author','our-team']

urlfile = 'urls.txt'
starter_url = "http://www.thatvideogameblog.com/news/page/"

pages = 2
important = 1

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
            for key,value in dist:
                d[key] = value+d[key] if key in d else value
    return d

def demo(vocab):
    top = sorted(vocab.items(), key = lambda x: x[1], reverse=True)
    print('Top 40 Dictionary Terms')
    for i in range(0,40):
            print("%-15s: %i" %(top[i][0],top[i][1]))
    
    terms=['game','gaming','experience','series','available','story', 'play', 'new', 'character','display'] 
    print('\nManually selected Top 10 Terms')
    for term in terms:
        print(term)
    
if __name__ == '__main__':    
    main()    