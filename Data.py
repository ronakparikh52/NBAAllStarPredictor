
#importing necessary libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

class Data:
    def __init__(self):
        self.data = []
    
    #Uses webscraping techniques to get player name and if they were an all-star from the website basketball-reference. Returns a list of the names of all all-stars
    def allStars(self, year):
        URL = f"https://www.basketball-reference.com/allstar/NBA_{year}.html"
        r = requests.get(URL)
        if r.status_code == 429:
            if 'Retry-After' in r.headers:
                print(r.headers['Retry-After'])
        soup = BeautifulSoup(r.text, 'lxml')
        rows = soup.select('tr')[6:]
        names = []
        exclude = ['', 'Team Totals', 'Starters', 'Reserves']
        for row in rows:
            element = row.select('th')
            name = element[0].text
            if name not in exclude:
                names.append(name)
        
        id_element = soup.find(id="content")
        li_element = id_element.select('li')[0]
        a_element = li_element.select('a')
        for item in a_element:
            names.append(item.text)
        return names

    #Uses webscraping techniques to get player name and the six most important stats from the website basketball-reference. Returns a list of every player's stats
    def stats(self, year):
        URL = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml')
        rows = soup.select('[class="full_table"]')
        data = []
        for row in rows:
            element = row.select('td')
            name = element[0].text
            ppg = float(element[28].text)
            rpg = float(element[22].text)
            apg = float(element[23].text)
            spg = float(element[24].text)
            bpg = float(element[25].text)
            gamesPlayed = int(element[4].text)
            list = [name, ppg, rpg, apg, spg, bpg, gamesPlayed]
            data.append(list)
        return data
    
    #Creating Final Table. Using pandas to create and return 2D table with Name, Points per game, Assists per game, Rebounds per game, Steals per game, Blocks per game, Games played, and if they were an allstar.
    def finalData(self, year) :
        stats = self.stats(year)
        allStars = self.allStars(year)
        for player in stats:
            if player[0] in allStars:
                player.append(1)
            else:
                player.append(0)
        df = pd.DataFrame(stats, columns = ['Name', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'Games Played', 'All Star'])
        return df
    
#Can get data from a specific year here. Added feature, not necessary for running the model
def main():
    scraping = Data()
    while True:
        year = input("What year would you like all the data to be from? ")
        try:
            year = int(year)
            if 1950 < year < 2025:
                break
            print("Please enter a valid year")
        except ValueError:
                print("Please enter a valid year")
    
    table = scraping.finalData(year)
    print(table)

if __name__ == "__main__":
    main()

