from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd

options = Options()

options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

driver.get('https://priem.mirea.ru/accepted-entrants-list/')
time.sleep(2)

wait = WebDriverWait(driver, 10)
cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="css-bgi5uq"]/following-sibling::tr[1]')))
time.sleep(2)
url_list = [card.find_element(By.XPATH, './td/a').get_attribute('href') for card in cards]


driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 10)
books_list = []
print(len(url_list))

i=3

for url_item in url_list[0: i]:

    books_dict = {}



    driver2.get(url_item)
    try:
        name = wait2.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-bco1gb']/b[@class='chakra-text css-1ghp9xx']"))).text
    except Exception:
        name = None

    try:
        code = wait2.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-bco1gb']/i"))).text
    except Exception:
        code = None

    try:
        places = wait2.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1ilqeby']/b"))).text
    except Exception:
        places = None
    
    
    rows = len(driver2.find_elements(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr'))
   

    cols = len(driver2.find_elements(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr[1]/td'))

    for r in range(2, rows+1):
        number=driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[1]').text
        snils=driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[2]').text
        priority = driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[3]').text
        bally= driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[11]').text
        #time.sleep(1)
        books_list.append({
            'name': name.strip(),
            'code': code.strip(),
            'places': places.strip(),
            'N': number.strip(),
            'SNILS': snils.strip(),
            'priority': priority.strip(),
            'balls quantity': bally.strip()                      
            })
    time.sleep(3)

    driver2.quit()
    
   


df = pd.DataFrame(books_list)
print(df)

df.to_csv('file_resultSS'+str(i)+'.csv', encoding='utf-8-sig')

