#!/usr/bin/python
from flask import Flask
import sys 
 
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"
 
 
if __name__ == "__main__":
    sys.stdout.write("\nHello Patent & Trade Office! Thanks for running me!\n\n")
#    app.run()
