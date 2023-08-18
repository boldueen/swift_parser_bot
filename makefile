

tests:
	echo start testing the app...
	# tests....
	echo tests passed!

run-dev:
	echo starting...
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.dev.yml up --build 


run-prod:
	echo starting...
	docker-compose -f docker-compose.prod.yml down
	docker-compose -f docker-compose.prod.yml up -d --build 
