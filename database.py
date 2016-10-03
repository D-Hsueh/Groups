#-*- coding:utf-8 -*-
import pymysql.cursors
class database:
    __connection__=object
    __config__ = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'xd8uojko8k',
        'db': 'Teams',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    def __init__(self):
        self.__connection__ = pymysql.connect(**self.__config__)

    def finishmission(self,missionid):
        try:
            with self.__connection__.cursor() as cursor:
                sql = "UPDATE mission SET schedule=101 WHERE missionid=%s"
                cursor.execute(sql, (missionid))
                self.__connection__.commit()
                return "1"
        except Exception, e:
            return '!'

    def exitTeam(self,userid,jointeamname):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT * FROM team WHERE userid=%s and teamname=%s'
                cursor.execute(sql, (userid, jointeamname))
                if (cursor.fetchone() != None):
                    sql = 'SELECT * FROM mission WHERE teamname=%s and schedule<100'
                    cursor.execute(sql, (jointeamname))
                    if (cursor.fetchone() != None):
                        return "Error:您是团队的创建者，团队中还有未完成的任务，无法退出团队"
                    else :

                        sql = "DELETE FROM  jointeam WHERE teamname=%s"
                        cursor.execute(sql, (jointeamname))
                        self.__connection__.commit()
                        sql = "DELETE FROM  mission WHERE teamname=%s"
                        cursor.execute(sql, (jointeamname))
                        self.__connection__.commit()

                        sql = "DELETE FROM  team WHERE teamname=%s"
                        cursor.execute(sql, (jointeamname))
                        self.__connection__.commit()
                        return '1'
                else :
                    sql = 'SELECT * FROM mission WHERE userid=%s and teamname=%s and schedule<100'
                    cursor.execute(sql, (userid, jointeamname))
                    if (cursor.fetchone() != None):
                        return 'Error:您在该团队中存在未完成任务，退出失败'
                    else :
                        sql = "DELETE FROM  mission WHERE teamname=%s and userid=%s"
                        cursor.execute(sql, (jointeamname,userid))
                        self.__connection__.commit()
                        sql = "DELETE FROM  jointeam WHERE teamname=%s and userid=%s"
                        cursor.execute(sql, (jointeamname, userid))
                        self.__connection__.commit()
                        return '1'
        except Exception, e:
            return e.message

    def joinTeam(self,userid,jointeamname):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT * FROM jointeam WHERE userid=%s and teamname=%s'
                cursor.execute(sql,(userid, jointeamname,))
                if (cursor.fetchone()!=None):
                    return "2"
                sql = "INSERT INTO jointeam(userid,teamname) VALUE (%s, %s)"
                cursor.execute(sql, (userid, jointeamname,))
                self.__connection__.commit()
                return "1"
        except Exception, e:
            return "2"

    def changeschedule(self,missionid,schedule):
        try:
            with self.__connection__.cursor() as cursor:
                sql = "UPDATE mission SET schedule=%s WHERE missionid=%s"
                cursor.execute(sql, (schedule,missionid))
                self.__connection__.commit()
                return "1"
        except Exception, e:
            return '!'

    def showmymission(self,userid):
        try:
            with self.__connection__.cursor() as cursor:
                sql='SELECT t1.missionid,t1.missionname,t1.missionintr,t1.schedule,t1.deadline,t1.teamname FROM mission t1,user t3 WHERE t3.userid=%s  and t1.userid=t3.userid'
                cursor.execute(sql, (userid))
                result = cursor.fetchall()
                return result
        except Exception, e:
            return '!'

    def showteammission(self,teamname):
        try:
            with self.__connection__.cursor() as cursor:
                sql='SELECT t1.missionname,t1.missionintr,t1.schedule,t3.nickname FROM mission t1,user t3 WHERE t1.teamname=%s and t1.missionid=t1.missionid and t1.userid=t3.userid'
                cursor.execute(sql, (teamname))
                result = cursor.fetchall()
                return result
        except Exception, e:
            return '!'

    def createMission(self,missionname,missionintr,deadline,belonguser,teamname):
        try:
            with self.__connection__.cursor() as cursor:
                userid = self.finduserid(belonguser)
                sql = "INSERT INTO mission(missionname,missionintr,deadline,teamname,userid) VALUE (%s, %s, %s,%s,%s)"
                cursor.execute(sql,(missionname,missionintr,deadline,teamname,userid))
                self.__connection__.commit()
                return "1"
        except Exception, e:
            return "2"

    def findmissionid(self,missionname):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT missionid FROM mission WHERE missionid=(SELECT max(missionid) FROM mission WHERE missionname=%s)'
                cursor.execute(sql,(missionname))
                return cursor.fetchone()['missionid']
        except Exception, e:
            return "-1"

    def getnumber(self,teamname):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT t2.email,t2.nickname FROM jointeam t1,user t2 WHERE t1.teamname=%s and t1.userid=t2.userid'
                cursor.execute(sql, (teamname))
                result = cursor.fetchall()
                return result
        except Exception, e:
            print e.message
            return '!'

    def commitmes(self,str,teamname):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT announcement FROM team WHERE teamname=%s'
                cursor.execute(sql, (teamname))
                result = cursor.fetchone()
                if (result['announcement']!=None):
                    str=result['announcement']+str
                sql = "UPDATE team SET announcement=%s WHERE teamname=%s"
                cursor.execute(sql, (str,teamname))
                self.__connection__.commit()
                sql = 'SELECT announcement FROM team WHERE teamname=%s'
                cursor.execute(sql, (teamname))
                result = cursor.fetchone()
                return result['announcement']
        except Exception, e:
            print e.message
            return '!'

    def getteammessage(self,teamname):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT * FROM team WHERE teamname=%s'
                cursor.execute(sql, (teamname))
                result = cursor.fetchone()
                return result
        except Exception, e:
            print e.message
            return '!'

    def getmyteam(self,userid):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT teamname FROM jointeam WHERE userid=%s'
                cursor.execute(sql, (userid))
                result = ""
                while (True):
                    temp=cursor.fetchone()
                    if (temp==None) :
                        break
                    result = result + str(temp['teamname']) + " "
                return result
        except Exception, e:
            print e.message
            return '!'

    def finduser(self,email):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT nickname FROM user WHERE email=%s'
                cursor.execute(sql, (email))
                result = cursor.fetchone()
                return result['nickname']
        except Exception, e:
            return '!'

    def finduserid(self,email):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT userid FROM user WHERE email=%s'
                cursor.execute(sql, (email))
                result = cursor.fetchone()
                return result['userid']
        except Exception, e:
            return '!!'

    def createTeam(self,teamname,mainid,introduction,userid):
        try:
            with self.__connection__.cursor() as cursor:
                sql = "INSERT INTO team(teamname,mainider,introduction,userid) VALUE (%s, %s, %s,%s)"
                cursor.execute(sql,(teamname,mainid,introduction,userid))
                self.__connection__.commit()
                sql = "INSERT INTO jointeam(userid,teamname) VALUE (%s, %s)"
                cursor.execute(sql, (userid, teamname,))
                self.__connection__.commit()
                return "1"
        except Exception, e:
            return "2"

    def login(self,email,nickname,passwd):
        try:
            with self.__connection__.cursor() as cursor:
                sql = "INSERT INTO user(email,nickname,passwd) VALUE (%s, %s, %s)"
                cursor.execute(sql,(email,nickname,passwd))
                self.__connection__.commit()
                return "1"
        except Exception, e:
            return "2"

    def sign(self,username,password):
        try:
            with self.__connection__.cursor() as cursor:
                sql = 'SELECT * FROM user WHERE email=%s and passwd=%s'
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                if (result=='None'):
                    return '2'
                else:
                    return '1'
        except Exception, e:
            return "2"