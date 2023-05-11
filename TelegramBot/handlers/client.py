from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Выбери результат какой модели хотите узнать.', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом возможно через ЛС.')

@dp.message_handler(commands=['TF-IDF'])
async def pizza_open_command(message: types.Message):
    with open('../AnalysisVR/bd_bot/tfidf.csv', 'r') as file:
        lines = file.readlines()
    table_lines = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        formatted_line = f"Название вакансии: {parts[1]}\nScore: {parts[2]}\nНазвание резюме: {parts[3]}\nСсылка на вакансию: {parts[4]}\nСсылка на резюме: {parts[5]}\n"
        table_lines.append(formatted_line)
    table = '\n'.join(table_lines)
    await message.answer(table)

@dp.message_handler(commands=['BOWords'])
async def pizza_open_command(message: types.Message):
    with open('../AnalysisVR/bd_bot/bowords.csv', 'r') as file:
        lines = file.readlines()
    table_lines = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        formatted_line = f"Название вакансии: {parts[1]}\nScore: {parts[2]}\nНазвание резюме: {parts[3]}\nСсылка на вакансию: {parts[4]}\nСсылка на резюме: {parts[5]}\n"
        table_lines.append(formatted_line)
    table = '\n'.join(table_lines)
    await message.answer(table)

@dp.message_handler(commands=['Word2Vec'])
async def pizza_open_command(message: types.Message):
    with open('../AnalysisVR/bd_bot/word2vec.csv', 'r') as file:
        lines = file.readlines()
    table_lines = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        formatted_line = f"Название вакансии: {parts[1]}\nScore: {parts[2]}\nНазвание резюме: {parts[3]}\nСсылка на вакансию: {parts[4]}\nСсылка на резюме: {parts[5]}\n"
        table_lines.append(formatted_line)
    table = '\n'.join(table_lines)
    await message.answer(table)

@dp.message_handler(commands=['DistilBERT'])
async def pizza_open_command(message: types.Message):
    with open('../AnalysisVR/bd_bot/distilbert.csv', 'r') as file:
        lines = file.readlines()
    table_lines = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        formatted_line = f"Название вакансии: {parts[1]}\nScore: {parts[2]}\nНазвание резюме: {parts[3]}\nСсылка на вакансию: {parts[4]}\nСсылка на резюме: {parts[5]}\n"
        table_lines.append(formatted_line)
    table = '\n'.join(table_lines)
    await message.answer(table)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['TF-IDF'])
    dp.register_message_handler(pizza_open_command, commands=['BOWords'])
    dp.register_message_handler(pizza_open_command, commands=['Word2Vec'])
    dp.register_message_handler(pizza_open_command, commands=['DistilBERT'])