from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import os, time, random, csv

driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.maximize_window()
link = "https://www.dnb.com/business-directory/company-information.food_manufacturing.ca.ontario.html?page="
page= 9

to_scrape = link + str(page)
driver.get(to_scrape)
data=[]
businesses = driver.find_elements(By.XPATH, '//*[@id="companyResults"]/div[contains(@class, "data")]/div[1]/a')[1:]
for b in businesses:
    data.append([b.text])
locations = driver.find_elements(By.XPATH, '//*[@id="companyResults"]/div[contains(@class, "data")]/div[2]')[1:]
loc_data = []
for i in range(len(locations)):
    loc_data.append(locations[i].text.replace('\n', ' '))
revenues = driver.find_elements(By.XPATH, '//*[@id="companyResults"]/div[contains(@class, "data")]/div[3]')[1:]
for i, b in enumerate(businesses):
    time.sleep(1)
    driver.get(b.get_attribute('href'))
    time.sleep(300)
    

