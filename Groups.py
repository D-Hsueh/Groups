from flask import Flask,render_template,request,redirect,url_for,session
from database import database
import json,datetime

app = Flask(__name__)

app.secret_key = '23KIRUFJPIEO2FU2F0O34IJFPOW3JG3;4L24JGP39IKJ'

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

@app.route('/')
def ToWelcome():
    return render_template('welcome.html')

@app.route('/mainview')
def mainview():
    if 'username' in session:
        nickname=dbcontorller.finduser(session['username'])
        return render_template('mainview.html',name=nickname,email=session['username'])
    return 'You are not logged in'

@app.route('/mainview',methods=['POST'])
def chuli():
    if 'username' in session:
        if request.method == "POST":
            if (request.form['commond']=='signout'):
                session.pop('username', None)
                return '/'
            elif(request.form['commond']=='createTeam'):
                teamname = request.form['teamname']
                mainid = request.form['mainid']
                introduction = request.form['introduction']
                userid=dbcontorller.finduserid(session['username'])
                return dbcontorller.createTeam(teamname,mainid,introduction,userid)
            elif (request.form['commond'] == 'getmyteam'):
                result=dbcontorller.getmyteam(dbcontorller.finduserid(session['username']))
                print result
                return result
            elif(request.form['commond'] == 'getteammessage'):
                result=dbcontorller.getteammessage(request.form['teamname']);
                message=json.dumps(result, ensure_ascii = False)
                return message
            elif (request.form['commond'] == 'commitmes'):
                mes=request.form['mes']
                user=dbcontorller.finduser(session['username'])
                userid = dbcontorller.finduserid(session['username'])
                return dbcontorller.commitmes(user+": "+mes+"\r\n",request.form['teamname'])
            elif (request.form['commond'] == 'getnumber'):
                teamname=request.form['teamname']
                result=dbcontorller.getnumber(teamname)
                message = json.dumps(result, ensure_ascii=False)
                return message
            elif (request.form['commond'] == 'createmession'):
                missionname=request.form['missionname']
                missionintr = request.form['missionintr']
                deadline = request.form['deadline']
                belonguser = request.form['belonguser']
                belonguser=belonguser.split(":")[1]
                teamname = request.form['teamname']
                return dbcontorller.createMission(missionname,missionintr,deadline,belonguser,teamname)
            elif (request.form['commond'] == 'showteammission'):
                teamname = request.form['teamname']
                result=dbcontorller.showteammission(teamname)
                try :
                    if (result=='!'| result==None):
                        return '2'
                except Exception, e:
                    message = json.dumps(result, ensure_ascii=False)
                    return message
            elif (request.form['commond'] == 'showmymission'):
                userid = dbcontorller.finduserid(session['username'])
                result =dbcontorller.showmymission(userid)
                try :
                    if (result=='!'| result==None):
                        return '2'
                except Exception, e:
                    message = json.dumps(result,cls=CJsonEncoder,ensure_ascii=False)
                    return message
            elif (request.form['commond'] == 'changeschedule'):
                missionid=request.form['missionid']
                schedule=request.form['schedule']
                return dbcontorller.changeschedule(missionid,schedule)
            elif (request.form['commond'] == 'joinTeam'):
                jointeamname=request.form['jointeamname']
                userid = dbcontorller.finduserid(session['username'])
                return dbcontorller.joinTeam(userid,jointeamname)
            elif (request.form['commond'] == 'exitTeam'):
                jointeamname=request.form['jointeamname']
                userid = dbcontorller.finduserid(session['username'])
                return dbcontorller.exitTeam(userid,jointeamname)
            elif (request.form['commond'] == 'finishmission'):
                missionid=request.form['missionid']
                return dbcontorller.finishmission(missionid)

    return '2'


@app.route('/signinsuccess/<name>')
def siginjump(name):
    session['username']=name
    return redirect(url_for('mainview'))



@app.route('/',methods=['POST'])
def login():
    if request.method=="POST":
        if (request.form["status"]=='login'):
            username = request.form["username"]
            password = request.form["password"]
            nickname = request.form["nickname"]
            return dbcontorller.login(username,nickname,password)
        elif(request.form["status"]=='signin'):
            username = request.form["username"]
            password = request.form["password"]
            a= dbcontorller.sign(username,password)
            return a
    return "2"


if __name__ == '__main__':
    dbcontorller=database()
    app.run()
