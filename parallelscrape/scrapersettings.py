from selenium import webdriver
# telling them to wait for at least a specific amount of time until somethign
from selenium.webdriver.support.wait import WebDriverWait
# occurs when it takes more time for the until event and if the element doesn't exist
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# condition (used here to check if something is loading)
from selenium.webdriver.support import expected_conditions as EC
# finding things by XPATH, ID, CLASS_NAME and other things
from selenium.webdriver.common.by import By
# for selecting options
from selenium.webdriver.support.ui import Select
import time

# for creating csv files
import csv

# create csv file in write mode
def scraper(data, language_index, practitioner):
    # settings you want to change sometimes

    # how long we wait for each setting
    delay = 10
    # calling the driver
    driver_path = "C:\\Users\\Nosar\\OneDrive\\Documents\\Projects\\LingoLedger\\individual\\msedgedriver\\msedgedriver.exe"
    # Naati Directory to scrape
    url = 'https://www.naati.com.au/online-directory/'
    fields = ['Name', 'Language', 'Current Certifications', 'Location', 'Phone', 'Email', 'Website', 'Past Credentials']

    # start of the actual function
    driver = webdriver.Edge(driver_path)
    driver.get(url)
    writer = csv.DictWriter(data, fieldnames=fields)
    # write headers
    writer.writeheader()
    # open chrome driver up - have to change this depending on user
    # user must also download their own drivers
    driver.get(url)
    # wait for the webpage to load before we scrape
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="require"]')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    # get rid of the cookies text
    driver.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click()
    number = 1
    pages = 1

    # opening option menus
    select = Select(driver.find_element_by_id('require'))
    # choose translator selection
    select.select_by_index(practitioner)

    # loop through languages and skip if no practitioners found (no languages found should skip)
    time.sleep(0.5)
    WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
    selected_language = Select(driver.find_element_by_id('for-language'))

    # select practitioner
    selected_language.select_by_index(language_index)
    language = selected_language.first_selected_option.text

    # clicking on submit button
    submit_button = driver.find_element_by_id('od-submit')
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    # wait till data loads
    WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))

    # wait till data loads
    WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))

    # find last page number
    page_number = int(driver.find_element_by_class_name('total-pages').text)
    pages = 1
    # loop through pages
    while (pages <= page_number):
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
        # wait until page loads
        # looping through actual practitiners
        while (number <= 5):
            # sometimes not exactly 5 per page
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
            # click for past credentials box
            past_cred_box = driver.find_element_by_xpath('//*[@id="modal"]/div[1]')
            driver.execute_script("arguments[0].scrollIntoView();", past_cred_box)
            past_cred_box.click()
            
            # name
            name = driver.find_element_by_xpath('//*[@id="od-practitioner-name"]').text
            # current certifications
            current_certs = driver.find_element_by_xpath('//*[@id="od-current-certifications"]').text
            # location
            location = driver.find_element_by_xpath('//*[@id="od-practitioner-location"]').text
            # phone number
            contact_number = driver.find_element_by_xpath('//*[@id="od-practitioner-phone"]').text
            # email
            email = driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[2]/div[2]/div/div/div[5]/div/div').text
            # website
            website = driver.find_element_by_xpath('//*[@id="od-practitioner-website"]').text
            #past naati credentials
            past_cred = driver.find_element_by_xpath('//*[@id="od-past-certifications"]').text

            # add to csv file
            writer.writerow({'Name' : name, 'Language': language, 'Current Certifications' : current_certs, 'Location' : location, 'Phone' : contact_number, 'Email' : email, 'Website': website,  'Past Credentials': past_cred})
            # close the box - seems to be a problem here I got to fix or not cause it works fine for another test
            driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[1]/button').click()
            # go to next contact
            number = number + 1
            # wait till box disappears
            WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="od-practitioner-modal"]/div')))
        try:
            # click the next page button
            next_button = driver.find_element_by_xpath('//*[@id="od-pagination-content"]/span/a[3]')
        except NoSuchElementException:
            # no next page button on the last page
            break
        number = 1
        # go to the next page button
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        # click the next page button
        next_button.click()
        pages = pages + 1
    print("All done!")