import requests
import urllib3
import configparser

class True_False:
  def __init__(self):
    self.X = True
Loop1 = True_False()
Loop2 = True_False()

def initalize_connection(ipaddress,username,password):
    
    """
    This function will initialize a connection to the Viptela vManage platform.

    :param ipaddress: This is the IP Address and Port number of vManage (i.e., "192.168.0.1:8443")
    :param username:  This is the username for vManage
    :param password:  This is a password for vManage
    :return: A session object which can be used to make subsequent calls for other queries
    """

    # Disable warnings like unsigned certificates, etc.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url="https://"+ipaddress+"/j_security_check"

    payload = "j_username="+username+"&j_password="+password
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }

    sess=requests.session()

    # Handle exceptions if we cannot connect to the vManage
    try:
        response = sess.request("POST", url, data=payload, headers=headers,verify=False,timeout=10)
    except requests.exceptions.ConnectionError:
        print ("Unable to Connect to "+ipaddress)       
        return False

    Loop1.X = False
    return sess

def get_inventory(serveraddress,session):

    """
    This function retrieves the complete hostname data for everything in vManage
    :param serveraddress: This is the IP Address and Port number of vManage (i.e., "192.168.0.1:8443")
    :param session: session object that was returned from the prior initialize_connection function
    :return: inventory data in a dictionary format
    """
    print("Retrieving the inventory data from the vManage at "+serveraddress+"\n")

    url = "https://" + serveraddress + "/dataservice/device"
    response = session.request("GET", url, verify=False, timeout=300)

    try:
        json_string = response.json()
    except ValueError:
        print ("Incorrect username/password. Re-enter.. ")
        Loop1.X= True
        return False

    Loop2.X= False
    Loop1.X= False

    #print(json_string)
    #for item in json_string['data']:
    #   print(item)

    # Initialize the inventory data dictionary
    inv={}

    # Store each item in the dictionary with the key of the "system-ip"
    for item in json_string['data']:
    #   print (item['local-system-ip']+"   "+item['host-name'])
        inv[item['system-ip']]=item['host-name']
    return(inv)


def get_tunnel_statistic(serveraddress,session,systemip,inventory):

    """
    This function will return the details for all the tunnels for a particular endpoint
    :param serveraddress: This is the IP Address and Port number of vManage (i.e., "192.168.0.1:8443")
    :param session: session object that was returned from the prior initialize_connection function
    :param systemip: systemip of a device that we want to receive detailed statistics on
    :return: nothing
    """
    print ("Returning the tunnel statistics for device: "+systemip+"\n")

    url = "https://"+serveraddress+"/dataservice/device/tunnel/statistics?deviceId="+systemip
    links_det={}

    response = session.request("GET", url,verify=False,timeout=300)
    json_string=response.json()
    #print (json_string)
    #for item in json_string['data']:
    #    print(item)

    # If there is an error, with the query then let's print out the error code
    if 'error' in json_string:
        print("An Error Occured processing the data")
        print(json_string['error']['details'])
        targets=[]
        colors=[]
        links_det['target']=targets
        links_det['source']=systemip
    else:
       
        # Process through each Tunnel on the device
        
        targets=[]
        colors=[]
        for stats in json_string['data']:
            #rx=rx+int(stats['rx_octets'])
            #tx=tx+int(stats['tx_octets'])
            #print(stats)
            links_det['source']=stats['vdevice-host-name']
            targets.append(stats['system-ip']+' '+stats['local-color'])
            colors.append(stats['local-color'])
            #links_det['target']=stats['system-ip']#,stats['local-color']
            #print(inventory[stats['system-ip']])
        
        links_det['target']=targets
        colors=list(set(colors))
        #links_det['colors']=colors
        print(colors,'Here')
        
    return links_det,colors
