from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/TF-IDF')
b2 = KeyboardButton('/BOWords')
b3 = KeyboardButton('/Word2Vec')
b4 = KeyboardButton('/DistilBERT')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1,b2).row(b3, b4)