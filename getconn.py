import viptelaquery
import flask
from flask import Flask, render_template, url_for, request,redirect,jsonify, flash, session, abort
import time


app=Flask(__name__)

colors=['#cd5c5c','#0000ff','#008000','#884513','#ff0ff']

@app.route("/")
def home():
    session=viptelaquery.initalize_connection('ip','user','pwd')
    inventory=viptelaquery.get_inventory('ip',session)
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
            session=viptelaquery.initalize_connection('ip','user','pwd')
            link_det,color_list=viptelaquery.get_tunnel_statistic('ip',session,ip,inventory)
            #
            print(link_det)
            
	    for t in link_det['target']:
                link={}
                link['source']=node['id']
                link['target']=mapper[t.split(' ')[0]]####when there is error in viptelaquery???
                link['color']=colors[color_list.index(t.split(' ')[1])]
                if (str(link['source'])+' '+str(link['target'])+' '+t.split(' ')[1] in linkstrack) or (str(link['target'])+' '+str(link['source'])+' '+t.split(' ')[1] in linkstrack):#any(d['source'] == mapper[t.split(' ')[0]] for d in links) and any(d['target'] == node['id'] for d in links):
                    pass
                else:
                    links.append(link)
                    linkstrack.append(str(link['source'])+' '+str(link['target'])+' '+t.split(' ')[1])
        else:
            pass

    
    dat['nodes']=nodes
    dat['links']=links
    print(dat)
    return render_template("index.html",topdat=dat)

if __name__=="__main__":
    app.run(debug=True)
