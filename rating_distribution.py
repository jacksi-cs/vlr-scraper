import datetime
import pickle
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup

# date_str = "March 31, 2021"
# date_obj = datetime.datetime.strptime(date_str, '%B %d, %Y').date()
# print(date_obj)


# tuple_test = {}
# tuple_test["Team Liquid"] = (datetime.date.today(), 2450)
# with open('test.txt', 'wb') as t:
#     pickle.dump(tuple_test, t)

# with open('test.txt', 'rb') as t:
#     print(type(pickle.load(t)))

rating_dict = {}

url_list = ["https://www.vlr.gg/rankings/europe", "https://www.vlr.gg/rankings/north-america", "https://www.vlr.gg/rankings/asia-pacific", "https://www.vlr.gg/rankings/latin-america", "https://www.vlr.gg/rankings/oceania", "https://www.vlr.gg/rankings/korea", "https://www.vlr.gg/rankings/mena"]

"Iterate through all regions"
for url in url_list:
    driver = webdriver.Chrome()
    driver.get(url)

    "Iterate through all teams (of that specific region)"
    team_elem_list = driver.find_elements_by_xpath("//td[@class='rank-item-team']//a")
    for index in range(1,len(team_elem_list)+1):
        try:
            team = driver.find_element_by_xpath("(//td[@class='rank-item-team'])[" + str(index) + "]//a")
        except NoSuchElementException:
            print("URL: ", url, "index: ", index)
            time.sleep(1)
            team = driver.find_element_by_xpath("(//td[@class='rank-item-team'])[" + str(index) + "]//a")
            
        driver.execute_script("arguments[0].click();", team) # Goes to the team profile
        
        rating_dist = []

        "Scrapes the rating data storing rating elements (date, rating) into a list, which is then added to a dict"
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for point in soup.find_all("div", class_="tip"):
            date_str = point.find("div").text.strip()
            date_obj = datetime.datetime.strptime(date_str, '%B %d, %Y').date()
            rating = point.find("div", class_="result").text.strip()
            rating = rating[rating.find("(")+1 : rating.find(")")]
            rating_dist.append((date_obj, rating))

        team_name = driver.find_element_by_xpath("//div[contains(@class,'wf-title')]//h1").text.strip()
        rating_dict[team_name] = rating_dist

        driver.back()

    with open('rating_distribution.txt', 'wb') as file:
        print("Finished pickling ", url)
        pickle.dump(rating_dict, file)
    
    driver.close()

print("Finished pickling all")