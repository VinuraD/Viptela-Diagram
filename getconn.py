import viptelaquery
import flask
from flask import Flask, render_template, url_for, request,redirect,jsonify, flash, session, abort
import time


app=Flask(__name__)

@app.route("/")
def home():
    session=viptelaquery.initalize_connection('172.25.107.121','admin','cisco')
    inventory=viptelaquery.get_inventory('172.25.107.121',session)
    print(inventory)
    dat={}
    nodes=[]
    links=[]
    linkstrack=[]

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
            session=viptelaquery.initalize_connection('172.25.107.121','admin','cisco')
            link_det=viptelaquery.get_tunnel_statistic('172.25.107.121',session,ip,inventory)
            #
            print(link_det)
            
            for t in link_det['target']:
                link={}
                link['source']=node['id']
                link['target']=mapper[t.split(' ')[0]]####when there is error in viptelaquery???
                if (str(link['source'])+' '+str(link['target'])+' '+t.split(' ')[1] in linkstrack) or (str(link['target'])+' '+str(link['source'])+' '+t.split(' ')[1] in linkstrack):#any(d['source'] == mapper[t.split(' ')[0]] for d in links) and any(d['target'] == node['id'] for d in links):
                    pass
                else:
                    links.append(link)
                    linkstrack.append(str(link['source'])+' '+str(link['target'])+' '+t.split(' ')[1])
        else:
            pass

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
			"target": '1'
		},
		{
			"source": '0',
			"target": '2'
		}
	]
}
    dat['nodes']=nodes
    dat['links']=links
    print(dat)
    return render_template("index.html",topdat=dat)

if __name__=="__main__":
    app.run(debug=True)