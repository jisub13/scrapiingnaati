# most important and basically brings everything
from selenium import webdriver
# telling them to wait for at least a specific amount of time until somethign
from selenium.webdriver.support.wait import WebDriverWait
# occurs when it takes more time for the until event
from selenium.common.exceptions import TimeoutException
# condition (used here to check if something is loading)
from selenium.webdriver.support import expected_conditions as EC
import time
# finding things by XPATH, ID, CLASS_NAME and other things
from selenium.webdriver.common.by import By
# to scroll and find actions
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome("C:\\Users\\Nosar\\Downloads\\chromedriver_win32\\chromedriver")
driver.get('https://www.naati.com.au/online-directory/?require=interpreter&for=[482,570,707,724,1306,1487,1551,1277,1300]')

# wait for the webpage to load before we scrape
delay = 10 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="od-table-content"]/div[1]/div[1]/span/a')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

#driver.find_element_by_xpath('//*[@id="od-table-content"]/div[{}]/div[1]/span/a'.format(number)).click()

# find number of pages
page_number = int(driver.find_element_by_class_name('total-pages').text)
number = 1
pages = 1
#driver.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click
while (pages <= page_number):
    time.sleep(3)
    # have to figure out how to make it wait until display is none myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="inside-content-right"]/div[1]')))
    while (number <= 5):
        element = driver.find_element_by_xpath('//*[@id="od-table-content"]/div[{}]/div[1]/span/a'.format(number))
        driver.execute_script("arguments[0].scrollIntoView();", element)
        #clicking each name
        element.click()
        time.sleep(0.5)
        print(driver.find_element_by_xpath('//*[@id="od-practitioner-name"]').text)
        driver.find_element_by_xpath('//*[@id="od-practitioner-modal"]/div/div/div[1]/button').click()
        time.sleep(0.5)
        number = number + 1
    driver.find_element_by_xpath('//*[@id="od-pagination-content"]/span/a[3]').click()
    number = 1
    pages = pages + 1