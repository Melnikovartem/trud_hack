from selenium import webdriver
from parsel import Selector
import time
import ParseFromLinkedin
import json
from pathlib import Path

path = Path('names.txt')
names = [
	"Вера", 
	"Анатолий", 
	"Максим", 
	"Александр", 
	"Андрей", 
	"Владислав", 
	"Вадим", 
	"Демид", 
	"Денис", 
	"Глеб", 
	"Геннадий", 
	"Вячеслав", 
	"Павел",
	"Семён",
	"Арсен",
	"Станислав",
	"Федор",
	"Ярослав",
	"Яков",
	"Тимофей",
	"Юрий",
	"Ростислав",
	"Марк",
	"Иннокентий",
	"Захар"
]
res = []
ParseFromLinkedin.enter()
for name in names:
    print(name)
    res += ParseFromLinkedin.search_and_get(name, 'менеджер')
    path = Path('users_id_workers1.txt')
    path.write_text(json.dumps(res, indent=2), encoding='utf-8')


