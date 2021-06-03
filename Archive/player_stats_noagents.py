from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

event_group_id = "all"
event_id = "all"
region = "all"
country = "all"
min_rounds = "0"
min_rating = "1600"
agent = "all"
map_id = "all"
timespan = "all"

file_name = "player_stats_noagents_" + event_group_id + "_" + event_id + "_" + region + "_" + country + "_" + min_rounds + "_" + min_rating + "_" + agent + "_" + map_id + "_" + timespan + ".csv"

url = "https://www.vlr.gg/stats/?event_group_id=" + event_group_id + "&event_id=" + event_id + "&region=" + region + "&country=" + country + "&min_rounds=" + min_rounds + "&min_rating=" + min_rating + "&agent=" + agent + "&map_id=" + map_id + "&timespan="+timespan

driver = webdriver.Chrome()
driver.get(url)

"Collect data using bs4"
soup = BeautifulSoup(driver.page_source, "html.parser")
table = soup.find("table")
if (table is not None):
    rows = table.findAll('tr')[1::] # The 0th row is the title row, therefore excluded
    output_rows = [] # Will contain all rows needed to be added to csv file
    for row_elem in rows:
        cols = row_elem.findAll('td')
        output_row = [] # Will contain the current row, which will be appended to output_rows
        for col in cols:
            player_elem = col.find("div", class_="text-of") # If currently in the Player column, this will be found
            team_elem = col.find("div", class_="stats-player-country") # Not all players are guaranteed to have a team, this is a check
            span_elem = col.find("span") # Refers to the columns that store the data in a span
            
            cur_elem_class = None # Will either be None (if class DNE) or the class of the current element
            if col.has_attr('class'):
                cur_elem_class = col['class'][0]

            if (player_elem is not None):
                output_row.append(player_elem.text)
            elif (team_elem is not None):
                output_row.append(team_elem.text)
            elif (span_elem is not None):
                output_row.append(span_elem.text)
            elif (cur_elem_class != "mod-agents"): # Case for all other columns EXCLUDING agents
                output_row.append(col.text.strip())
        output_rows.append(output_row)

"Writes all of the data acquired into a csv file"
with open(file_name, 'w') as csvfile: # NOTE: As the flag is 'w' this will overwrite any other file (in the dir) with the same name
    writer = csv.writer(csvfile)
    writer.writerow(["Player","# RND","ACS","K:D","ADR","KPR","APR","FKPR","FDPR","HS%","CL%","CL","KMAX","K","D","A","FK","FD"]) # Titles
    writer.writerows(output_rows)

driver.close()