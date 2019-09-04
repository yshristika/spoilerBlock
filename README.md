# SpoilerBlock extension
The function of this Chrome extension is to block any content of the movie or show.  This extension removes all mentions of your favorite show/movie from any webpage loaded in your browser.
## Work Done until now
- Created an extension with static keywords to find a movie or a show and block the content of it. 
- Created a python script to 
  - find a  wikipedia page of the show/movie given by the user using a Wikipedia API. 
  - Clean the data
  - Run TF-IDF to find the important keywords in the web page.
  - Sort the words according to their TF-IDF.
  - Return top 10 words.
- Created a web server using Flask. Web server will run the python script whenever called.

## Work to be done 
- Run the webserver when user clicks on the extension. 
- Write ajax code to connect the javascript to call the webserver.

## Installation
- Download the files.
- Click on 
chrome://extensions/
- Enable the Developer Mode on the right top corner and click on Load unpacked on left hand corner.
- Select the downloaded folder and click OK.
- An extension will be added.

### Project make use of - 
- Wikipedia API
- Flask to create web srver
- Python for NLP processing
- Javascript for creating extension
