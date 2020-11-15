import viptelaquery
import flask
from flask import Flask, render_template, url_for, request,redirect,jsonify, flash, session, abort
import time
from viptelaquery import Loop1,Loop2

import getpass
class Login:
    def __init__(self,ip,un,pw):
        self.ip = ip
        self.name = un
        self.pw = pw
D= Login(input('IP address: '),input('Username: '),getpass.getpass())

while Loop2.X:
        while Loop1.X:
            ip_address= D.ip
            username= D.name
            password = D.pw
            if(viptelaquery.initalize_connection(ip_address,username,password)==False):
                 D.ip= input('IP address: ')
            else:
                session=viptelaquery.initalize_connection(ip_address,username,password)
        if(viptelaquery.get_inventory(ip_address,session)==False):
            D.name = input('Username: ')
            D.pw = getpass.getpass()
        else:
            inventory=viptelaquery.get_inventory(ip_address,session)

app=Flask(__name__)

colors=['#cd5c5c','#0000ff','#008000','#884513','#ff0ff']


@app.route("/")
def home():    
    print(inventory)
    dat={}
    nodes=[]
    links=[]
    linkstrack=[]
    link_colors=[]
    link_details=[]

    mapper={}
    index=0
    for key,value in inventory.items():
        #print(key)
        description={}
        if value!='vmanage' and value!='vBond' and value!='vsmart':
            description['id']=index
            description['name']=value+' '+key
            nodes.append(description)
            mapper[key]=index
            index+=1
        else:
            pass
    
    #print(nodes)
    
    for node in nodes:
        name=node['name'].split(' ')[0]
        ip=node['name'].split(' ')[1]
        #print(name)
        if name!='vmanage' and value!='vBond' and value!='vsmart':
            session=viptelaquery.initalize_connection(ip_address,username,password)
            link_det,color_list=viptelaquery.get_tunnel_statistic(ip_address,session,ip,inventory)
            link_colors.extend(color_list)
            print(link_det)
            link_details.append(link_det)
            #print(colorlist)
        else:
            pass
            
    color_list=sorted(list(set(link_colors)))    
    for link_det in link_details:        
        for t in link_det['target']:
            link={}
            nodeid=nodes[link_details.index(link_det)]['id']
            link['source']=nodeid
            link['target']=mapper[t.split(' ')[0]]####when there is error in viptelaquery???
            link['color']=colors[color_list.index(t.split(' ')[1])]
            print(link['color'])
            if (str(link['source'])+' '+str(link['target'])+' '+t.split(' ')[1] in linkstrack) or (str(link['target'])+' '+str(link['source'])+' '+t.split(' ')[1] in linkstrack):#any(d['source'] == mapper[t.split(' ')[0]] for d in links) and any(d['target'] == node['id'] for d in links):
                pass
            else:
                links.append(link)
                linkstrack.append(str(link['source'])+' '+str(link['target'])+' '+t.split(' ')[1])
        

    
    dat['nodes']=nodes
    dat['links']=links
    print(dat)
    legend_dat={}
    for color in color_list:
        legend_dat[color]=colors[color_list.index(color)]

    return render_template("index.html",topdat=dat, legenddat=legend_dat)

@app.route("/test")
def test():
    dat2={
	"nodes": [
		{
			"id": '0',
			"name": "York"
		},
		{
			"id": '1',
			"name": "Los Angeles"
		},
		{
			"id": '2',
			"name": "Houston"
		}
	],
	"links": [
		{
			"source": '0',
			"target": '1',
            "color":"red"
		},
		{
			"source": '0',
			"target": '2',
            "color":"blue"
		}
	]
}
    return render_template("index.html",topdat=dat2)


if __name__=="__main__":    
    app.run(debug=False)
