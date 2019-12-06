'''
===============================================================================
ENGR 133 Program Description 
	This is the file that finds the book titles similar to the title entered based on the option picked.
    It then computes the cosine similarity and sorts the list of titles according to the similarity.

Assignment Information
	Assignment:     Final Project
	Author:         Ainesh Sootha, asootha@purdue.edu
	Team ID:        001-14
	
Contributor:    
   
	My contributor(s) helped me:	
	[ ] understand the assignment expectations without
		telling me how they will approach it.
	[ ] understand different ways to think about a solution
		without helping me plan my solution.
	[ ] think through the meaning of a specific error or
		bug present in my code without looking at my code.
	Note that if you helped somebody else with their code, you
	have to list that person as a contributor here as well.
===============================================================================
'''


import pandas as pd
import numpy as np
import re, math
from collections import Counter
import requests
import xmltodict

#This reads the hdf5 file (dataset) as a pandas dataframe. I am using hdf5 instead of csv because it is faster to access
data1 = pd.read_hdf("datasetBooks.h5")
#This basically breaks lines into words (excluding symbols, numerals etc)
WORD = re.compile(r'\w+')
#This function computes the cosine similarity for 2 vectors
#It requires 2 arguments (2 vectors computed using text_to_vector())
def get_cosine(vec1, vec2):
    #This finds similarity for each word and creates a list
     intersection = set(vec1.keys()) & set(vec2.keys())
     #The rest of this function basically computes the "dot product" of the 2 vectors and divides it with the magnitude of the list
     numerator = sum([vec1[x] * vec2[x] for x in intersection])
     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)
     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator
        
#This function converts the string(text) to vectors (Dictionary of all words with their respective count)
def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)
#This function finds the author of the book from the dataset
#It requires the title of the book as a parameter
def findAuthor(title):
    #This creates a pandas series with all the rows with the same title as the parameter
    rows = data1[data1['title'] == title.lower()]
    #This then matches the author column of the title and stores the author as a list into author
    author = list(rows['Author'].values)
    #Finally the author(list) is returned
    return author

#This fuction finds the list of genres of the book from the dataset
#It requires the title of the book as a parameter
def findGenre(title):
    #This creates a pandas series with all the rows with the same title as the parameter
    rows = data1[data1['title'] == title.lower()]
     #This then matches the author column of the title and stores the genres as a list into genrelist
    genreset = list(rows['Genre'].values)
    l=[]
    linit=[]
    #Since in the dataset, the genres are separated using ", this loop is checks if the list is empty, if not, it separates the strings
    for i in genreset:
        if(str(i).lower()=='nan'):
            return None
        linit=i.split('"')
    #Finally, each genre is appended to the final list (l) after being checked for random values that may occur
    for i in linit:
        if(':' not in i and '/m/' not in i and ',' not in i):
            l.append(i)       
    l=list(filter(None,l))
    return l

#This function finds books with the same genre(s) as the book that is entered. It returns a sorted list of titles(based on cosine similarity)
#It requires 2 arguments, the list of genre(s) of the book and the title of the book
def findBooksGenre(genrelist,title):
    #This creates a pandas series from all the genres in the list
    for i in genrelist:
        rows=(data1[data1['Genre'].str.contains(i,na=False)])
    l=[]
    #This creates a list of 0s (same number of 0s as rows from the series)
    for index,i in rows.iterrows():
        l.append(0)
        for j in genrelist:
            #This conditional adds 1 for every genre matched in the list of genres from the book and the series created
            if(j in i['Genre']):
                l[-1]=l[-1]+1
    titleset=[]
    summaryset=[]
    j=-1
    #This iterates through the rows and creates 2 new lists (titles and summaries)
    for index,i in rows.iterrows():
        j=j+1
        #This conditional checks if the number of genres matching the main book is close to the maximum in the list
        if(l[j]>0 and (l[j]==max(l) or l[j]==max(l)-1)):
            titleset.append(i['title'])
            summaryset.append(i['Summary'])
    #Here I created the mainrow which contains all the values of the main book from the dataset
    mainrow=(data1[data1['title'].str.contains(title.lower(),na=False)])
    summary=mainrow['Summary'].values
    for i in summary:
        summary=i
    #This converts the summary of the book into a vector
    v1=text_to_vector(summary)
    cosinelist=[]
    #This loop computes the cosine similarity of the summaries and the summary of the main book
    for i in summaryset:
        v2= text_to_vector(i)
        cosinelist.append(get_cosine(v1,v2))
    maintitles=[]
    #This creates a sorted list of titles using the cosine similarities(minimum to maximum similarity)
    maintitles=[x for y,x in sorted(zip(cosinelist,titleset))]  
    #Since the most similar summary would be itself, the last(maximum) similar title is popped from the list and the list is returned.    
    maintitles.pop(-1)
    return maintitles
#This function finds the books with the same author and returns the list of titles, sorted from least similar book to most similar book.
#It requires the name of the author and the title of the book
def findBooksAuthor(author,title):
    #This creates a pandas series of all rows with matching authors to the main book
    rows=data1[data1['Author']==str(author)]
    #This creates a list of titles from the pandas series
    titleset = list(rows['title'].values)
    #This removes the title if the title matches the title of the main book
    for i in range(0,len(titleset)):
        if(str(titleset[i])==title.lower()):
            titleset.pop(i)
            break
    
    summaryset=[]
    #This loop creates a list of summaries of all books from the titleset
    for index,i in rows.iterrows():
        summaryset.append(i['Summary'])
    #This is the row of the main book
    mainrow=(data1[data1['title'].str.contains(title.lower(),na=False)])
    summary=mainrow['Summary'].values
    for i in summary:
        summary=i
    #This converts the summary of the main book to a vector
    v1=text_to_vector(summary)
    cosinelist=[]
    #This computes the cosine similarity of each book with the main book summary
    for i in summaryset:
        v2= text_to_vector(i)
        cosinelist.append(get_cosine(v1,v2))
    maintitles=[]
    #This creates a list of titles sorted using the list of cosine similarities
    maintitles=[x for y,x in sorted(zip(cosinelist,titleset))]       
   
    return maintitles

#This is the main function of this file, it calls all the required functions and returns the final lists
#It requires the title of the main book
def findbook(title):
    #This finds the author of the book using the findAuthor() function
    author = findAuthor(title)
    #If the author is not found, it is because the book doesn't exist in the dataset. Thus the function returns None,None, so that the error can be handled
    if(not author):
        return None,None
    #This creates a list of genres for the book
    genrelist = findGenre(title)
    #Some books are missing genres in the dataset. Thus, the function returns None,None to handle the error
    if not genrelist:
        return None,None
    #Since Novel is a very common 'genre', I deleted Novel from the genrelist to find more efficient results
    for i in range(0,len(genrelist)):
        if('Novel' in genrelist[i]):
            genrelist.pop(i)
            break
    #This rechecks if the genrelist doesn't have elements. If so, it returns None,None to handle the error
    if not genrelist:
        return None,None
    #Finally, the sorted list of books with same genre is created
    titlesFromGenre = findBooksGenre(genrelist,title)
    if(len(author)>1):
        author=author[0]
    else:
        for i in author:
            author=i
    #This finds the books with the same author
    titlesFromAuthor = findBooksAuthor(author,title)
    finallistGenre=[]
    finallistAuthor=[]
    maxn=5
    maxn2=5
    #Since I don't want to display more than 5 books, this limits the number in the list to 5 or total (whichever is less)
    if len(titlesFromGenre)<5:
        maxn=len(titlesFromGenre)
    if len(titlesFromAuthor)<5:
        maxn2=len(titlesFromAuthor)

    for i in range(0,maxn):
        finallistGenre.append(titlesFromGenre[i-1])
    for i in range(0,maxn2):
        finallistAuthor.append(titlesFromAuthor[i-1])
    return finallistAuthor,finallistGenre


#This function uses the Goodreads API to return a link to the poster of the book
#It requires the author and the title
def findPoster(title,author):
    #First, the title is modified to work with the API
    title_edited=title.replace(' ','+')
    author_edited=author.replace(' ','')
    #Using the requests module, the goodreads API returns an XML file with all the data required
    r=requests.get(f"https://www.goodreads.com/search/index.xml?key=ToxHhDKy3FxFWYdcRmhUg&q={title_edited}")
    #This converts the xml to a readable dict which can be parsed to find the required data
    books = xmltodict.parse(r.content)
    #This loop finds the required book from the API dict and then returns the posterlink
    for i in books['GoodreadsResponse']['search']['results']['work']:
        x= i['best_book']['author']['name'].lower()
        x=x.replace(' ','')      
        if(x==author_edited.lower()):
            return i['best_book']['image_url']

'''
===============================================================================
ACADEMIC INTEGRITY STATEMENT
    I have not used source code obtained from any other unauthorized
    source, either modified or unmodified. Neither have I provided
    access to my code to another. The project I am submitting
    is my own original work.
===============================================================================
'''            