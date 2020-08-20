#DATA_REPO=https://github.com/emmadoughty/Daily_COVID-19.git
DATA_REPO=https://github.com/tomwhite/covid-19-uk-data.git
DATA_DIR=covid-19-uk-data/

# install python venv and install python libraries
env:
	python -m venv env
	./env/bin/python ./env/bin/pip3 install -r requirements.txt
	
# install: env
# 	git clone $(DATA_REPO)
	
update:
# 	cd $(DATA_DIR) && git pull $(DATA_REPO) && cd ..
	RScript get_dataR.R
	./env/bin/python bristol-covid19-bot.py


	
	