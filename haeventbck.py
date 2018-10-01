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
    reg_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='NIK', callback_data='nik'),
                    InlineKeyboardButton(text='Password', callback_data='password'),
                    InlineKeyboardButton(text='Nama', callback_data='nama'),
                    InlineKeyboardButton(text='Loker', callback_data='loker'),
                    InlineKeyboardButton(text='Daftar', callback_data='daftar'),
                    # InlineKeyboardButton(text='Data', callback_data='data'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
    unbind_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='Unbind', callback_data='unbind'),
                    # InlineKeyboardButton(text='Data', callback_data='data'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )
    def __init__(self, *args, **kwargs):
        super(HadirEvent, self).__init__(*args, **kwargs)
        self._count = 0
        self._state = ''
        self._state_input = ''
        self.data_user = {}
        self._editor = ''

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

    def on_chat_message(self, msg):
        self._count += 1
        # self.sender.sendMessage(self._count)
        content_type, chat_type, chat_id = telepot.glance(msg)
        # if self._state == '':
            # self.sender.sendMessage(
            #     'Press Register to register ...',
            #     reply_markup=InlineKeyboardMarkup(
            #         inline_keyboard=[[
            #             InlineKeyboardButton(text='REGISTER', callback_data='register'),
            #         ]]
            #     )
            # )
        if msg['text'] == 'Daftar':
            id_telegram = db.get_all_id_telegram()
            if not db.contains(chat_id, id_telegram):
                self._state = 'daftar'
                sent = self.sender.sendMessage(
                    '\
                    NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
                    self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
                    reply_markup=self.reg_keyboard
                )
                self._editor = telepot.helper.Editor(self.bot, sent)
            else:  
                self._state = 'daftar'
                id_user = db.get_user_telegram(chat_id)
                nik = db.get_user(id_user[0][1])[0][1]
                sent = self.sender.sendMessage('Akun Telegram anda telah terhubung dengan NIK: {}'.format(nik),
                    reply_markup=self.unbind_keyboard)
                self._editor = telepot.helper.Editor(self.bot, sent)

        elif msg['text'] == 'Lihat Data':
            sent = self.sender.sendMessage('\
                NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
                self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')))

        elif self._state == 'daftar':
            # print (msg)
            if self._state_input == 'nik':                
                nik = db.get_all_nik()
                if not db.contains(msg['text'], nik):
                    self.data_user['nik'] = msg['text']
                    self._editor.deleteMessage()
                    sent = self.sender.sendMessage(
                    '\
                    NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
                    self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
                    reply_markup=self.reg_keyboard
                    )
                    self._editor = telepot.helper.Editor(self.bot, sent)



            elif self._state_input == 'password':
                self.data_user['password'] = msg['text']
                self._editor.deleteMessage()
                '\
                NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
                self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
                reply_markup=self.reg_keyboard
                )
                self._editor = telepot.helper.Editor(self.bot, sent)
            elif self._state_input == 'nama':
                self.data_user['nama'] = msg['text']
                self._editor.deleteMessage()
                sent = self.sender.sendMessage(
                '\
                NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
                self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
                reply_markup=self.reg_keyboard
                )
                self._editor = telepot.helper.Editor(self.bot, sent)
            elif self._state_input == 'loker':
                self.data_user['loker'] = msg['text']
                self._editor.deleteMessage()
                sent = self.sender.sendMessage(
                '\
                NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
                self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
                reply_markup=self.reg_keyboard
                )
                self._editor = telepot.helper.Editor(self.bot, sent) 
            # elif self._state_input == 'daftar':
            #     # self.data_user['loker'] = msg['text']
            #     self._editor.deleteMessage()
                # self.sender.sendMessage('Data anda '+self.data_user)   
            # self.sender.sendMessage(
            #     'Klik',
            #     reply_markup=self.reg_keyboard
            # )
        elif msg['text'] == 'Hadir':
            user = db.get_user_telegram(chat_id)
            self._state_input = 'hadir'
            # self.data_user['nik'] = msg['text']
            # self._editor.deleteMessage()
            sent = self.sender.sendMessage('Masukkan OTP: ')
            # sent = self.sender.sendMessage(
            # '\
            # NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
            # self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
            # reply_markup=self.reg_keyboard
            # )
            self._editor = telepot.helper.Editor(self.bot, sent)
        elif self._state_input == 'hadir':
            try:
                event = db.get_event_by_otp(msg['text'])
                # print (event)
                if event[0][0]:
                    print(event[0][0])
                    data = {}
                    data['id_event'] = event[0][0]
                    data['id_user'] = db.get_user_telegram(chat_id)[0][1]
                    db.insert_event_participant(data)
            except:        
                self.sender.sendMessage('Masukkan OTP: ')

        else:
            markup = ReplyKeyboardMarkup(keyboard=[
                     ['Daftar', KeyboardButton(text='Ubah Data')],
                     [KeyboardButton(text='Lihat Data'), KeyboardButton(text='Hadir', request_location=False)],
                 ])
            
            sent = self.sender.sendMessage(
                'Press something',
                reply_markup=markup
            )
            self._editor = telepot.helper.Editor(self.bot, sent)
            # self._cancel_last()
            self.close()

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        # if query_data == 'daftar':
        #     self._state = 'daftar'
        #     self.sender.sendMessage(
        #         'Klik',
        #         reply_markup=self.reg_keyboard
        #     )
        # print(self._state)
        if self._state == 'daftar':
            if query_data == 'nik':
                self._state_input = 'nik'
                self._cancel_last()
                sent = self.sender.sendMessage('Masukkan NIK anda: ')
                self._editor = telepot.helper.Editor(self.bot, sent)
            elif query_data == 'password':
                self._state_input = 'password'
                self._cancel_last()
                sent = self.sender.sendMessage('Masukkan Pasword anda: ')
                self._editor = telepot.helper.Editor(self.bot, sent)
            elif query_data == 'nama':
                self._state_input = 'nama'
                self._cancel_last()
                sent = self.sender.sendMessage('Masukkan Nama anda: ')
                self._editor = telepot.helper.Editor(self.bot, sent)
            elif query_data == 'loker':
                self._state_input = 'loker'
                self._cancel_last()
                sent = self.sender.sendMessage('Masukkan Loker anda: ')
                self._editor = telepot.helper.Editor(self.bot, sent)
            elif query_data == 'daftar':
                self._state_input = 'daftar'
                self._cancel_last()
                print(2)
                if len(self.data_user) == 4:
                    # id_user = 'u{}'.format(314)
                    print(3)
                    nik = db.get_all_nik()
                    if not db.contains(self.data_user['nik'], nik):
                        print(6)
                        data = {}
                        # data['id_user'] = None
                        data['nik'] = self.data_user['nik']
                        data['password'] = self.data_user['password']
                        data['name'] = self.data_user['nama']
                        data['loker'] = self.data_user['loker']
                        data['account_type'] = 'MEMBER'
                        data['created_at'] = 'CURRENT_TIMESTAMP'
                        chat_id = from_id
                        insert_user = db.insert(data,chat_id)
                        sent = self.sender.sendMessage('Data anda tersimpan. {}'.format(insert_user))
                        self._editor = telepot.helper.Editor(self.bot, sent)
                        self._state = ''

                    else:
                        print(7)
                        sent = self.sender.sendMessage('Data nik anda telah . {}'.format(insert_user))
            elif query_data == 'unbind':
                print (from_id)
                unbind = db.unbind(from_id)
                sent = self.sender.sendMessage('Unbind berhasil. {}'.format(unbind))
                self._editor = telepot.helper.Editor(self.bot, sent)
                self._state = ''


        # elif query_data == 'data':
        #     sent = self.sender.sendMessage('\
        #         NIK------------:{}\n\
        #         Password---:{}\n\
        #         Nama--------:{}\n\
        #         Loker---------:{}'.format(self.data_user.get('nik'),
        #         self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')))

# TOKEN = sys.argv[1]  # get token from command-line
TOKEN = '692089019:AAHR_d7I0VRer2BELku90RHlzP6m7fp14DY'
bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
    pave_event_space())(
        per_chat_id(), create_open, HadirEvent, timeout=100
    ),
])


MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
