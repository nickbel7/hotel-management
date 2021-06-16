from flask import Flask, render_template, request
import pypyodbc
from datetime import datetime
import re

app = Flask(__name__)

sql_user = 'sa'
sql_password = '2019'
sql_server_name = 'BELLOS-DELL-G3\SQL2019'
sql_database_name = 'HotelManagement'
connection = pypyodbc.connect('Driver={SQL Server};Server='+sql_server_name+';Database='+sql_database_name+';uid='+sql_user+';pwd='+sql_password)

rs = connection.cursor()    
rs.execute("SELECT * FROM Customers")
s = "<ul style='border:1px solid red'>"    
for row in rs:    
    s = s + "<li>"    
    for x in row:    
        s = s + str(x) + " "    
    s = s + "</li>"
s = s + "</ul>"
connection.close() 

@app.route("/")
def home():
    return "<html><body>" + s + "</body></html>" 

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content