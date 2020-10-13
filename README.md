# Viptela-Diagram
This is a Python-Flask based code to generate a diagram of a Cisco SDWAN network (dataplane only) and display the tunnels between the branches. This is based on Cisco's NextUI and viptelaquery (https://github.com/CiscoSE/viptelaquery). some changes have been made to the original code.

####To use
Requirements: Python 3.7+, Flask, configparser (optional)
*change ip,username and pwd to connect to vmanage, in the getconn.py
*Download NextUI js and css files from Cisco devnet (https://d1nmyq4gcgsfi5.cloudfront.net/site/neXt/) 
*put html,js,css files in relevent folder hierarchy (of Flask) (https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/)
*run getconn.py
*view from the browser (eg:- http://localhost:5000)
