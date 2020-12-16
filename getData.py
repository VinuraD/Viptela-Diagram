import requests
import statistics

def get_statistics(server_address,session):     
    url = "https://"+server_address+"/dataservice/statistics/approute/transport/summary/jitter"
    response = session.request("GET", url, verify= False)
    json_string = response.json()

    jitter = []
    color = []
    loss_percentage = []
    latency = []

    for data in json_string['data']:   #separting values for the relevent color
        if data['color'] in color:
            index = color.index(data['color'])
            jitter[index].append(data['jitter'])
            loss_percentage[index].append(data['loss_percentage'])
            latency[index].append(data['latency'])
        else:
            color.append(data['color'])
            index = color.index(data['color'])
            jitter.append([])
            loss_percentage.append([])
            latency.append([])
            jitter[index].append(data['jitter'])
            loss_percentage[index].append(data['loss_percentage'])
            latency[index].append(data['latency'])


    jitter_avg=[]
    loss_avg = []
    latency_avg = []
    for count in range(len(color)):         #Taking the avg. 
        color[count]= color[count].split(':')[0]
        print(color)
        jitter_avg.append(round(statistics.mean(jitter[count]),2))
        loss_avg.append(round(statistics.mean(loss_percentage[count]),2))
        latency_avg.append(round(statistics.mean(latency[count]),2))

    statistic = {'ISP':color, 'Jitter':jitter_avg ,'Loss':loss_avg , 'Latency':latency_avg}  
    return statistic
