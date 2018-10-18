import sys
import time
import telepot
# import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import per_chat_id, create_open, pave_event_space,include_callback_query_chat_id 
from dbhelper import dbhelper
db = dbhelper()

# data_edit = {}
# data_edit['name'] = 'Lala'
# data_edit['loker'] = 'ULI'
# data_edit['id'] = id_user

#edit_user = edit(data_edit)
# delete_user = delete(id_user)
# 

class HadirEvent(telepot.helper.ChatHandler):
    
    def __init__(self, *args, **kwargs):
        super(HadirEvent, self).__init__(*args, **kwargs)
        self._count = 0
        self._state = ''
        self._state_input = ''
        self.data_user = {}
        self._editor = ''
        self.keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='Daftar', callback_data='daftar'),
                    InlineKeyboardButton(text='Lihat Data', callback_data='lihatData'),
                    InlineKeyboardButton(text='Absen', callback_data='absen'),
                    InlineKeyboardButton(text='Order', callback_data='order'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
        self.loker = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='DAMAN', callback_data='daman'),
                    InlineKeyboardButton(text='AMO', callback_data='amo'),
                    InlineKeyboardButton(text='ASO', callback_data='aso'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
        self.unbind_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='Unbind', callback_data='unbind'),
                    # InlineKeyboardButton(text='Data', callback_data='data'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
        self.bind_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='Bind', callback_data='bind'),
                    ],
                    ]
                )
        self.absen_replykeyboard = ReplyKeyboardMarkup(keyboard=[
                     [KeyboardButton(text='Hadir', request_location=True)],
                 ],one_time_keyboard=True)
    def _cancel_last(self):
        if self._editor:
            self._editor.deleteMessage()
            self._editor = None
            self._edit_msg_ident = None

    def _cancel_markup(self):
        if self._editor:
            self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None

    def _send_message(self,text,markup=None):
        sent = self.sender.sendMessage(text,reply_markup=markup)
        self._editor = telepot.helper.Editor(self.bot, sent)

    def on_chat_message(self, msg):
        self._count += 1
        content_type, chat_type, chat_id = telepot.glance(msg)
        
        if self._state == 'daftar':
            if self._state_input == 'daftar': 
                self._cancel_last()
                self.data_user['nik'] = msg['text']
                if db.get_user('nik',self.data_user['nik']):
                    self._send_message('NIK anda sudah terdaftar.',self.bind_keyboard)
                else:
                    self._send_message('Masukkan Nama anda:')
                    self._state_input = 'nik'
                    
            elif self._state_input == 'nik':
                self.data_user['nama'] = msg['text']
                self._cancel_last()
                self._send_message('Masukkan Loker anda:')
                self._state_input = 'nama'
            elif self._state_input == 'nama':
                self.data_user['loker'] = msg['text']
                self._cancel_last()
                print(2)
                if self.data_user['nik'] and self.data_user['nama'] and self.data_user['loker']:
                    # id_user = 'u{}'.format(314)
                    print(3)
                    if not db.get_user('nik',self.data_user['nik']):
                        print(6)
                        # data['id_user'] = None
                        nik = self.data_user['nik']
                        name = self.data_user['nama']
                        loker = self.data_user['loker']
                        account_type = 'member'
                        created_at = 'CURRENT_TIMESTAMP'
                        insert_user = db.insert(nik,name,loker,account_type,created_at,chat_id)
                        self._send_message('Data anda tersimpan.',self.keyboard)
                        self._state = ''
                        self._state_input = 'loker'

                    else:
                        print(7)
                        sent = self.sender.sendMessage('Data nik anda telah.')
        elif self._state == 'absen':
            if self._state_input == 'absen': 
                self._cancel_last()
                self.data_user['kode_event'] = msg['text']
                self.id_user = db.get_user_telegram(chat_id)['id_user']
                self.event = db.get_event('id_event',self.data_user['kode_event'])
                if self.event:
                    if any(d.get('id_user') == self.id_user for d in db.get_event_user('id_event',self.data_user['kode_event'], 'id_user')):
                        self._send_message('{}\n{}\n{}\n{}'.format(self.event['event_name'],self.event['event_venue'],self.event['event_start'],self.event['event_end']))
                        if self.event['bot_absen'] == 1:
                            if not db.get_event_participant(self.event['id_event'],self.id_user):
                                self._send_message('Klik Hadir',self.absen_replykeyboard)                    
                                self._state_input = 'kode_event'
                            else:
                                self._send_message('Anda telah absen.',self.keyboard)
                                self._state = ''
                                self._state_input = ''
                        else:
                            self._send_message('Tidak dapat absen lewat bot.',self.keyboard)
                            self._state = ''
                            self._state_input = ''
                    else:
                        self._send_message('Anda tidak dapat absen untuk event tersebut.',self.keyboard)
                        self._state = ''
                        self._state_input = ''
                else:
                    self._send_message('Event tidak dikenali.',self.keyboard)
                    self._state = ''
                    self._state_input = ''
                    
            elif self._state_input == 'kode_event':
                location = msg['location']
                # self._cancel_last()
                check_radius = db.check_radius(location['latitude'],location['longitude'],self.event['latitude'],self.event['longitude'])

                if check_radius <= self.event['radius']:
                    db.insert_event_participant(self.event['id_event'],self.id_user,1)
                    self._send_message('Anda berhasil absen.',ReplyKeyboardRemove())
                else:
                    db.insert_event_participant(self.event['id_event'],self.id_user,2)
                    self._send_message('Lokasi anda terlalu jauh dari event. Anda harus berada dalam radius {} km. Untuk saat ini data anda tersimpan dengan status Di Luar Lokasi.'.format(self.event['radius']),ReplyKeyboardRemove())
                self._state = ''
                self._state_input = ''

        elif self._state == 'cek_event':
            location = msg['location']
            check_radius = db.check_radius(location['latitude'],location['longitude'],self.event['latitude'],self.event['longitude'])
            self._send_message(check_radius*1000)    
            self._state = ''
            self._state_input = ''
        else:
            if msg['text'].upper().startswith('/CEK'):
                kode_event = msg['text'].split(' ')[1]
                self._cancel_last()
                self.event = db.get_event('id_event',kode_event)
                if self.event:
                    self._send_message('{}\n{}\n{}\n{}'.format(self.event['event_name'],self.event['event_venue'],self.event['event_start'],self.event['event_end']))
                    self._send_message('Klik Hadir',self.absen_replykeyboard)                    
                    self._state = 'cek_event'
                else:
                    self._send_message('Event tidak dikenali.',self.keyboard)
                    self._state = ''
                    self._state_input = ''

            else:    
                self._send_message('Silahkan kaka ...',self.keyboard)
                self.close()

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data == 'daftar':
            self._cancel_markup()
            if not db.get_user_telegram(from_id):
                self._send_message('Masukkan NIK anda:')
                self._state = 'daftar'
                self._state_input = 'daftar'
            else:  
                self._state = None
                id_user = db.get_user_telegram(from_id)['id_user']
                print(id_user)
                nik = db.get_user('id_user',id_user)[0]['nik']
                self._send_message('Akun Telegram anda telah terhubung dengan NIK: {}'.format(nik),self.unbind_keyboard)
        elif query_data == 'lihatData':
            self._cancel_markup()
            user_telegram = db.get_user_telegram(from_id)
            if user_telegram:
                user = db.get_user('id_user',user_telegram['id_user'])  
                self._send_message('\
                    NIK------------:{}\nNama--------:{}\nLoker---------:{}'.format(user[0]['nik'],user[0]['name'],user[0]['loker']),self.keyboard)
            else:
                self._send_message('Anda belum terdaftar. Klik daftar.',self.keyboard)
        elif query_data == 'absen':
            self._cancel_markup()
            user_telegram = db.get_user_telegram(from_id)
            if user_telegram:
                self._send_message('Masukkan Kode Event:')
                self._state = 'absen'
                self._state_input = 'absen'
            else:
                self._send_message('Anda belum terdaftar. Klik daftar.',self.keyboard)

        elif query_data =='bind' :
            id_user = db.get_user('nik',self.data_user['nik'],'id_user')
            print(id_user)
            bind = db.bind(id_user[0]['id_user'],from_id)
            self._send_message('Bind berhasil.',self.keyboard)
            self._state = ''
        # elif query_data == 'order':
            
        elif query_data == 'unbind':
            unbind = db.unbind(from_id)
            self._send_message('Unbind berhasil.',self.keyboard)
            self._state = ''

# TOKEN = sys.argv[1]  # get token from command-line
if sys.version[0] == '3':
    # @developmentdamanbot
    TOKEN = '694699130:AAG4S3Tb9uxxxPHjbl5fP-QiNsjOehOhieM'
else:
    # @haeventbot
    TOKEN = '692089019:AAHR_d7I0VRer2BELku90RHlzP6m7fp14DY'

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
    pave_event_space())(
        per_chat_id(), create_open, HadirEvent, timeout=500
    ),
])

MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
