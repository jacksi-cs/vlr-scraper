from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "http://www.vlr.gg/stats"

driver = webdriver.Chrome()
driver.get(url)

"Iterates through all player elements, visiting each player profile to scrape data"
player_elem_list = driver.find_elements_by_xpath("//td[@class='mod-player mod-a']")
for index in range (1,len(player_elem_list)+1):
    xpath_test = "(//td[@class='mod-player mod-a'])[" + str(index) + "]"
    driver.find_element_by_xpath(xpath_test).click() # Player element, when clicked goes to profile
    "TODO: Collect data using bs4"
    driver.back()
    time.sleep(0.1)

driver.close()
