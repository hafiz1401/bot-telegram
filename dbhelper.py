import pymysql.cursors
import os
import subprocess

class dbhelper:
    def __init__(self, dbname="indi_banua"):
        # self.dbname = dbname
        # self.db = pymysql.connect(host='localhost',user='root',db=dbname)
        # self.db = pymysql.connect(host='192.168.1.146',user='root',db=dbname)
        # self.cursor = self.db.cursor()
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def get_all(self):
        # result = ''
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM user"
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            self.connection.close()

        return result
   
    def get_user(self,where,tosearch,toget='*'):
        # result = ''
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT {} FROM user WHERE `{}` = {}".format(toget,where,tosearch)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            self.connection.close()

        return result

    def get_user_telegram(self,id_telegram):
        # result = ''
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM user_telegram WHERE `id_telegram` = {}".format(id_telegram)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            self.connection.close()

        return result

    def get_event_by_otp(self,otp):
        # result = ''
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT id_event FROM otp WHERE `otp` = {}".format(otp)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            self.connection.close()

        return result
        
    def insert_event_participant(self, data):
        # result = ''
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `event_participant` (`id_event`, `id_user`) VALUES ('{}','{}');".format(*data.values()) 
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            self.connection.close()

        return result

    def insert(self,nik,name,loker,account_type,created_at,chat_id):
        # result = ''
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user` (`nik`, `name`, `loker`,\
                    `account_type`, `created_at`) VALUES ('{}', '{}', '{}','{}', {});"\
                    .format(nik,name,loker,account_type,created_at) 
                cursor.execute(sql)
                sqltelegram = "INSERT INTO `user_telegram` ( `id_user`, `id_telegram`) VALUES \
                    ('{}','{}');".format(self.cursor.lastrowid,chat_id)
                cursor.execute(sqltelegram)
                result = cursor.fetchall()

            connection.commit()
        finally:
            self.connection.close()

        return result
        
      
    def edit(self,data):
        # result = ''
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `user` SET `name` = '{}', `loker` = '{}' WHERE \
                    `user`.`id_user` = '{}';".format(*data.values())
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            self.connection.close()

        return result
      
       
    def delete(self,id_user):
        # result = ''
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `user` WHERE `id_user` = '{}'".format(id_user)
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            self.connection.close()

        return result

    def bind(self, id_user, id_telegram):
        # result = ''
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user_telegram` (`id_user`,`id_telegram`) VALUES ('{}','{}')".format(id_user,id_telegram)
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            self.connection.close()

        return result

    def unbind(self, id_telegram):
        # result = ''
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `user_telegram` WHERE `id_telegram` = '{}'".format(id_telegram)
        
            connection.commit()
        finally:
            self.connection.close()

        return result
        
    def password_hash(self,pw):
        p = subprocess.Popen(['php',os.getcwd()+'\\genpass.php',pw],shell=True,stdout=subprocess.PIPE)
        result = p.communicate()[0]
        return result

    def password_verify(self,pw,hashpw):
        p = subprocess.Popen(['php',os.getcwd()+'\\verpass.php',pw,hashpw],shell=True,stdout=subprocess.PIPE)
        result = p.communicate()[0]
        return result
