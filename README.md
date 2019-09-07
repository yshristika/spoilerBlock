# SpoilerBlock extension
The function of this Chrome extension is to block any content of the movie or show.  This extension removes all mentions of your favorite show/movie from any webpage loaded in your browser. It takes the title of a show/movie from the user and itself generates the keywords representing that show and blocks any content which have those keywords. 

## Work Done until now
- Created an extension with static keywords to find a movie/show and block the content of it. 
  - manifest.json
  - startup.js
  - blockSpoiler.js
- Created a python script to 
  - find a  wikipedia page of the show/movie given by the user using a Wikipedia API. 
  - Clean the data
  - Run TF-IDF to find the important keywords in the web page.
  - Sort the words according to their TF-IDF.
  - Return top 10 words.
- Created a web server using Flask. Web server will run the python script whenever called.
  - getData.py
- Launched Flask application on EC2 instance - 
  - Creating an AWS EC2 instance under the free tier
  - Deploying demon process(flask application) on EC2 instance

## Work to be done 
- Use API call in javascript code to connect connect the user to the webserver.
- Create an html pop-up on clicking the extension which will take the input from user.

## Installation
- Download the files.
- Click on 
chrome://extensions/
- Enable the Developer Mode on the right top corner and click on Load unpacked on left hand corner.
- Select the downloaded folder and click OK.
- An extension will be added.

## Project make use of - 
- Wikipedia API
- Flask to create web server
- Python for NLP processing
- Javascript for creating extension
- HTML for the pop-up on clicking the extension button.
