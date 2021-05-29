from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

## CHANGEABLE VARIABLES ##
file_name = "output.csv"
date_range = "all" # 30d, 60d, 90d, or all
url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=1000&min_rating=1600&agent=all&map_id=all&timespan="+date_range

driver = webdriver.Chrome()
driver.get(url)

output_rows = [] # Will contain all rows needed to be added to csv file

"Iterates through all player elements, visiting each player profile to scrape data"
player_elem_list = driver.find_elements_by_xpath("//td[@class='mod-player mod-a']")
for index in range (1,len(player_elem_list)+1):
    xpath_test = "(//td[@class='mod-player mod-a'])[" + str(index) + "]"
    driver.find_element_by_xpath(xpath_test).click() # Player element, when clicked goes to profile

    "Clicking the correct date range for player profile (30d,60d,90d,all)"
    filter_list = driver.find_elements_by_xpath("//a[@class='player-stats-filter-btn ']")
    for elem in filter_list:
        if (elem.text.strip().lower() == date_range):
            time.sleep(0.1)
            driver.execute_script("arguments[0].click();", elem)
            break

    "Collect data using bs4"
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table")
    if (table is not None):
        row = table.findAll('tr')[1::] # The 0th row is the title row, therefore excluded
        for row_elem in row:
            player_name = soup.find("h1").text.strip()
            cols = row_elem.findAll('td')
            output_row = [player_name] # Will contain the current row, which will be appended to output_rows
            for col in cols:
                agent_elem = col.find('img', alt=True) # Finding the data containing agent
                usage_elem = col.find('span')
                if (agent_elem is not None): # If currently on the Agent column of that respective row
                    output_row.append(test['alt'])
                elif (usage_elem is not None): # If currently on the Usage column of that respective row
                    val = test2.text
                    output_row.append(val[val.find("(")+1:val.find(")")])
                else: # Every other column
                    output_row.append(col.text.strip())
            output_rows.append(output_row)

    "Goes back from the player profile to the stats menu"
    if (date_range != "60d"):
        driver.back()
    driver.back()
    time.sleep(0.1)

"Writes all of the data acquired into a csv file"
with open(file_name, 'w') as csvfile: # NOTE: As the flag is 'w' this will overwrite any other file (in the dir) with the same name
    writer = csv.writer(csvfile)
    writer.writerow(["Player","Agent", "Usage", "# RND", "ACS", "K:D", "ADR", "KPR", "APR", "FKPR", "FDPR", "K", "D", "A", "FK", "FD"]) # Titles
    writer.writerows(output_rows)

driver.close()
