[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/VinuraD/Viptela-Diagram)

# Viptela-Diagram
This is a Python-Flask based code to generate a diagram of a Cisco SDWAN network (dataplane only) and display the IPSec tunnels between the branches. Currently it displays all the tunnels in different colours. This is only the first development stage. 

![MicrosoftTeams-image](https://user-images.githubusercontent.com/31266374/98461589-5ef71800-21d3-11eb-924c-578f309d7415.png)


## Use case
As described, this can be used to view the IPsec tunnels created between the branches in a Cisco SDWAN network. *No controllers are displayed*

## Installation

* Clone the repository. ( Or download the .zip file directly).
```
git clone https://github.com/VinuraD/Viptela-Diagram 
```

* Go to the directory
```
cd .../Viptela-Diagram
```

* This requires Python 3.7+ mainly. Install Python added to path. It is preferred to have a virtualenv created for this project separately. After that following libraries are required.
-Flask, Configparser (optional)

* To create virtualenv,

```python 
python3 -m venv venv
```
>(For Linux) or 

```python 
virtualenv venv
``` 
>(For Windows)

* You can use `pip install <library_name>` to install them one by one. Or use requirements.txt as below (after activating the virtualenv)

```python
pip install -r requirements.txt
```

* Download NextUI js and css files from Cisco devnet (https://d1nmyq4gcgsfi5.cloudfront.net/site/neXt/). NextUI is used to build the UI here. 

* Use normal folder hierarchy used in a flask project, as explained here (https://flask.palletsprojects.com/en/1.1.x/tutorial/layout) You have to put app.js and data.js files in the 'static' folder. Here, data.js contains only an example dataset. One can edit it to statically include a diagram. Here in the repo, they are in order. But after downloading NextUI files, you will have to put them manually in the 'static' folder.

## Configuration

*Note: I have put the timeout for a API request as 300s (a big value). This might be required of you are using a VPN connection. Otherwise you may bring it down to something like 10s. (default value), as below (in viptelaquery.py)

```python
response = session.request("GET", url,verify=False,timeout=300)
```

## Usage

* To run, get a terminal/CMD and go to the directory where the project folder lies

 ```
 cd .../Viptela-Diagram/
 ```

* Activate virtualenv (if one is used only)

```python
source venv/bin/activate
```
>(Linux) or 
```python
venv\Scripts\activate
``` 
>(Windows)

* Then run the script,

```python
Python getconn.py
```
* You would see the Flask server intiated and you would be asked for ip address of the viptela server(vmanage),username and password
* This has only one web page to display the diagram, view it from a browser,

```
http://localhost:5000
```
*port=5000 might be different on your testing environment. If port 5000 is unused for other process, it will be occupied by Flask by default*.

## Testing

This was tested with an actual implementation of a Cisco SDWAN network

## Known Issues

If the API calls get delayed too much, the app might throw an unhandled error. But this will be caused due to network latencies such as when connecting through a remote VPN connection to make API requests. Hence, I have put 300s timeout (not recommended, only for testing/VPN environment)

## Getting Involved

You are welome to make improvements to the app via forks or give suggestions and even track/pointout issues.
[CONTRIBUTING](https://github.com/VinuraD/Viptela-Diagram/blob/main/CONTRIBUTING.md)

vinurad@millenniumitesp.com 

## Credits and references

https://github.com/CiscoSE/viptelaquery, Thanks, I used this as the code to make API requests. (I have made some changes to the original code in this project).
https://github.com/pcardotatgit/My_NeXt-UI_Tutorials, A good set of tutorials for NextUI

## LICENSE

Please view the LICENSE file
[LICENSE](https://github.com/VinuraD/Viptela-Diagram/blob/main/LICENSE)
