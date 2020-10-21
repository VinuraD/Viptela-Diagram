from flask import Flask, render_template, url_for, request,redirect,jsonify, flash, session, abort
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_session import Session
import datetime
import pymongo
from pymongo import MongoClient
from itertools import islice 
from flask_mail import Mail, Message


app = Flask(__name__)

#loginmanager=LoginManager()
#loginmanager.init_app(app)

app.config['SECRET_KEY'] = 'cisco'
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '76e33b2f4b3738'
app.config['MAIL_PASSWORD'] = '8a8251963cfe85'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail= Mail(app)
#app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:cisco@localhost/Support_dashboard2'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#db = SQLAlchemy(app)

#class User(UserMixin):
#  def __init__(self,id):
#    self.id = id

#class inventory(db.Model):
#    __tablename__ = 'inventory'

#    serial = db.Column(db.VARCHAR, nullable=False, primary_key=True)
#    coverage = db.Column(db.Boolean, nullable=False)
#    startdate = db.Column(db.VARCHAR)
#    enddate = db.Column(db.VARCHAR, nullable=False)
#    eos=db.Column(db.VARCHAR)
#    type=db.Column(db.VARCHAR, nullable=False)
#    notes=db.Column(db.VARCHAR)
#    year=db.Column(db.VARCHAR)


#    def __init__(self, serial, coverage, startdate, enddate, eos, type, notes, year):
#        self.serial = serial
#        self.coverage = coverage
#        self.startdate = startdate
#        self.enddate = enddate
#        self.eos=column
#        self.type=type
#        self.notes=notes
#        self.year=year
        

my_users = {
    'admin': {'password': 'cisco123', 'roles': ['admin']},
    'cisco': {'password': 'cisco', 'roles': []},
}
client = MongoClient('localhost', 27017)
db=client["support_det"]
col1=db["all"]
col2=db["customer"]
col3=db['tablehistory']


@app.route("/")
def home():
    return redirect("/login")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect('/login')
        else:
            if username=='admin' and password=='C1sco123#':
                session[username] = True
                return redirect(url_for("index", username=username))
            elif username=='cisco' and password=='cisco123':
                session[username] = True
                return redirect(url_for("indexother", username=username))
            else:
                flash("Username or Password invalid.")
                return render_template('login.html', message="Invalid username or password.")
    else:
        return render_template("login.html")

@app.route("/logout/<username>")
def logout(username):
    session.pop(username, None)
    flash("successfully logged out.")
    return render_template("login.html")

@app.route("/index/<username>")
def index(username):
    if not session.get(username):
        abort(401)
    else:
        return render_template("index.html",username=username)

@app.route("/indexother/<username>")
def indexother(username):
    if not session.get(username):
        abort(401)
    else:
        return render_template("indexother.html",username=username)

@app.route("/index",methods=['GET','POST'])
def submit():
    return render_template("index.html")

@app.route("/indexother",methods=['GET','POST'])
def submitother():
    return render_template("indexother.html")

@app.route("/tables",methods=['GET','POST'])
def table():
    #category='all'
    return render_template('displaytable.html')

@app.route("/tablesother",methods=['GET','POST'])
def tablesother():
    #category='all'
    return render_template('displaytableother.html')


@app.route("/query", methods=['GET','POST'])
def query():
    cursor=list(col1.find({}))
    data_list=[]
    for i in cursor:
        #print("daaa",i)
        rec=i['dat']
        rec['exp']=expiry(i['dat'])
        data_list.append(rec)
        #data=
    response_dict={"data":""}
    response_dict["data"]=data_list
    return jsonify(response_dict)
    
@app.route("/edit",methods=['POST','GET'])
def edit():
    action=request.form['action']
    if action=='create':
        data=request.form.to_dict()
        #print(data)
        records=(parse(data))
        #print(records)
        #response_list=[]
        #response_dict={"data":""}
        #print(items[0])
        #dat={"dat":items[0]}
        for record in records["data"]:
            #print((record))
            dat={"dat":record}
            col1.insert_one(dat)
        #response_dict["data"]=response_list.append(items[0])
        report(records,changetype='Create')
        return jsonify(records)
            
    elif action=='edit':
        data=request.form.to_dict()
        #print(data)
        records=(parse(data))
        #process before entering to above format
        #response_list=[]
        #response_dict={"data":""}
        #dat={"dat":items[0]}
        for record in records["data"]:
            dat={"dat":record}
            col1.replace_one({'dat.sn':record['sn']},dat)#changing serial number????
        #response_dict["data"]=response_list.append(items[0])
        txt,txtlist=report(records,changetype='Update')
        history(txtlist)
        return jsonify(records)

    elif action=='remove':
        data=request.form.to_dict()
        records=(parse(data))
        print(records["data"])
        #process before entering to above format
        #response_list=[]
        #response_dict={"data":""}
        #dat={"dat":items[0]}        
        #print(items[1])
        for record in records["data"]:
            #print(record)
            #cursor=col1.find_one({"dat.sn":record["sn"]})
            col1.delete_one({'dat.sn':record['sn']})
        #print(cursor.get('_id'))        
        response_dict={}
        report(records,changetype='Delete')
        return jsonify(response_dict)
    
    else:
        return 'Error'
   
    #print(data)
    #return 'OK'
@app.route("/customer",methods=["POST","GET"])
def customer():
    return render_template('customer.html')

@app.route("/customerother",methods=["POST","GET"])
def customerother():
    return render_template('customerother.html')

@app.route("/customerquery",methods=["POST","GET"])
def customerquery():
    cursor=list(col2.find({}))
    data_list=[]
    for i in cursor:
        #print("daaa",i)
        rec=i['dat']
        data_list.append(rec)
        #data=
    response_dict={"data":""}
    response_dict["data"]=data_list
    return jsonify(response_dict)

@app.route("/customerlist",methods=["GET"])
def customerlist():
    cursor=(col2.distinct('dat.customer'))
    print(cursor)
    return jsonify(cursor)

@app.route("/customeredit",methods=['POST','GET'])
def customeredit():
    action=request.form['action']
    if action=='create':
        data=request.form.to_dict()
        #print(data)
        records=(parsecustomer(data))
        #print(records)
        #response_list=[]
        #response_dict={"data":""}
        #print(items[0])
        #dat={"dat":items[0]}
        for record in records["data"]:
            #print((record))
            dat={"dat":record}
            col2.insert_one(dat)
        #response_dict["data"]=response_list.append(items[0])
        return jsonify(records)
            
    elif action=='edit':
        data=request.form.to_dict()
        #print(data)
        records=(parsecustomer(data))
        #process before entering to above format
        #response_list=[]
        #response_dict={"data":""}
        #dat={"dat":items[0]}
        for record in records["data"]:
            dat={"dat":record}
            col2.replace_one({'dat.customer':record['customer']},dat)#changing serial number????
        #response_dict["data"]=response_list.append(items[0])
        return jsonify(records)

    elif action=='remove':
        data=request.form.to_dict()
        records=(parsecustomer(data))
        print(records["data"])
        #process before entering to above format
        #response_list=[]
        #response_dict={"data":""}
        #dat={"dat":items[0]}        
        #print(items[1])
        for record in records["data"]:
            #print(record)
            #cursor=col1.find_one({"dat.sn":record["sn"]})
            col2.delete_one({'dat.customer':record['customer']})
        #print(cursor.get('_id'))        
        response_dict={}
        return jsonify(response_dict)
    
    else:
        return 'Error'

@app.route('/history')
def history_view():
    return (render_template('history.html')) 


@app.route('/tablehistory')
def tablehistory():
    cursor=list(col3.find({}))
    data_list=[]
    for i in cursor:
            #print("daaa",i)
        rec=i['dat']
        data_list.append(rec)
            #data=
    response_dict={"data":""}
    response_dict["data"]=data_list
    return jsonify(response_dict)
       


def parse(data):
    state=data['action']
    del data['action']
    if state!='remove':
        fields=['customer','project','year','category','pronum','description','sn','contract','coverage','startdate','enddate','startdatemit','enddatemit','eos','notes','exp']
        #item=next(iter(data))
        #row=(item.split(']')[0][5:])
        dlist=[]
        for record in chunks(data):
            new_data={}
            
            for i in range(len(record)):           
                new_data[(fields)[i]]=record[list(record)[i]]
            
            print(new_data)            
            if new_data['sn']=='':
                new_data={"fieldErrors": [{"name":"sn","status": "This field is required"}]}
            else:
                new_data["DT_RowId"]=new_data['sn']
                dlist.append(new_data)  
        ddict={}       
        ddict["data"]=dlist
        return ddict

    else:
        fields=['DT_RowId','customer','project','year','pronum','description','category','sn','contract','coverage','startdate','enddate','startdatemit','enddatemit','eos','notes','exp']
        #item=next(iter(data))
        #row=(item.split(']')[0][5:])
        dlist=[]
        for record in chunks(data,17):
            new_data={}
            for i in range(len(record)):           
                new_data[sorted(fields)[i]]=record[list(record)[i]]            
            dlist.append(new_data) 
        ddict={}         
        ddict["data"]=dlist
        
        return ddict

def parsecustomer(data):
    state=data['action']
    del data['action']
    if state!='remove':
        fields=['customer','contact','category']
        #item=next(iter(data))
        #row=(item.split(']')[0][5:])
        dlist=[]
        for record in chunks(data,3):
            new_data={}
            
            for i in range(len(record)):           
                new_data[(fields)[i]]=record[list(record)[i]]
            
            print(new_data)            
            if new_data['customer']=='':
                new_data={"fieldErrors": [{"name":"customer","status": "This field is required"}]}
            else:
                new_data["DT_RowId"]=new_data['customer']
                dlist.append(new_data)  
        ddict={}       
        ddict["data"]=dlist
        return ddict

    else:
        fields=['DT_RowId','customer','contact','category']
        #item=next(iter(data))
        #row=(item.split(']')[0][5:])
        dlist=[]
        for record in chunks(data,4):
            new_data={}
            for i in range(len(record)):           
                new_data[sorted(fields)[i]]=record[list(record)[i]]            
            dlist.append(new_data) 
        ddict={}         
        ddict["data"]=dlist
        
        return ddict

def parshistory(data):
    
    fields=['update','time']
        #item=next(iter(data))
        #row=(item.split(']')[0][5:])
    dlist=[]
    for record in chunks(data,2):
        new_data={}            
        for i in range(len(record)):           
            new_data[(fields)[i]]=record[list(record)[i]]          
            if new_data['update']=='':
                new_data={}
            else:
                new_data["DT_RowId"]=new_data['time']
                dlist.append(new_data)  
        ddict={}       
        ddict["data"]=dlist
        
    return ddict

def chunks(data, SIZE=16):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

def expiry(data):
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    cur_mon=datetime.datetime.now().month
    cur_year=int(str(datetime.datetime.now().year)[-2:])
    state=''
    if data['enddatemit']!="":
        mon=data['enddatemit'][3:6]
        mon2=data['enddatemit'][2:5]
        if mon in months or mon2 in months:            
            if mon.isalpha():
                year=data['enddatemit'][7:][-2:]
                print(year,cur_year)
                if int(year)<cur_year:
                    state='alert'
                elif cur_mon+2==months.index(mon) and int(year)==cur_year:
                    state='warn'
                elif (cur_mon+1==months.index(mon) or cur_mon==months.index(mon)) and int(year)==cur_year:
                    state='alert'
                elif (cur_mon-months.index(mon)==11) and int(year)==cur_year+1:
                    state='alert'
                elif (cur_mon-months.index(mon)==10) and int(year)==cur_year+1:
                    state='warn'
                elif cur_mon>months.index(mon) and int(year)==cur_year:
                    state='warn'
                else:
                    state=''

            else:
                year=data['enddatemit'][6:][-2:]
                print(year,cur_year)
                if int(year)<cur_year:
                    state='alert'
                elif cur_mon+2==months.index(mon) and int(year)==cur_year:
                    state='warn'
                elif (cur_mon+1==months.index(mon) or cur_mon==months.index(mon)) and int(year)==cur_year:
                    state='alert'
                elif (cur_mon-months.index(mon)==11) and int(year)==cur_year+1:
                    state='alert'
                elif (cur_mon-months.index(mon)==10) and int(year)==cur_year+1:
                    state='warn'
                elif cur_mon>months.index(mon) and int(year)==cur_year:
                    state='warn'
                else:
                    state=''

        else:
            mon=(data['enddatemit'].split('/'))[0]
            year=(data['enddatemit'].split('/'))[2][-2:]
            print(year,cur_year)
            if mon.isalpha():
                if int(year)<cur_year:
                    state='alert'
                elif cur_mon+2==months.index(mon) and int(year)==cur_year:
                    state='warn'
                elif (cur_mon+1==months.index(mon) or cur_mon==months.index(mon)) and int(year)==cur_year:
                    state='alert'
                elif (cur_mon-months.index(mon)==11) and int(year)==cur_year+1:
                    state='alert'
                elif (cur_mon-months.index(mon)==10) and int(year)==cur_year+1:
                    state='warn'
                elif cur_mon>months.index(mon) and int(year)==cur_year:
                    state='warn'
                else:
                    state=''
            else:
                if int(year)<cur_year:
                    state='alert'
                elif cur_mon+2==int(mon) and int(year)==cur_year:
                    state='warn'
                elif (cur_mon+1==int(mon) or cur_mon==int(mon)) and int(year)==cur_year:
                    state='alert'
                elif (cur_mon-int(mon)==11) and int(year)==cur_year+1:
                    state='alert'
                elif (cur_mon-int(mon)==10) and int(year)==cur_year+1:
                    state='warn'
                elif cur_mon>int(mon) and int(year)==cur_year:
                    state='warn'
                else:
                    state=''

    else:   
        if data['enddate']!="":
            mon=data['enddate'][3:6]
            mon2=data['enddate'][2:5]
            if mon in months or mon2 in months:
                if mon.isalpha():
                    year=data['enddate'][7:][-2:]
                    if int(year)<cur_year:
                        state='alert'
                    elif cur_mon+2==months.index(mon) and int(year)==cur_year:
                        state='warn'
                    elif (cur_mon+1==months.index(mon) or cur_mon==months.index(mon)) and int(year)==cur_year:
                        state='alert'
                    elif (cur_mon-months.index(mon)==11) and int(year)==cur_year+1:
                        state='alert'
                    elif (cur_mon-months.index(mon)==10) and int(year)==cur_year+1:
                        state='warn'
                    elif cur_mon>months.index(mon) and int(year)==cur_year:
                        state='warn'
                    else:
                        state=''
                else:
                    year=data['enddate'][6:][-2:]
                    #print(year,cur_year)
                    if int(year)<cur_year:
                        state='alert'
                    elif cur_mon+2==months.index(mon2) and int(year)==cur_year:
                        state='warn'
                    elif (cur_mon+1==months.index(mon2) or cur_mon==months.index(mon2)) and int(year)==cur_year:
                        state='alert'
                    elif (cur_mon-months.index(mon2)==11) and int(year)==cur_year+1:
                        state='alert'
                    elif (cur_mon-months.index(mon2)==10) and int(year)==cur_year+1:
                        state='warn'
                    elif cur_mon>months.index(mon2) and int(year)==cur_year:
                        state='warn'
                    else:
                        state=''
            else:
                mon=(data['enddate'].split('/'))[0]
                year=(data['enddate'].split('/'))[2][-2:]
                #print(mon, data['enddate'])
                if mon.isalpha():
                    if int(year)<cur_year:
                        state='alert'
                    elif cur_mon+2==months.index(mon) and int(year)==cur_year:
                        state='warn'
                    elif (cur_mon+1==months.index(mon) or cur_mon==months.index(mon)) and int(year)==cur_year:
                        state='alert'
                    elif (cur_mon-months.index(mon)==11) and int(year)==cur_year+1:
                        state='alert'
                    elif (cur_mon-months.index(mon)==10) and int(year)==cur_year+1:
                        state='warn'
                    elif cur_mon>months.index(mon) and int(year)==cur_year:
                        state='warn'
                    else:
                        state=''
                else:
                    if int(year)<cur_year:
                        state='alert'
                    elif cur_mon+2==int(mon) and int(year)==cur_year:
                        state='warn'
                    elif (cur_mon+1==int(mon) or cur_mon==int(mon)) and int(year)==cur_year:
                        state='alert'
                    elif (cur_mon-int(mon)==11) and int(year)==cur_year+1:
                        state='alert'
                    elif (cur_mon-int(mon)==10) and int(year)==cur_year+1:
                        state='warn'
                    elif cur_mon>int(mon) and int(year)==cur_year:
                        state='warn'
                    else:
                        state=''

        elif state!='':
            pass
        else:
            state=''

    return state

def report(content,changetype):    
    msg = Message('Support_Portal_MITESP'+' '+str(datetime.datetime.now())+' '+'<No reply>', sender = '76e33b2f4b3738', recipients = ['07e3891334-5346f6@inbox.mailtrap.io'])
    final=''
    item=content['data']
    finallist=[]
    for record in item:
        #print(record)
        txt=''
        for key,value in record.items():
            if key=='customer' or key=='pronum' or key=='sn':
                txt=txt+key+': '+value+'\n'
                final.append(txt)
            else:
                pass
        final=final+txt+'\n'+'*'*25+'\n'

    msg.body = 'Dear admin,'+'\n'+'\n'+'Below changes were recorded in the Support Portal('+changetype+')'+'\n'+'\n'+final
    mail.send(msg)
    return final,finallist

def history(input):
    ##########clearing here##########
    #if mode='input':
    element={'update':'','time':''}
    for item in input:
        element['update']=item
        element['time']=str(datetime.datetime.now())
        dat={}
        dat['dat']=element
        col3.insert_many(input)


if __name__=="__main__":
    app.run(debug=True)