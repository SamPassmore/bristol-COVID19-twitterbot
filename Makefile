DATA_REPO=https://github.com/emmadoughty/Daily_COVID-19.git

# install python venv and install python libraries
env:
	python -m venv env
	./env/bin/python ./env/bin/pip3 install -r requirements.txt
	
install: env
	git clone $(DATA_REPO)
	
update:
	cd ./Daily_COVID-19 && git pull $(DATA_REPO) && cd ..
	./env/bin/python bristol-covid19-bot.py


	
	