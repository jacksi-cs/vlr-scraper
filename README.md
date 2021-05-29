# Web Scraper for VLR.gg

## player_stats_agents.py
Scrapes from https://www.vlr.gg/stats the player performance on each agent. To apply filter properties, modify the URL in the source code (under the comment CHANGEABLE VARIABLES). Other changeable variables include the file name for the generated csv file and the date range for the player data.

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
