## Programming vacancies compare
The program parses two most popular job sites: [HeadHunter](https://hh.ru/) and [SuperJob](https://www.superjob.ru/). 
It's return statistics on offered salaries (in RUR) by vacancies in the 10 most popular programming languages.


## How to install
Python3 should already be installed. Use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```    
For using you also need your TOKEN from [SuperJob](https://api.superjob.ru/).
You should use environment variables. Create file name `.env` and variable SUPERJOB_TOKEN in the root directory.
In file `.env` only one line:
```
SUPERJOB_TOKEN='Here is your personal TOKEN'
```
Example for command line:
```
$ \programmer_salary> py main.py
```


## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).