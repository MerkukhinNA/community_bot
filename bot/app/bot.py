import os, telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery


class Bot:
   
    def __init__(self):
        print(f"-----bot-launched-----")
        self._bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
    
        # @Logger().error_redirect_message
        @self._bot.message_handler(commands=['start'])
        def haldle_commands(message: Message) -> None:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text='Открыть', url=os.environ['TG_APP_URL']))
            self._bot.send_message(
                chat_id=message.from_user.id,
                text='Приложение бота',
                reply_markup=keyboard
            )
        
        self._bot.delete_my_commands()
        self._bot.polling(none_stop=True, interval=0)