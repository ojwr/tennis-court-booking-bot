import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
import sys

sleep_time = 3

#Load driver
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

#Load login page
driver.get('https://auth.clubspark.uk/account/signin?ReturnUrl=%2fissue%2fwsfed%3fwa%3dwsignin1.0%26wtrealm%3dhttps%253a%252f%252fclubspark.lta.org.uk%252f%26wctx%3drm%253d0%2526id%253d0%2526ru%253dhttps%25253a%25252f%25252fclubspark.lta.org.uk%25252f%26wct%3d2021-10-11T09%253a48%253a39Z%26prealm%3dhttps%253a%252f%252fclubspark.lta.org.uk%252f%26proot%3dhttps%253a%252f%252fclubspark.lta.org.uk%252f%26paroot%3dhttps%253a%252f%252fclubspark.lta.org.uk%252f%26source%3dch%26error%3dFalse%26message%3d&wa=wsignin1.0&wtrealm=https%3a%2f%2fclubspark.lta.org.uk%2f&wctx=rm%3d0%26id%3d0%26ru%3dhttps%253a%252f%252fclubspark.lta.org.uk%252f&wct=2021-10-11T09%3a48%3a39Z&prealm=https%3a%2f%2fclubspark.lta.org.uk%2f&proot=https%3a%2f%2fclubspark.lta.org.uk%2f&paroot=https%3a%2f%2fclubspark.lta.org.uk%2f&source=ch&error=False&message=')
time.sleep(sleep_time)

#Login
username = driver.find_element(By.NAME, 'EmailAddress')
password = driver.find_element(By.NAME, 'Password')
username.send_keys('XXXXX')
password.send_keys('XXXXX')
driver.find_element(By.ID, 'signin-btn').click()
time.sleep(sleep_time)

#Get time and date of court booking
start_time_24h = int(sys.argv[1])
try:
    day = int(sys.argv[2])
    month = int(sys.argv[3])
    year = int(sys.argv[4])
except:
    today = datetime.datetime.today()
    delta = datetime.timedelta(days=6) 
    date_in_one_week = today + delta
    year = date_in_one_week.year
    month = date_in_one_week.month
    day = date_in_one_week.day
if day < 10:
    day = '0' + str(date_in_one_week.day)

#Load court boooking page
driver.get(f"https://clubspark.lta.org.uk/KenningtonPark/Booking/BookByDate#?date={year}-{month}-{day}&role=guest")
time.sleep(sleep_time)

#Select numerical reference for chosen time
start_time_tag = 480 + (start_time_24h - 8) * 60
bookable_hours = 14

#Scroll to specified timing slot (does not work if slot if not on screen)
height = driver.execute_script("return document.body.scrollHeight") - 1080
scroll_height = int(round(height * ((start_time_24h - 8)/ bookable_hours)))
driver.execute_script(f'window.scrollTo(0, {scroll_height})') 
time.sleep(sleep_time)

#Courts listed in order of preference
court_dict = {
    #values represent HTML tag for each court
    'court 5': '12903ed0-496e-4da6-b5ed-83eafff703fc',
    'court 1': '48d10536-b799-4e21-868c-da7fb3fe43e0',
    'court 4': '48ce242f-d10d-43d7-ad21-92009296bd20',
    'court 3': '5d0109b3-9485-40cd-bc9b-2b0671fa459c',
    'court 2': 'e5416aea-0453-4bdd-b87c-b84afbad5213',
}

#Find a free court 
for court, court_tag in court_dict.items():
    print('Court number: ', court)
    try: 
        driver.find_element(By.CSS_SELECTOR, f'a[data-test-id="booking-{court_tag}|{year}-{month}-{day}|{start_time_tag}"]').click()
        time.sleep(sleep_time)
        try:
            driver.find_element(By.CSS_SELECTOR, f'button[id="submit-booking"]').click()
            break
        except:
            print(court, ' is already booked')
    #Court is a booking for longer than one hour so HTML reference is invalid
    except:
        print(court, ' is already booked')
    time.sleep(sleep_time)
         
#Enter payment details 
scroll_height = driver.execute_script("return document.body.scrollHeight") 
driver.execute_script(f'window.scrollTo(0, {scroll_height})') 

driver.find_element(By.CSS_SELECTOR, f'button[id="paynow"]').click()
time.sleep(sleep_time)

driver.find_element(By.CSS_SELECTOR, f'div[id="cs-stripe-elements-card-number"]').click()
card_number = "4242424242424242"
for number in card_number:
    ActionChains(driver).send_keys(int(number)).perform()   
time.sleep(sleep_time)

driver.find_element(By.CSS_SELECTOR, f'div[id="cs-stripe-elements-card-expiry"]').click()
card_expiry = "4242"
for number in card_expiry:
    ActionChains(driver).send_keys(int(number)).perform()
time.sleep(sleep_time)

driver.find_element(By.CSS_SELECTOR, f'div[id="cs-stripe-elements-card-cvc"]').click()
card_cvc = "424"
for number in card_cvc:
    ActionChains(driver).send_keys(int(number)).perform()
time.sleep(sleep_time)

#Confirm booking 
driver.find_element(By.CSS_SELECTOR, f'button[id="cs-stripe-elements-submit-button"]').click()