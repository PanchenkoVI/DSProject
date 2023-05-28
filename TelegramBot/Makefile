startdev:
	npm run dev

startprod:
	npm run prod

build:
	docker build  -t tgbot .

run:
	docker run -d -p 3000:3000 --name tgbot --rm tgbot
	
stop:
	docker stop tgbot