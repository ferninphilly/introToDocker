#!/usr/bin/python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello US Patent and Trade Office!'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0') 
#   sys.stdout.write("\nHello Patent & Trade Office! Thanks for running me!\n\n")
