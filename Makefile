# Первая версия проекта.
# Если хотете скачать вакансии с сайта hh.ru.
lv:
	python3 main.py --load_vacancy all 

# Если хотите скачать только одно резюме.
lro:
	python3 main.py --load_resume one

# Если хотите скачать больше одного резюме.
lrm:
	python3 main.py --load_resume more

# Для предобработки одного резюме.
tpor:
	python3 main.py --text_preprocessor one_resume

# Для предобработки множества резюме.
tpmo:
	python3 main.py --text_preprocessor more_resumes

# Для предобработки множества вакансий.
tpv:
	python3 main.py --text_preprocessor vacancyes

# Для запуска модели Tfidf.
tfidf:
	python3 main.py --load_model tfidf

# Для запуска модели BoW.
bow:
	python3 main.py --load_model bow

# Для запуска модели Word2Vec.
w2v:
	python3 main.py --load_model w2v

# Для запуска модели DistilBert.
db:
	python3 main.py --load_model dbert

# Для активации телеграм-бота.
botver1:
	sh ./TelegramBot/config/bot_run.sh