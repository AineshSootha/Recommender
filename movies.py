'''
===============================================================================
ENGR 133 Program Description 
	This is the file that finds the movie titles similar to the title entered based on the option picked.
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
from operator import add
import re, math
from collections import Counter
import requests
from PIL import Image
import io
import urllib.request
import functools

#This reads the hdf5 files (datasets) as pandas dataframe. I am using hdf5 instead of csv because it is faster to access
data1 = pd.read_hdf("datasetmovies.h5", usecols=['original_title','genres','overview','belongs_to_collection'])
datacast=pd.read_hdf("datasetcast.h5", usecols=['cast'])

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
 
#This fuction finds the list of genres of the movie from the dataset
#It requires the title of the movie as a parameter
def findGenre(title):
    #This creates a pandas series with all the rows with the same title as the parameter
    rows = data1[data1['original_title'].str.lower() == title.lower()]
    #This then matches the author column of the title and stores the genres as a list into genrelist
    genreset = rows['genres'].values
    #The list is modified as a string to create a list of genres
    genreset=str(genreset)
    genreset=genreset.strip('[')
    genreset=genreset.strip(']')
    genreset=genreset.strip('\"')

    genreset=genreset.strip('[')
    genreset=genreset.strip(']')
    genreset=genreset.strip('{')
    genreset=genreset.strip('}')
    genreset=genreset.split('}, {')
    for i in range(0,len(genreset)):
        if genreset[i]=='':
            genreset.pop(i)
        
    return genreset


#This function finds the list of collections for the movie from the dataset
#It requires the title of the movie as a parameter
def findCollection(title):
    #This creates a pandas series with all the rows with the same title as the parameter
    rows = data1[data1['original_title'].str.lower() == title.lower()]
    #This then matches the author column of the title and stores the author as a list into author
    collectionSet = list(rows['belongs_to_collection'].values)
    #Clean the list of any 'nan' values
    cleanedList = [x for x in collectionSet if str(x) != 'nan']
    #If the list is empty, return None as error
    if not cleanedList:
        return None
    #Modify list to make it easier to use
    for i in collectionSet:
        collectionSet=i
    collectionSet=str(collectionSet)
    collectionSet=collectionSet.strip('{')
    collectionSet=collectionSet.strip('}')
    collectionSet=collectionSet.split(', ')
    for i in range(0,len(collectionSet)):
        if("name" in collectionSet[i]):
            mainCollection=collectionSet[i]
    return mainCollection


#This function finds the cast of the movie from the 2 datasets
#It requires the title of the movie
def findCast(title):
    #Since the datasets have matching indices (First movie in main dataset -> First movie in Cast dataset)
    #Get the value of the index of the title from the main pandas dataframe
    index=data1.loc[data1['original_title'].str.lower()==title.lower()].index[0]
    #Locate the same index in the cast dataframe
    rows=datacast.iloc[index,0]
    #Modify the string to remove unneeded characters
    rows=rows.strip('[')
    rows=rows.strip(']')
    rows=rows.split(', ')
    l=[]
    #Create and return list of cast
    for i in rows:
        if("name" in i):
            l.append(i)
    return l


#This function finds the list of genres of the movie from the dataset
#It requires the list of genres and the title of the movie as parameters
def findMoviesGenre(genrelist,title):
    #Find the rows containing any genre from the list
    for i in genrelist:
        rows=(data1[data1['genres'].str.contains(i,na=False)])
    l=[]
    #Iterate through the pandas series and create a list of 0s
    #Then 1 is added for every matching genre
    for index,i in rows.iterrows():
        l.append(0)
        for j in genrelist:
            if(j in i['genres']):
                l[-1]=l[-1]+1
    titleset=[]
    summaryset=[]
    j=-1
    #Save only the titles with max number of genres matching the main movie (or close to the max)
    #Create a list of titles and summaries to these books
    for index,i in rows.iterrows():
        j=j+1
        if(l[j]>0 and (l[j]==max(l) or l[j]==max(l)-1)):
            titleset.append(i['original_title'])
            summaryset.append(i['overview'])
    #This creates a pandas row for the main movie with all the details from the dataframe
    mainrow=(data1[data1['original_title'].str.lower()==title.lower()])
    summary=mainrow['overview']
   
    for i in summary:
        summary=i
    #This converts the summary to 'vectors'
    v1=text_to_vector(summary)
    cosinelist=[]
    #This computes the cosine similarity of the summaries to the main summary
    for i in summaryset:
        v2= text_to_vector(str(i))
        cosinelist.append(get_cosine(v1,v2))
    maintitles=[]
    finaltitles=[]
    #This creates a SORTED list of the titles based on the cosine similarities
    maintitles=[x for y,x in sorted(zip(cosinelist,titleset))]       
    #Since the most similar sumamry would be the main movie itself, the last(max similarity) movie title is deleted from the list
    maintitles.pop(-1)
    #The last 10 titles are returned as a list (10 Most similar)
    for i in range(len(maintitles)-10,len(maintitles)):
        finaltitles.append(maintitles[i])
    return finaltitles

#This finds the movies with same cast members as the movie entered
#It requires the castlist and the title of the main movie as parameters
def findMoviesCast(castlist,title):
    indexlist=[]
    for i in range(0,5):
        #Find all rows with the same cast members (top 5) and save the indices of the rows as a list
        rows = datacast.index[datacast['cast'].str.contains(castlist[i])].tolist()
        #Append the list to indexlist
        indexlist.append(rows)
    #Since the 'rows' created would be multi dimensional, reduce() reduces the list to a single dimension
    indexlist=functools.reduce(add ,indexlist)
    
    #Remove any repeated elements by converting the list to a set and the back to a list
    indexlist=list(set(indexlist))
    titleset=[]
    l=[]
    summaryset=[]
    #Locate all the rows with indices from the indexlist
    row=data1.iloc[indexlist]
    #Create a list of titles and summaries from the rows
    titleset=list(row['original_title'])
    summaryset=list(row['overview'])
    #Get the data for the main title
    mainrow=(data1[data1['original_title'].str.lower()==title.lower()])
    #Get the summary of the main title
    summary=mainrow['overview']
    for i in summary:
        summary=i
    #Convert the summary to a 'vector'
    v1=text_to_vector(summary)
    cosinelist=[]
    #Compute the cosine similarirty for each summary to the main summary
    for i in summaryset:
        v2= text_to_vector(str(i))
        cosinelist.append(get_cosine(v1,v2))
    maintitles=[]
    #This creates a SORTED list of titles using the cosine similarities (min to max similarity)
    maintitles=[x for y,x in sorted(zip(cosinelist,titleset))]       
    #Since the most similar summary is of itself, the last (most similar summary) title is deleted
    maintitles.pop(-1)
    #6 titles are returned (6 most similar summaries)
    return maintitles[-6:]
    
#This function usins the OMDb API and returns the link to the poster of a movie
#It requires the title of the movie
def findPoster(title):
    #This uses the requests module to get the JSON data from the OMDb API
    detailsList = requests.get(url=f'http://www.omdbapi.com/?apikey={}={title}')
    data=detailsList.json()
    #The JSON data is converted to a dict and the the poster link is returned
    posterlink=data['Poster']
    return posterlink

#This function finds movies from the same collection as the main movie
#It requires the collection and the title of the main movie as parameters
def findMoviesCollection(collectionlist,title):
    #All rows that contain movies from the same collection are stored as a pandas series
    rows=(data1[data1['belongs_to_collection'].str.contains(collectionlist,na=False)])
    l=[]
    #Iterate through the pandas series and create a list of 0s
    #Then 1 is added for every matching collection
    for index,i in rows.iterrows():
        l.append(0)
        for j in collectionlist:
            if(j in i['belongs_to_collection']):
                l[-1]=l[-1]+1
    titleset=[]
    summaryset=[]
    j=-1
    #The rest of the function is similar to other functions
    for index,i in rows.iterrows():
        j=j+1
        if(l[j]>0 and (l[j]==max(l) or l[j]==max(l)-1)):
            titleset.append(i['original_title'])
            summaryset.append(i['overview'])
    mainrow=(data1[data1['original_title'].str.lower()==title.lower()])
    summary=mainrow['overview']
   
    for i in summary:
        summary=i
    v1=text_to_vector(summary)
    cosinelist=[]
    for i in summaryset:
        v2= text_to_vector(str(i))
        cosinelist.append(get_cosine(v1,v2))
    maintitles=[]
    maintitles=[x for y,x in sorted(zip(cosinelist,titleset))]       
    maintitles.pop(-1)
    return maintitles

#This is the main function of the file. It calls the other functions and returns the required lists
#It requires the title of the movie as a parameter
def findMovies(title):
    #Store genres in list
    genrelist=findGenre(title)
    #If genrelist is empty, return None,None,None (Error)
    if not genrelist:
        return None,None,None
    #Find castlis and store as list
    castlist=findCast(title)
    #Store collection of the movie(If exists (else empty))
    collectionlist=findCollection(title)
    #Get a sorted list of titles with same genres and similar summaries
    moviesByGenre=findMoviesGenre(genrelist,title)
    #Get a sorted list of titles with same actor(s) and similar summaries
    moviesByCast=findMoviesCast(castlist,title)
    #If collectionlist is empty, store none to return
    #Else, find movies from same collection
    if not collectionlist:
        moviesByCollection=None
    else:
        moviesByCollection=findMoviesCollection(collectionlist,title)
    return moviesByGenre,moviesByCast,moviesByCollection

'''
===============================================================================
ACADEMIC INTEGRITY STATEMENT
    I have not used source code obtained from any other unauthorized
    source, either modified or unmodified. Neither have I provided
    access to my code to another. The project I am submitting
    is my own original work.
===============================================================================
'''
