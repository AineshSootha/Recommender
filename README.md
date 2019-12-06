# Recommendation System

[aineshsootha.pythonanywhere.com](https://aineshsootha.pythonanywhere.com/)(live version)

# ENGR-133 Final Project

## Ainesh Sootha



This project is a **book/movie recommendation system** written in **Python** (Flask). It uses the CMU book summaries dataset for books and the Kaggle movies dataset for movies.\* The program uses Pandas (Python data analysis library) to work with the datasets. The program uses an algorithm called **&#39;cosine similarity&#39;** to find similar books to recommend. The algorithm is explained in later paragraphs.

\*The datasets are originally in csv but are converted using the csvtohdf.py file to hdf5 files since hdf5 is faster to access than csv.

**Books**

The program allows the user to enter the title of the book they have read and choose what they liked about the book. They may choose **Genre** or **Writing Style**. Each of these options prompts the program to call a different function. If the user chooses Genre, the program would return a list of books with similar genres **sorted according to the similarity of their summaries.** Similarly, if the user chooses Writing Style, the program would return a list of books from the same author **sorted according to the similarity of their summaries.**

The similarity is computed using the cosine similarity algorithm which is explained in later paragraphs.

**Movies**

The program allows the user to enter the title of the movie they have watched and choose what they liked about the movie. They may choose **Genre** , **Cast** or **Collection**. Each of these options prompts the program to call a different function. If the user chooses Genre, the program would return a list of movies with similar genres **sorted according to the similarity of their summaries**.

\*Collection refers to a franchise or series like Toy Story or Harry Potter

The similarity is computed using the cosine similarity algorithm (A ML algorithm) which is explained in later paragraphs.

**Other details**

The UI of the program is created using Flask + HTML/CSS/JS. I used flask primarily because it is very lightweight, minimalist, whereas Django is a heavy, batteries-included, full-stack framework. This would have added too many features I wouldn&#39;t need.

The design is completely responsive (designed in bootstrap) and can be used on any device (iPhone, iPad etc.)

I chose to host the project on Pythonanywhere.com since it is easier to go from development straight to production without the requirement of virtual environments and without the requirement of my laptop being present at the time of use.

The program uses the Goodreads API (for books) which generates an XML for the title, which is converted to a multi-level dictionary. This is used to get a link to the poster of the book. This is then displayed in the result page.

Similarly, the program uses the OMDb API (for movies) which generates a json for the title, which is converted to a dictionary. Then the link of the poster for the movie is obtained from this dictionary and the poster (from the link) is displayed on the result page.

If a book/movie title is entered such that it doesn&#39;t exist in the dataset(s), the user is shown an error screen and the title entered is appended to either missingbook.csv or missingmovie.csv (depending on whether user chose book or movie). This is done to create reference files for me to add new titles into the dataset.

**Cosine Similarity**

Similarity, for shorter strings, can be measured by simply counting the number of times each word appears in the string.

Eg:

Mark and Andy play with the balls.

Andy and Mark play with a ball.

If we computed the similarity of these 2 strings by counting the repeating words, they would be almost 100% similar. But, there is an inherent flaw with this method, especially when used with larger files. Since words may be repeated more frequently in a large string, the comparison using this method becomes less accurate. Thus, I used the cosine similarity method, a **Machine Learning algorithm used to compute the similarity of large strings/documents**.

This algorithm, as the name suggests, is based on the cosine of vectors.


Where A,B are 2 vectors.

Thus, cosΘ is given by


To put it simply, here the vectors are the strings to compare. The 2 strings are converted to vectors, or sets of words (dictionaries in Python, with each number representing the number of times the word is repeated)

&quot;When plotted on a multi-dimensional space, where each dimension corresponds to a word in the document, the cosine similarity captures the orientation (the angle) of the documents and not the magnitude.&quot;– (From machinelearningplus.com)

Basically, each word creates an axis in a multi dimensional space, and the vector of each string (computed using the number of times each word is repeated) can be plotted on this multi-dimensional space. If the 2 strings have vectors pointing in the same direction, it represents that these 2 strings are very similar in meaning. Thus, they have a high cosine similarity value. (Lower angle = Higher cosine).

To make it easier to understand, here is an example:

If there are 2 strings, consisting of the words &#39;books&#39; and &#39;movies&#39; only, with:

- String A having 40 repetitions of the word &#39;books&#39; and 20 repetitions of &#39;movies&#39;
- String B having 30 repetitions of the word &#39;books&#39; and 30 repetitions of &#39;movies&#39;

If we plot these on a 2D plot with one axis being &#39;books&#39; and one being &#39;movies&#39;, the graph would look like this:

It can be observed here that the angle theta is used to measure the cosine similarity of the 2 strings. Once more words are added, more axes are created and thus the accuracy of the similarity algorithm improves. For the similarity to be higher, theta is smaller, thus the cosine of the angle is closer to 1.

This is very useful in computing the similarity of books and movies because the summaries of books and movies tell us a lot about the books/movies themselves. For example, a fantasy book would have words like &quot;wizard&quot;, &quot;dragons&quot; etc, so other books with similar words (with the same meaning) would be closer (in terms of vector in the multidimensional space).

Thus, I used this method to compute similar books/ movies.



**Overview**

The program consists of 3 main files:

- Project.py
  - This is the main file, the flask app. It renders the HTML templates (index.html, result.html, error.html) as required and calls the functions findbook() and findmovie() from the books and movies modules respectively.
  - It gets the user input from index.html (from the main form), where the user chooses whether they want to enter book or movie, the title of the book/movie and finally what they liked about the book/movie. This is received using the flask request module and then the required function (findbook() or findmovie()) is called depending on the user input for the choice of book/movie.
  - It also calls findposter() for either book or movie as required.
  - It renders the error.html template if the list of books is empty (suggesting that the dataset is empty) or if the movie is not a part of any collection/series. It also calls writemissing() from missing.py if an error is encountered.
  - If no errors are encountered, it renders the result.html template and populates it with data returned from the functions.
- Books.py
  - This is the file for finding similar books.
  - The main function of the file is findbooks(), which requires the title of the main book, and it returns sorted lists of book titles,  one list with similar genres, and one with the same author as the main book.
  - It uses pandas to read the hdf5 file which contains the dataset of books (converted from csv) and find the author/genres as required and then creates a list of books with the same author/genre as required, and finally sorts the lists based on the cosine similarity of the book summaries.
  - The dataset used is the CMU book summaries dataset.
  - It also uses the goodreads API to find the poster link to the book being searched. It uses the requests module to work with the API, which returns XML data about the book. This data is converted to a dictionary using the function xmltodict() (from PyPI) and then the dict is used to locate the poster image.
- Movies.py
  - This is the file for finding similar movies
  - The main function of the file is findmovies(), which requires the title of the main movie, and it returns sorted lists of movie titles, one list with similar genres, one with similar cast, and one from the same series/collection.
  - It uses pandas to read the hdf5 file which contains the dataset of movies (converted from csv) and find the genres/cast/collection as required and then creates a list of movies with the same genres/cast/collection as required, and finally sorts the list based on the cosine similarity of the book summaries.
  - The dataset used is the Kaggle movies dataset.
  - It also uses the OMDb API to find the poster link to the movie being searched. It uses the requests module to work with the API, which returns JSON data about the book. This data is converted to a dictionary using the .json() method and then the dict is used to locate the poster image.

Other files:

- Missing.py
  - The main function of this module (writemissing()) is used to append the title of the book/movie to the appropriate file if an error is observed.
- Index.html
  - This is the main template file.
  - It contains the main form and sends the data to flask from this form using the POST method.
- Result.html
  - This is the result template file.
  - It gets the values from the Project.py file and displays the details as required.
- Error.html
  - This is the error template file.
  - It is rendered if an error is encountered. The message displayed depends on the error.
  - Possible errors are:
    - Book/Movie not present in dataset
    - Movie is not part of any collection/series
- Main.css
  - This is the css file for all the templates
- Csvtohdf.py
  - This is a file I created to convert the csv dataset files to hdf once I learned that hdf5 files are faster to access
- Datasetbooks.csv / datasetbook.h5
  - These are the CMU book datasets I am using for the books module
- Datasetmovies.csv / datasetmovies.h5
  - These are the Kaggle movie datasets I am using for the movies module
- Datasetcast.csv / datasetcast.h5
  - These are the Kaggle movie datasets I am using for finding the cast in the movies module
