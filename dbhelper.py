import pymysql
import os
import subprocess

class dbhelper:
    def __init__(self, dbname="indi_banua"):
        self.dbname = dbname
        self.db = pymysql.connect(host='localhost',user='root',db=dbname)
        # self.db = pymysql.connect(host='192.168.1.146',user='root',db=dbname)
        self.cursor = self.db.cursor()

    def get_all(self):
        sql = "SELECT * FROM user"
        
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_user(self,where,tosearch,toget='*'):
        sql = "SELECT {} FROM user WHERE `{}` = {}".format(toget,where,tosearch)

        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_user_telegram(self,id_telegram):
        sql = "SELECT * FROM user_telegram WHERE `id_telegram` = {}".format(id_telegram)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_event_by_otp(self,otp):
        sql = "SELECT id_event FROM otp WHERE `otp` = {}".format(otp)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_event_participant(self, data):
        sql = "INSERT INTO `event_participant` (`id_event`, `id_user`) VALUES ('{}','{}');"\
        .format(*data.values()) 
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except pymysql.IntegrityError as e:
            return str(e)

    def insert(self,datauser,chat_id):
        sql = "INSERT INTO `user` (`nik`, `name`, `loker`,\
        `account_type`, `created_at`) VALUES ('{}', '{}', '{}','{}', {});"\
        .format(*datauser.values()) 
        
        try:
            self.cursor.execute(sql)
            sqltelegram = "INSERT INTO `user_telegram` ( `id_user`, `id_telegram`) VALUES \
            ('{}','{}');".format(self.cursor.lastrowid,chat_id)
            try:
                self.cursor.execute(sqltelegram)
                self.db.commit()
            except Exception as e:
                self.db.commit()
                return str(e)
            return self.cursor.fetchall()
        except pymysql.IntegrityError as e:
            return str(e)

    def edit(self,data):
        sql = "UPDATE `user` SET `name` = '{}', `loker` = '{}' WHERE \
        `user`.`id_user` = '{}';".format(*data.values())
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except pymysql.IntegrityError as e:
            return e
       
    def delete(self,id_user):
        sql = "DELETE FROM `user` WHERE `id_user` = '{}'".format(id_user)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except pymysql.IntegrityError as e:
            return e    

    def bind(self, id_user, id_telegram):
        sql = "INSERT INTO `user_telegram` (`id_user`,`id_telegram`) VALUES ('{}','{}')".format(id_user,id_telegram)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except pymysql.IntegrityError as e:
            return e    


    def unbind(self, id_telegram):
        sql = "DELETE FROM `user_telegram` WHERE `id_telegram` = '{}'".format(id_telegram)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except pymysql.IntegrityError as e:
            return e    

    
    def password_hash(self,pw):
        p = subprocess.Popen(['php',os.getcwd()+'\\genpass.php',pw],shell=True,stdout=subprocess.PIPE)
        result = p.communicate()[0]
        return result

    def password_verify(self,pw,hashpw):
        p = subprocess.Popen(['php',os.getcwd()+'\\verpass.php',pw,hashpw],shell=True,stdout=subprocess.PIPE)
        result = p.communicate()[0]
        return result
