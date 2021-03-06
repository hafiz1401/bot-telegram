import pymysql.cursors
import os
import subprocess
from math import radians, cos, sin, asin, sqrt
from datetime import datetime



class dbhelper:
    def __init__(self, dbname="indi_banua"):
        self.dbname = dbname
        # self.db = pymysql.connect(host='localhost',user='root',db=dbname)
        # self.db = pymysql.connect(host='192.168.1.146',user='root',db=dbname)
        # self.cursor = self.db.cursor()


    def makeConn(self):
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db=self.dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        return connection

    def check_radius(self,check_point_lat,check_point_long,center_point_lat,center_point_long):
        lat1 = center_point_lat
        lon1 = center_point_long
        lat2 = check_point_lat
        lon2 = check_point_long

        a = self.haversine(lon1, lat1, lon2, lat2)
        return a

    
   
    def get_event(self,where,tosearch,toget='*'):
        # result = ''
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT event.{},lokasi.{} FROM event INNER JOIN lokasi on lokasi.id_lokasi = event.id_lokasi WHERE event.{} = {} AND event.event_start < '{}' AND event.event_end > '{}' ".format(toget,toget,where,tosearch,now,now)
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            connection.close()

        return result

    def get_event_participant(self,id_event,id_user,toget='*'):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT {} FROM event_participant WHERE `id_event` = {} AND `id_user` = {}".format(toget,id_event,id_user)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

    def get_event_user(self,where,tosearch,toget='*'):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT {} FROM event_user WHERE `{}` = {}".format(toget,where,tosearch)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

    def get_user(self,where,tosearch,toget='*'):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT {} FROM user WHERE `{}` = {}".format(toget,where,tosearch)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

    def get_user_telegram(self,id_telegram):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM user_telegram WHERE `id_telegram` = {}".format(id_telegram)
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            connection.close()

        return result

    def get_event_by_otp(self,otp):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id_event FROM otp WHERE `otp` = {}".format(otp)
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result
        
    def insert_event_participant(self, id_event,id_user,hadir):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `event_participant` (`id_event`, `id_user`,`hadir`) VALUES ('{}','{}','{}');".format(id_event,id_user,hadir) 
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            connection.close()

        return result

    def insert(self,nik,name,loker,account_type,created_at,chat_id):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user` (`nik`, `name`, `loker`,\
                    `account_type`, `created_at`) VALUES ('{}', '{}', '{}','{}', {});"\
                    .format(nik,name,loker,account_type,created_at) 
                cursor.execute(sql)
                sqltelegram = "INSERT INTO `user_telegram` ( `id_user`, `id_telegram`) VALUES \
                    ('{}','{}');".format(cursor.lastrowid,chat_id)
                cursor.execute(sqltelegram)
                result = cursor.fetchall()

            connection.commit()
        finally:
            connection.close()

        return result
        
      
    def edit(self,data):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `user` SET `name` = '{}', `loker` = '{}' WHERE \
                    `user`.`id_user` = '{}';".format(*data.values())
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            connection.close()

        return result
      
       
    def delete(self,id_user):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `user` WHERE `id_user` = '{}'".format(id_user)
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            connection.close()

        return result

    def bind(self, id_user, id_telegram):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user_telegram` (`id_user`,`id_telegram`) VALUES ('{}','{}')".format(id_user,id_telegram)
                cursor.execute(sql)
                result = cursor.fetchall()

            connection.commit()
        finally:
            connection.close()

        return result

    def unbind(self, id_telegram):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `user_telegram` WHERE `id_telegram` = '{}'".format(id_telegram)
                cursor.execute(sql)
                result = cursor.fetchall()
        
            connection.commit()
        finally:
            connection.close()

        return result
        
    def password_hash(self,pw):
        p = subprocess.Popen(['php',os.getcwd()+'\\genpass.php',pw],shell=True,stdout=subprocess.PIPE)
        result = p.communicate()[0]
        return result

    def password_verify(self,pw,hashpw):
        p = subprocess.Popen(['php',os.getcwd()+'\\verpass.php',pw,hashpw],shell=True,stdout=subprocess.PIPE)
        result = p.communicate()[0]
        return result

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def get_broadcast(self):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM broadcast"
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

    def delete_broadcast(self,id_broadcast):
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM broadcast WHERE `id_broadcast` = {}".format(id_broadcast)
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()

        return result

class User:
    def __init__(self, dbname="indi_banua"):
        self.dbname = dbname

    def makeConn(self):
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db=self.dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        return connection

    def get_all(self):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM user"
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result
        
class Order:
    def __init__(self, dbname="indi_order"):
        self.dbname = dbname
        # self.db = pymysql.connect(host='localhost',user='root',db=dbname)
        # self.db = pymysql.connect(host='192.168.1.146',user='root',db=dbname)
        # self.cursor = self.db.cursor()


    def makeConn(self):
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db=self.dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        return connection

    def insert(self,loker,order_by,order,jenis,keterangan):
        # result = ''
        connection = self.makeConn()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `order` (`loker`, `order_by`, `order`,`jenis`,`keterangan`)\
                    VALUES ('{}', '{}', '{}','{}','{}');"\
                    .format(loker,order_by,order,jenis,keterangan) 
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()

        return result
        

