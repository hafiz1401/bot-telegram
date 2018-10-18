import json
import requests
import time
import urllib
import re
import requests
import threading
import time
from dbhelper import dbhelper
db = dbhelper()
# @developmentdamanbot:
TOKEN = "692089019:AAHR_d7I0VRer2BELku90RHlzP6m7fp14DY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
exitflag = 0

class theThread(threading.Thread):
    def __init__(self, threadID, name, message,chat_id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.message = message
        self.chat_id = chat_id

    def run(self):
        print("Starting "+self.name)
        send_message(self.message,self.chat_id)
        print("Exiting "+self.name)

### Fungsi untuk mengambil respon dari URL yang kita akses
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

### Karena respon dari telegram memiliki format json, sehingga perlu diload supaya memudakan pembacaan di python 
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

### Fungsi untuk mendapatkan update yang masuk pada bot telegram
def get_updates(offset = None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

### Fungsi untuk mengambil id dari update terakhir
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

### Fungsi untuk mengirim pesan
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text.encode('utf-8', 'strict'))
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
### Fungsi untuk mengirim lokasi
def send_location(chat_id, latitude, longitude):
    url = URL + "sendLocation?chat_id={}&latitude={}&longitude={}".format(chat_id, latitude, longitude)
    get_url(url)

### Fungsi untuk membuat keyboard tambahan
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup, ensure_ascii = True)

## Fungsi utama yang memulai serangkaian perintah lainnya
def main():
    print('Running')
    from datetime import datetime
    while True:
        to_broadcast =  db.get_broadcast()
        thread = []
        pos = 0
        # print(datetime.now())
        for each in to_broadcast:
            # send_message(each['message'],each['chat_id'])
            thread.append(theThread(pos,'Thread-'+str(pos),each['message'],each['chat_id']))
            db.delete_broadcast(each['id_broadcast'])
            pos+=1
        # print(datetime.now())
        before = datetime.now()
        for each in thread:
            each.start()
        for each in thread:
            each.join()
        after = datetime.now()
        # print(after-before)
    print('Exiting')  
if __name__ == '__main__':
    main()
