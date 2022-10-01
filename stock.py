from operator import truediv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import time

import configparser
config = configparser.ConfigParser()
config.read('stock.ini')
STOCK_LIST = config['setting']['STOCK_LIST']

options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
FILE_MODIFY = False
import json 
def get_json():
    with open('stock.json') as f:
        json_data = json.load(f)
    return json_data
def input_json(json_data, stock_num, time_stamp, price):
    global FILE_MODIFY
    if stock_num not in json_data:
        FILE_MODIFY = True
        json_data[stock_num] = {}
    if time_stamp not in json_data[stock_num]:
        print("Input new price")
        FILE_MODIFY = True
        json_data[stock_num][time_stamp] = price
    return json_data

def store_json(json_data):
    with open('stock.json', 'w') as fp:
        json.dump(json_data, fp)

def get_price(stock_num):
    chrome.get("https://invest.cnyes.com/twstock/TWS/{0}".format(stock_num))
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    time_tag = soup.find("time")
    time_stamp = time_tag.getText().split(" ")[0]

    price_tag = soup.find("div", {"class" : "info-lp"})
    price = price_tag.find("span").getText()

    return time_stamp, price

json_data = get_json()
print(json_data)
for stock_num in STOCK_LIST.split(","):
    time_stamp, price = get_price(stock_num)
    input_json(json_data, stock_num, time_stamp, price)
    time.sleep(1)

if FILE_MODIFY:
    print("Change Stock FILE")
    store_json(json_data)
else:
    print('Same data')
print("END!!!!!")
chrome.quit()