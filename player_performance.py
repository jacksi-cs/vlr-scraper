from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re # Used for find the substring of the match URL to generate the match ID

"Input list of team URLs"
team_url_list = ["https://www.vlr.gg/team/474/team-liquid/"]

"Generate list of players from all teams listed (player name, player URL)"
player_url_dict = {} # Key: player name, value: player profile URL (NOTE: just for debugging)
player_url_list = [] # List of all URLs for player profiles
for url in team_url_list:
    driver = webdriver.Chrome()
    driver.get(url)
    roster_elem_list = driver.find_elements_by_xpath("//div[@class='team-roster-item']")
    for member in roster_elem_list:
        try:
            member.find_element_by_xpath(".//div[@class='wf-tag mod-light team-roster-item-name-role']") # Only appears if staff or inactive
        except NoSuchElementException:
            player_url_dict[str(member.find_element_by_xpath(".//div[@class='team-roster-item-name-alias']").text)] = member.find_element_by_xpath(".//a").get_attribute('href') # NOTE: just for debugging
            player_url_list.append(member.find_element_by_xpath(".//a").get_attribute('href'))
    driver.close()
print(player_url_list)

"Generate player performance for each player on each map"
"(team name, opp team name, team rank, opp rank, map, match ID, date, agent, ACS, KDA, ADR, HS%, FK, FD)"

#row_container
#output_row
output_rows = []
"Iterating through all players' profiles of the teams in the team_url_list"
for url in player_url_list:
    driver = webdriver.Chrome()
    driver.get(url)
    more_results_elem = driver.find_element_by_xpath("//div[@class='wf-more']//a") # Web element of the more results for match history
    driver.execute_script("arguments[0].click();", more_results_elem)

    "Iterate through each match checking to see if the match ID is in output_rows (already added)"
    match_list = driver.find_elements_by_xpath("//a[contains(@class,'wf-module-item')]")
    for index in range (1,len(match_list)+1):
        match = driver.find_element_by_xpath("(//a[contains(@class,'wf-module-item')])[" + str(index) + "]")
        match_url = match.get_attribute('href') # https://www.vlr.gg/(match ID)/(other information)
        match_id = match_url.split("/")[3] # "/" separates the string, the match ID is in the 4th section
        player_name = driver.find_element_by_xpath("//h1[@class='wf-title']").text.strip()

        "If output_rows does not contain the match ID -> click on match, add all players' performance in (only 'marking' the current player)"
        # NOTE: The sequence of actions: click on match, iterate through maps played, grab all player data (marking only specified played)
        if not output_rows or not any(row[0] == match_id for row in output_rows):
            driver.execute_script("arguments[0].click();", match) # Click on match
            map_list = driver.find_elements_by_xpath("//div[contains(@class, 'vm-stats-gamesnav-item')][@data-disabled=0]")
            for map in map_list[1::]: # Iterate through maps played (skipping the first as it is 'All Maps')
                driver.execute_script("arguments[0].click();", map)
                # TODO: scrape data using bs4
            driver.back()

        # If output_rows does contain the match ID -> find all rows with the matching match ID and player name and 'mark' it
        else:
            for row in output_rows:
                if row[0] == match_id and row[3] == player_name and row[17] == False:
                    row[17] = True # 'Marking' the row

    driver.close()