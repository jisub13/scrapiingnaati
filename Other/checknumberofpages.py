# scraper that dynamically scrapes naati database
# creates three different csv files for translators, interpreters and death interepreters
# most important and basically brings everything
from selenium import webdriver
# telling them to wait for at least a specific amount of time until somethign
from selenium.webdriver.support.wait import WebDriverWait
# occurs when it takes more time for the until event
from selenium.common.exceptions import TimeoutException
# importing error when something doesn't exist
from selenium.common.exceptions import NoSuchElementException
# condition (used here to check if something is loading)
from selenium.webdriver.support import expected_conditions as EC
# finding things by XPATH, ID, CLASS_NAME and other things
from selenium.webdriver.common.by import By
# selecting options
from selenium.webdriver.support.ui import Select
import time

# for creating csv files
import csv
from datetime import datetime
# get todays date and time
todaydate = datetime.now().strftime("%d_%m_%Y__%H%M")
print(todaydate)
# open chrome driver up - have to change this depending on user
# user must also download their own drivers
driver = webdriver.Chrome("C:\\Users\\Nosar\\Downloads\\chromedriver_win32\\chromedriver")
driver.get('https://www.naati.com.au/online-directory/')

# max wait time for loading
# if wait is longer than 10 seconds i think it crashes
delay = 10 # seconds

# wait for the webpage to load before we scrape
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="require"]')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

number = 1
pages = 1
option_number = 1
options = 3
# loop through required options no languages should skip by doing an exception
while(option_number <= options):
    if (option_number == 1):
        print("translator")
    elif (option_number == 2):
        print("interpreter")
    elif(option_number == 3):
        print("deaf writer")
    # opening option menus
    select = Select(driver.find_element_by_id('require'))
    # choosing a selection
    select.select_by_index(option_number)
    # if option = 1 than translater file
    language_index = 1
    # loop through languages and skip if no practitioners found (no languages found should skip)
    time.sleep(0.5)
    while(True):
        #optimise this??
#        time.sleep(0.5)
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
        selected_language = Select(driver.find_element_by_id('for-language'))
        #if no languages than next practitioner type
        try:
            selected_language.select_by_index(language_index)
            language = selected_language.first_selected_option.text
        except NoSuchElementException:
            break
        # clicking on submit button
        submit_button = driver.find_element_by_id('od-submit')
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        # wait till data loads
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
        # find last page number
        try:
            page_number = int(driver.find_element_by_class_name('total-pages').text)
        except NoSuchElementException:
            # pages with only 1 page has no end number
            page_number = 1
        if (page_number >= 20):
            print( "Selection Index" + str(language_index) + " Language: " + language + "    Pages: " + str(page_number))
        language_index = language_index + 1
    option_number = option_number + 1

# close all the files at the end
print("All done!")
print(datetime.now().strftime("%d/%m/%Y__%H:%M"))