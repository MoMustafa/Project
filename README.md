Project - NLP Chatbot Phase I
Mohammad Mustafa
msm151030

DOCUMENTATION

main()
    Uses the Beautiful Soup library to read several pages (determined by the
    'pages' variable) starting from the assigned starter_url.
    For each webpage, calles the compile_urls() function
    Then clean_urls() is called to remove duplicate links.
    Then read_urls() is called to go through the list of retrieved webpage links
    and reads and documents them. 
    Then the clean_text() method removes numerals, special characters, 
    newlines etc. from the files and writes a new file.
    The extractor() method is then called and returns a dictonary of the 
    vocabulary extracted from the knowledge base of cleaned files.
    
compile_urls()
    Opens/creates the designated file for storing retrieved urls and reads
    through each html document and writes the urls contained within the 
    anchor tags.
    
clean_urls()
    reads the list of urls and appends the url to a list. By converting the
    list to a set and then back to a list removes any duplicates and the 
    new list is overwrritten on the .txt file of urls
    
read_urls()
    Opens each url in the .txt file of urls. Reads the text contained within
    the paragraph tags of the html document and a new .txt file is written 
    for each webpage containing the text read from that webpage. Text is only
    written to a new file if it does not fall under any of the omitted
    catagories. If the new .txt file is empty, it is deleted.
    
clean_text()
    Opens each of the files written by read_urls() reads the text and 
    lowercases it. Then it tokenizes the lines using the sent_tokenize nltk 
    method. Numerals, special characters, newlines and extra whitespaces are 
    removed from the sentences using Regular Expressions. The cleaned up 
    sentences are written to a new file with the 'CLEANED' suffix in its title  

extractor()
    For each 'CLEANED' file in the knowledge base directory, it reads each 
    line and word_tokenizes it. If the word is not a stopword, it is appended 
    to a list. After reading all the files, the FreqDist() nltk function 
    generates a frequency distribution of all the words. 
    What percentage of the common words are included in the distribution is
    determined by the 'important' variable. 
    A dictionary is created from the frequency distribution and returned.
    
demo()
    takes the 'vocab' dictionary returned by the extractor() from main and
    sorts it by word frequency. It then prints the top 40 words in the
    dictionary to the console. Then it prints my handpicked list of 10 terms.