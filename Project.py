'''
===============================================================================
ENGR 133 Program Description 
	This is the main project file, ie-the flask app. It renders the HTML templates 
    and displays the GUI that is seen by the user.

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

from flask import Flask, render_template,request
import books
import movies
import missing
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

#This allows flask to receive information from the form and display appropriate info on the results page
@app.route('/result',methods = ['POST', 'GET'])
#This is the main function to call the books module or the movies module
def result():
    titleMain=request.form['title']
    valueOption=request.form['options']
    selectOption=request.form['bmselect']
    #If the user selects books. get the lists using the title
    if(valueOption=="book"):
        #If user selects genre, make listgenre the mainlist
        if selectOption=="genre":
            listsecondary,listmain=books.findbook(titleMain)
        #Else make the other list the main list
        else:
            listmain,listsecondary=books.findbook(titleMain)
        author=books.findAuthor(titleMain)
        for i in author:
            author=i
        #If list does not exist, display error screen
        if not listmain:
            missing.writemissing(titleMain,'book')
            return render_template("error.html",error="list",option=valueOption)
        #Otherwise, display the result screen and find the poster of the book
        else:
            posterlink=books.findPoster(titleMain,author)
            return render_template("result.html", titleMain=titleMain, listmain=listmain,listsecondary=listsecondary,valueOption=valueOption,posterlink=posterlink)
    #The same as above for movies
    else:
        if selectOption=="genre":
            listmain,listsecondary,listtertiary=movies.findMovies(titleMain)
        elif selectOption=="cast":
            listsecondary,listmain,listtertiary=movies.findMovies(titleMain)
        elif selectOption=="collection":
            listsecondary,listtertiary,listmain=movies.findMovies(titleMain)
            if listmain==None:
                return render_template("error.html",error="collection",option=valueOption, selectOption=selectOption)
        
        if not listmain:
            missing.writemissing(titleMain,'movie')
            return render_template("error.html",error="list",option=valueOption, selectOption=selectOption)
        else:
            posterlink=movies.findPoster(titleMain)
            return render_template("result.html", titleMain=titleMain, listmain=listmain,listsecondary=listsecondary,valueOption=valueOption,posterlink=posterlink)
   

          
if __name__ == "__main__":
    app.run(debug=True)

'''
===============================================================================
ACADEMIC INTEGRITY STATEMENT
    I have not used source code obtained from any other unauthorized
    source, either modified or unmodified. Neither have I provided
    access to my code to another. The project I am submitting
    is my own original work.
===============================================================================
'''