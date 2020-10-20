# Viptela-Diagram
This is a Python-Flask based code to generate a diagram of a Cisco SDWAN network (dataplane only) and display the tunnels between the branches. Currently it displays all the tunnels in the same colour (without labelling or differentiation). One future improvement will be labelling and adding different colours to different tunnels. This is only the first development stage.

![Snap](/images/snap.png)
Format: ![Alt Text](url)


## Use case
As described, this can be used to view the IPsec tunnels created between the branches in a Cisco SDWAN network.
####To use
Requirements: Python 3.7+, Flask, configparser (optional)
1.change ip,username and pwd to connect to vmanage, in the getconn.py
2.Download NextUI js and css files from Cisco devnet (https://d1nmyq4gcgsfi5.cloudfront.net/site/neXt/) 
3.put html,js,css files in relevent folder hierarchy (of Flask) (https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/)
4run getconn.py
5.view from the browser (eg:- http://localhost:5000)

Please note that this is only in early development phase
