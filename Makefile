# Если хотете скачать вакансии с сайта hh.ru.
lv:
	python3 ./Back/main.py --load_vacancy all 

# Если хотите скачать только одно резюме.
lro:
	python3 ./Back/main.py --load_resume one

# Если хотите скачать больше одного резюме.
lrm:
	python3 ./Back/main.py --load_resume more

# Для предобработки одного резюме.
tp:
	python3 ./Back/main.py --text_preprocessor tp

# Для запуска моделей
model:
	python3 ./Back/main.py --load_model model

# Запуск тестового бота для разработки новых фич
startdev:
	cd ./Front && npm run dev

# Запуск бота для ПРОМа
startprod:
	cd ./Front && npm run prod

# Для использования на сервере или в других средах
# build:
# 	docker build  -t tgbot .

# run:
# 	docker run -d -p 3000:3000 --name tgbot --rm tgbot
	
# stop:
# 	docker stop tgbot

# vim ~/.bash_profile
# source ~/.bash_profile