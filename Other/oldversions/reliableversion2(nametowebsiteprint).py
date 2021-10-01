# scraper that dynamically scrapes naati database

# most important and basically brings everything
from selenium import webdriver
# telling them to wait for at least a specific amount of time until somethign
from selenium.webdriver.support.wait import WebDriverWait
# occurs when it takes more time for the until event
from selenium.common.exceptions import TimeoutException
# condition (used here to check if something is loading)
from selenium.webdriver.support import expected_conditions as EC
# finding things by XPATH, ID, CLASS_NAME and other things
from selenium.webdriver.common.by import By

# open chrome driver up - have to change this depending on user
# user must also download their own drivers
driver = webdriver.Chrome("C:\\Users\\Nosar\\Downloads\\chromedriver_win32\\chromedriver")
driver.get('https://www.naati.com.au/online-directory/?require=interpreter&for=[482,570,707,724,1306,1487,1551,1277,1300]')

# max wait time for loading
# if wait is longer than 10 seconds i think it crashes
delay = 10 # seconds

# wait for the webpage to load before we scrape
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="od-table-content"]/div[1]/div[1]/span/a')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

# find number of pages so we know when to while loop too
page_number = int(driver.find_element_by_class_name('total-pages').text)
number = 1
pages = 1

# temporary list for each person
# holds as name, current certifications, location, phone, email and website
temp = []
# big list to hold everything
final_list = []
# loop through the website
while (pages <= page_number):
    temp = []
    # wait until page loads
    WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="inside-content-right"]/div[1]/img')))
    # have to figure out how to make it wait until display is none myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="inside-content-right"]/div[1]')))
    while (number <= 5):
        element = driver.find_element_by_xpath('//*[@id="od-table-content"]/div[{}]/div[1]/span/a'.format(number))
        #scrolling to each name
        driver.execute_script("arguments[0].scrollIntoView();", element)
        #clicking each name
        element.click()
        # wait till box loads
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="od-practitioner-modal"]/div/div')))
        # wait till information loads
        WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH,'//*[@id="od-practitioner-modal"]/div/div/div[2]/div[1]/img')))
        
        # name
        print(driver.find_element_by_xpath('//*[@id="od-practitioner-name"]').text)
        # current certifications
        print(driver.find_element_by_xpath('//*[@id="od-current-certifications"]').text)
        # location
        print(driver.find_element_by_xpath('//*[@id="od-practitioner-location"]').text)
        # phone number
        print(driver.find_element_by_xpath('//*[@id="od-practitioner-phone"]').text)
        # email
        print(driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[2]/div[2]/div/div/div[5]/div/div').text)
        # website
        print(driver.find_element_by_xpath('//*[@id="od-practitioner-website"]').text)
        
        # close the box
        driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[1]/button').click()
        # go to next contact
        number = number + 1
    # click the next page button
    next_button = driver.find_element_by_xpath('//*[@id="od-pagination-content"]/span/a[3]')
    # go to the next page button
    driver.execute_script("arguments[0].scrollIntoView();", next_button)
    # click the next page button
    next_button.click()
    number = 1
    pages = pages + 1