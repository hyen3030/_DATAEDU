from bs4 import BeautifulSoup
from matplotlib.textpath import text_to_path
import requests, json, re, time, datetime, random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
import sys
import os
import warnings
warnings.filterwarnings('ignore')


def get_text(url):
      #url = 'https://www.bigkinds.or.kr/v2/news/newsDetailView.do?newsId=01500601.20200630141654001'
      options=webdriver.ChromeOptions()
      options.add_argument('headless')
      service = Service('./chromedriver.exe')
      driver = webdriver.Chrome(service=service, options=options)
      driver.get(url)
      req = requests.get(url)
      soup = BeautifulSoup(req.text, "html.parser")

      text = driver.find_element(By.ID, 'content').text
      #print(text)
      return text