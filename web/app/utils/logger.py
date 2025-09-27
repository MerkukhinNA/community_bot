# import datetime
# import functools
# import os
# import traceback
# import telebot
# from telebot.types import Message, CallbackQuery
# from modules.UserDataStorage.DataBaseManager import db 
# from modules.UserDataStorage.models import sqlalchemy, Log


# class Logger:
#     bot = telebot.TeleBot(os.environ.get("PRODUCTION_TOKEN"))
#     chat_chanel = os.environ.get("CHANEL_WARN")

#     @staticmethod
#     def log(text, service="BOTGENERAL", chat_id=-1, level="INFO", user_id=-1, auth=True):
#         if auth:
#             user_id = db.get_user_by_chat_id(chat_id).user_id if chat_id != -1 and user_id == -1 and db.get_user_by_chat_id(chat_id) else -1
#             db.execute_with_commit(
#             sqlalchemy.insert(Log).
#             values(datetime=datetime.datetime.now(), 
#                    level=level, user_id=user_id, service=service, text=text))
#         message = f"[{level}] {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | {text}"
#         print(message)
        
#     def error_redirect_call(self, func):
#         @functools.wraps(func)
#         def wrap(call: CallbackQuery):
#             try:
#                 result = func(call)
#                 return result
#             except Exception as e:
#                 self.send_message_with_error(e, call.message)
#         return wrap

#     def error_redirect_message(self, func):
#         @functools.wraps(func)
#         def wrap(message):
#             try:
#                 result = func(message)
#                 return result
#             except Exception as e:
#                 self.send_message_with_error(e, message)
#         return wrap

#     def send_message_with_error(self, exception, message):
#         print("==========================ERROR============================")
#         print(traceback.format_exc())
#         print(exception)
#         Logger.log(f"Bot internal error", level="ERROR")
#         self.send_traceback(traceback.format_exc())
#         self.bot.send_message(self.chat_chanel, f'{exception}\nѕользователь: {message.from_user.id}\n—ообщение: {message.text}')

#         self.bot.send_message(message.chat.id, f"Ќепредвиденна€ ошибка\nЌапишите или нажмите '/start' дл€ перезапуска бота")

#     def send_traceback(self, text):
#         if len(text) <= 4000:
#             self.bot.send_message(self.chat_chanel, text)
#             return
#         self.bot.send_message(self.chat_chanel, text[:4000])
#         self.send_traceback(text[4000:])