#                                              Uni Buddy

## Description: 
The student helper website serves two purposes:
  1. Users can solve math problems like simple arithematic calculation, linear equations
     with 2 unknown variables, finding roots of a quadratic equation
  2. Users can communicate with other users that are registered in the database by
     sending messages with a subject (like a e-mailing system)

## How to Run
Run the following commands in the folder containing the project (Windows powershell) :
-> pip install -r requirements.txt
-> $env:FLASK_APP="application.py"
-> flask run

Then open the link provided in a web browser, and voila !

## Specifications:
-> Flask, Python and sql languages are used. HTML and CSS for frontend.
-> application.py contains the main code describing all functions for app routes and helps.py contains helper
  functions.
-> student.db is a sqlite database containing 2 tables :
  1. 'students' to keep record of all registered users
  2. 'messages' to keep record of all messages sent and recieved

## Project Description:
   Youtube video link : https://youtu.be/OY2v4M9Bhoc
