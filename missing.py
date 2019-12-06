'''
===============================================================================
ENGR 133 Program Description 
	This file appends the missing titles to the appropriate file 
    (missingmovie.csv or missingbook.csv)

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


def writemissing(title,bm):
    if(bm=='movie'):
        with open('missingmovie.csv','a') as f:
            f.write(title)
    else:
        with open('missingbook.csv','a') as f:
            f.write(title)

'''
===============================================================================
ACADEMIC INTEGRITY STATEMENT
    I have not used source code obtained from any other unauthorized
    source, either modified or unmodified. Neither have I provided
    access to my code to another. The project I am submitting
    is my own original work.
===============================================================================
'''        