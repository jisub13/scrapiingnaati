# scraper that dynamically scrapes naati database

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

# find number of pages so we know when to while loop too
number = 1
pages = 1
option_number = 1
options = 3
language = 1
# temporary list for each person
# holds as name, current certifications, location, phone, email and website
temp = []
# big list to hold everything
final_list = []
practitioner = "translator"
# loop through required options no languages should skip by doing an exception
while(option_number <= options):
    # opening option menus
    select = Select(driver.find_element_by_id('require'))
    # choosing a selection
    try:
        select.select_by_index(option_number)
    except NoSuchElementException:
        break
    # practitioner type
    practitioner_type = select.first_selected_option.text
    final_list.append(practitioner_type)
    language = 1
    # loop through languages and skip if no practitioners found (no languages found should skip)
    while(True):
        time.sleep(0.5)
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
        select_language = Select(driver.find_element_by_id('for-language'))
        #if no languages than next practitioner type
        try:
            select_language.select_by_index(language)
            language_type = select_language.first_selected_option.text
            final_list.append(language_type)
        except NoSuchElementException:
            break
        # clicking on submit button
        submit_button = driver.find_element_by_id('od-submit')
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        # wait till data loads
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
        # skip if no practitioners
        if driver.find_element_by_xpath('//*[@id="od-table-content"]').text == "No practitioner found.":
            language = language + 1
            continue
        # wait till data loads
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
        # find last page number
        try:
            page_number = int(driver.find_element_by_class_name('total-pages').text)
        except NoSuchElementException:
            page_number = 1
        pages = 1
        # loop through pages
        while (pages <= page_number):
            temp = []
            WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
            # wait until page loads
            # looping through actual practitiners
            while (number <= 5):
                try:
                    element = driver.find_element_by_xpath('//*[@id="od-table-content"]/div[{}]/div[1]/span/a'.format(number))
                except NoSuchElementException:
                    break
                #scrolling to each name
                driver.execute_script("arguments[0].scrollIntoView();", element)
                #clicking each name
                element.click()
                # wait till box loads
                WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="od-practitioner-modal"]/div/div')))
                # wait till information loads
                WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="od-practitioner-modal"]/div/div/div[2]/div[1]/img')))
                
                # name
                temp.append(driver.find_element_by_xpath('//*[@id="od-practitioner-name"]').text)
                # current certifications
                temp.append(driver.find_element_by_xpath('//*[@id="od-current-certifications"]').text)
                # location
                temp.append(driver.find_element_by_xpath('//*[@id="od-practitioner-location"]').text)
                # phone number
                temp.append(driver.find_element_by_xpath('//*[@id="od-practitioner-phone"]').text)
                # email
                temp.append(driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[2]/div[2]/div/div/div[5]/div/div').text)
                # website
                temp.append(driver.find_element_by_xpath('//*[@id="od-practitioner-website"]').text)
                
                # append to final list
                final_list.append(temp)
                # close the box
                driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[1]/button').click()
                # go to next contact
                number = number + 1
                # wait till box disappears
                WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="od-practitioner-modal"]/div')))
            try:
                # click the next page button
                next_button = driver.find_element_by_xpath('//*[@id="od-pagination-content"]/span/a[3]')
            except NoSuchElementException:
                break
            number = 1
            # go to the next page button
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            # click the next page button
            next_button.click()
            pages = pages + 1
        language = language + 1
    option_number = option_number + 1
print(final_list)