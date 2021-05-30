# Web Scraper for VLR.gg

## player_stats_agents.py
Scrapes from https://www.vlr.gg/stats the player performance on each agent. To apply filter properties (as seen on https://www.vlr.gg/stats), modify the corresponding variables in the source code (under the comment CHANGEABLE VARIABLES). Other changeable variables include the file name for the generated csv file (defaulted to be "player_stats_agents_eventgroupid_eventid_region_country_minrounds_minrating_agent_mapid_timespan.csv") and the url (though it is automatically changed by certain variable values).

The generated csv file will contain a header field that is explained below:
* **Player**: Player name
* **Agent**: Agent used
* **Usage**: # of times played
* **# RND**: # of rounds played
* **ACS**: Average combat score
* **K:D**: Kills : Death ratio
* **ADR**: Average damage per round
* **KPR**: Kills per round
* **APR**: Assists per round
* **FKPR**: First kills per round
* **FDPR**: First deaths per round
* **K**: Total kills
* **D**: Total deaths
* **A**: Total assists
* **FK**: Total first kills
* **FD**: Total first deaths

## player_stats_noagents.py
Identical to player_stats_agents.py but does not explore and scrape data from the player profiles. Instead it srapes the aggregated data present in the table at https://www.vlr.gg/stats. Applying filter properties and modifying other changeable variables remain the same (under the comment CHANGEABLE VARIABLES), while file naming is defaulted to the same nomenclature as explained above.

The generated csv file will contain a header file, abbreviations that were explained above will not be repeated below:
* **HS%**: Headshot %
* **CL%**: Clutch success %
* **CL**: Clutch success (won/played)
* **KMAX**: Maximum kills in a single map
