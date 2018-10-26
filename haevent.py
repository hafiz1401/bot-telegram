import sys
import time
import telepot
# import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import per_chat_id, create_open, pave_event_space,include_callback_query_chat_id 
from dbhelper import *
db = dbhelper()
db_user = User()
db_order = Order()
db_guest = Guest()

class HadirEvent(telepot.helper.ChatHandler):
    
    def __init__(self, *args, **kwargs):
        super(HadirEvent, self).__init__(*args, **kwargs)
        self._state = ''
        self._state_input = ''
        self.data_user = {}
        self._editor = ''
        self.daftar_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='Daftar', callback_data='daftar'),
                    ],]
                )
        self.keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='Lihat Data', callback_data='lihatdata'),
                    InlineKeyboardButton(text='Absen', callback_data='absen'),
                    InlineKeyboardButton(text='Order', callback_data='order'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
        self.lihatdata_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='Unbind', callback_data='daftar'),
                    InlineKeyboardButton(text='Absen', callback_data='absen'),
                    InlineKeyboardButton(text='Order', callback_data='order'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
        self.loker_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='DAMAN', callback_data='orderdaman'),
                    InlineKeyboardButton(text='AMO', callback_data='orderamo'),
                    InlineKeyboardButton(text='ASO', callback_data='orderaso'),
                    ],
                    ]
                )
        self.orderdaman_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='RT/Bukis', callback_data='rt_bukis'),
                    ],[
                    InlineKeyboardButton(text='Modifikasi', callback_data='modifikasi'),
                    ],[
                    InlineKeyboardButton(text='Migrasi', callback_data='migrasi'),
                    ],[
                    InlineKeyboardButton(text='Migrasi Modifikasi', callback_data='migrasi_modifikasi'),
                    ],[
                    InlineKeyboardButton(text='Add service + Migrasi', callback_data='addservice_migrasi'),
                    ],[
                    InlineKeyboardButton(text='Add service + Modifikasi', callback_data='addservice_modifikasi'),
                    ],[
                    InlineKeyboardButton(text='Add service + Migrasi + Modifikasi', callback_data='addservice_migrasi_modifikasi'),
                    ],[
                    InlineKeyboardButton(text='Add service', callback_data='addservice'),
                    ],
                    ]
                )

        self.unbind_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='Unbind', callback_data='unbind'),
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
        content_type, chat_type, chat_id = telepot.glance(msg)
        
        
        if not db.get_user_telegram(chat_id):
            if self._state == '':
                if msg['text'].upper().startswith('/GUEST'):
                    kode_event = msg['text'].split(' ')[1]
                    self.event = db.get_event('id_event',kode_event)
                    print (self.event)
                    if self.event:
                        self._send_message('{}\n{}\n{}\n{}'.format(self.event['event_name'],self.event['event_venue'],self.event['event_start'],self.event['event_end']))
                        self._send_message('Masukkan NIK anda:',)                    
                        self._state = 'absen_guest'
                        self._state_input = 'absen_guest'
                    else:
                        self._send_message('Event tidak dikenali.',self.keyboard)
                        self._state = ''
                        self._state_input = ''
                else:
                    self._send_message('Anda belum terdaftar. Klik daftar.',self.daftar_keyboard)
            elif self._state == 'daftar':
                if self._state_input == 'daftar': 
                    self._cancel_last()
                    self.data_user['nik'] = msg['text']
                    if db_user.get_user('nik',self.data_user['nik']):
                        self._send_message('NIK anda sudah terdaftar.',self.bind_keyboard)
                    else:
                        self._send_message('Masukkan nama anda:')
                        self._state_input = 'nik'
                        
                elif self._state_input == 'nik':
                    self.data_user['nama'] = msg['text']
                    self._cancel_last()
                    self._send_message('Masukkan loker anda:')
                    self._state_input = 'nama'
                elif self._state_input == 'nama':
                    self.data_user['loker'] = msg['text']
                    self._cancel_last()
                    if self.data_user['nik'] and self.data_user['nama'] and self.data_user['loker']:
                        nik = self.data_user['nik']
                        name = self.data_user['nama']
                        loker = self.data_user['loker']
                        account_type = 'member'
                        created_at = 'CURRENT_TIMESTAMP'
                        insert_user = db_user.insert(nik,name,loker,account_type,created_at,chat_id)
                        self._send_message('Data anda tersimpan.',self.keyboard)
                        self._state = ''
                        self._state_input = ''
            elif self._state == 'absen_guest':
                if self._state_input == 'absen_guest':
                    self._cancel_last()
                    self.data_user['nik_guest'] = msg['text']
                    self._send_message('Masukkan nama anda:')
                    self._state_input = 'nik_guest'                    
                elif self._state_input == 'nik_guest':
                    self._cancel_last()
                    self.data_user['nama_guest'] = msg['text']
                    self._send_message('Masukkan nama instansi anda:')
                    self._state_input = 'nama_guest'  
                elif self._state_input == 'nama_guest':
                    self._cancel_last()
                    self.data_user['instansi_guest'] = msg['text']
                    self._send_message('Klik Hadir',self.absen_replykeyboard)
                    self._state_input = 'instansi_guest'  

                elif self._state_input == 'instansi_guest':
                    location = msg['location']
                    self._cancel_last()
                    check_radius = db.check_radius(location['latitude'],location['longitude'],self.event['latitude'],self.event['longitude'])
                    id_event = self.event['id_event']
                    nik_guest = self.data_user['nik_guest']
                    nama_guest = self.data_user['nama_guest']
                    instansi_guest = self.data_user['instansi_guest']
                    if check_radius <= self.event['radius']:
                        hadir = 1
                        resp = 'Anda berhasil absen.'
                    else:
                        hadir = 2
                        resp = 'Lokasi anda terlalu jauh dari event. Anda harus berada dalam radius {} km. Untuk saat ini data anda tersimpan dengan status Di Luar Lokasi.'.format(self.event['radius'])
                    
                    db_guest.insert_event_guest(id_event,nik_guest,nama_guest,instansi_guest,hadir)
                    self._send_message(resp,ReplyKeyboardRemove())
                    self._state = ''
                    self._state_input = ''


        else:
            self.data_user['id_user'] = db.get_user_telegram(chat_id)['id_user']
            if self._state == 'absen':
                if self._state_input == 'absen': 
                    self._cancel_last()
                    self.data_user['kode_event'] = msg['text']
                    self.event = db.get_event('id_event',self.data_user['kode_event'])
                    if self.event:
                        if any(d.get('id_user') == self.data_user['id_user'] for d in db.get_event_user('id_event',self.data_user['kode_event'], 'id_user')):
                            self._send_message('{}\n{}\n{}\n{}'.format(self.event['event_name'],self.event['event_venue'],self.event['event_start'],self.event['event_end']))
                            if self.event['bot_absen'] == 1:
                                if not db.get_event_participant(self.event['id_event'],self.data_user['id_user']):
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
                        self._send_message('Event tidak dikenali. Perhatikan waktu mulai event.',self.keyboard)
                        self._state = ''
                        self._state_input = ''
                        
                elif self._state_input == 'kode_event':
                    location = msg['location']
                    # self._cancel_last()
                    check_radius = db.check_radius(location['latitude'],location['longitude'],self.event['latitude'],self.event['longitude'])

                    if check_radius <= self.event['radius']:
                        db.insert_event_participant(self.event['id_event'],self.data_user['id_user'],1)
                        self._send_message('Anda berhasil absen.',ReplyKeyboardRemove())
                    else:
                        db.insert_event_participant(self.event['id_event'],self.data_user['id_user'],2)
                        self._send_message('Lokasi anda terlalu jauh dari event. Anda harus berada dalam radius {} km. Untuk saat ini data anda tersimpan dengan status Di Luar Lokasi.'.format(self.event['radius']),ReplyKeyboardRemove())
                    self._state = ''
                    self._state_input = ''

            elif self._state == 'cek_event':
                location = msg['location']
                check_radius = db.check_radius(location['latitude'],location['longitude'],self.event['latitude'],self.event['longitude'])
                self._send_message(check_radius*1000)    
                self._state = ''
                self._state_input = ''

            elif self._state == 'orderdaman':
                self._cancel_last()
                client = db_user.get_user('id_user',self.data_user['id_user'])
                loker_tujuan = 1
                order_by = self.data_user['id_user']
                order = msg['text']
                jenis = self._state_input
                db_order.insert(loker_tujuan,order_by,order,jenis)
                self._send_message('Order tersimpan.',self.keyboard)
                self._state = ''
                self._state_input = ''
            else:
                if msg['text'].upper().startswith('/GUEST'):
                    kode_event = msg['text'].split(' ')[1]
                    self.event = db.get_event('id_event',kode_event)
                    print (self.event)
                    if self.event:
                        self._send_message('{}\n{}\n{}\n{}'.format(self.event['event_name'],self.event['event_venue'],self.event['event_start'],self.event['event_end']))
                        self._send_message('Masukkan NIK anda:',)                    
                        self._state = 'absen_guest'
                        self._state_input = 'absen_guest'
                    else:
                        self._send_message('Event tidak dikenali.',self.keyboard)
                        self._state = ''
                        self._state_input = ''
                elif msg['text'].upper().startswith('/CEK'):
                    kode_event = msg['text'].split(' ')[1]
                    self._cancel_markup()
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
                nik = db_user.get_user('id_user',id_user)[0]['nik']
                self._send_message('Akun Telegram anda telah terhubung dengan NIK: {}'.format(nik),self.unbind_keyboard)
        elif query_data == 'lihatdata':
            self._cancel_markup()
            user_telegram = db.get_user_telegram(from_id)
            user = db_user.get_user('id_user',user_telegram['id_user'])  
            self._send_message('\
                NIK------------:{}\nNama--------:{}\nLoker---------:{}'.format(user[0]['nik'],user[0]['name'],user[0]['loker']),self.lihatdata_keyboard)
        elif query_data == 'absen':
            self._cancel_markup()
            self._send_message('Masukkan Kode Event:')
            self._state = 'absen'
            self._state_input = 'absen'
                

        elif query_data =='bind' :
            id_user = db_user.get_user('nik',self.data_user['nik'],'id_user')
            bind = db.bind(id_user[0]['id_user'],from_id)
            self._send_message('Bind berhasil.',self.keyboard)
            self._state = ''
        elif query_data == 'order':
            self._cancel_markup()
            self._send_message('Klik loker tujuan.',self.loker_keyboard)
            self._state = 'order'
        
        

        elif query_data == 'orderdaman':
            self._cancel_markup()
            self._send_message('Klik jenis order.',self.orderdaman_keyboard)
            self._state = 'orderdaman'
        elif query_data == 'rt_bukis':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'rt_bukis'
        elif query_data == 'modifikasi':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'modifikasi'
        elif query_data == 'migrasi':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'migrasi'
        elif query_data == 'migrasi_modifikasi':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'migrasi_modifikasi'
        elif query_data == 'addservice_migrasi':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'addservice_migrasi'
        elif query_data == 'addservice_modifikasi':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'addservice_modifikasi'
        elif query_data == 'addservice_migrasi_modifikasi':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'addservice_migrasi_modifikasi'
        elif query_data == 'addservice':
            self._cancel_markup()
            self._send_message('Masukkan nomor pelanggan.')
            self._state_input = 'addservice'
        

        elif query_data == 'unbind':
            unbind = db.unbind(from_id)
            self._send_message('Unbind berhasil.',self.daftar_keyboard)
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
