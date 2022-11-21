import csv
import cufflinks as cf
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
from flask import Flask,render_template,request
from selenium import webdriver
import time
import pandas as pd
app=Flask(__name__)
@app.route("/",methods=["GET"])
def cricket():
    return render_template("cricindex.html")
@app.route("/cricket",methods=["GET","POST"])

def cricket_player():
    if request.method=="POST":
        try:
            searching = request.form["team"].replace(" ", "-")
            link = "https://www.espncricinfo.com/team/" + searching

            driver = webdriver.Chrome(r"C:\\Users\\ajaykumar\\Downloads\\chromedriver_win32\\chromedriver.exe")
            driver.get(link)
            time.sleep(3)  # web driver sleeping purpose
            teamDetail=BeautifulSoup(driver.page_source, "html.parser")
            # print(teamDetail)
            TeamLink=teamDetail.find("section",class_="").find_all("nav")[0].find_all("div",class_="ds-bg-fill-content-prime")[0].find_all("a",class_="ds-px-3 ds-py-2 hover:ds-text-ui-typo-primary")[3]["href"]

            ab = requests.get(TeamLink)

            TeamRanking=BeautifulSoup(ab.text,"lxml")
            TeamRankingLinks= TeamRanking.find_all("div", class_="pnl253M")[0].find_all("ul", class_="Record")[2].find_all("li")[1].a["href"]
            TeamRankingLink="https://stats.espncricinfo.com/"+TeamRankingLinks
            driver.get(TeamRankingLink)
            TeamPlayer= BeautifulSoup(driver.page_source, "html.parser")

            TeamPlayerDetail=TeamPlayer.find_all("table", class_="engineTable")[0].find_all("tr")



            del TeamPlayerDetail[0]
            TeamAllPlayer = []

            for Teamplayer in TeamPlayerDetail:
                try:
                    PlayerName=Teamplayer.find_all("td")[0].text
                except:
                    PlayerName="player name not available in this team"
                try:
                    playYear=Teamplayer.find_all("td")[1].text
                except:
                    playYear="playYear is not available in this team"
                try:
                    PlayingMatch =Teamplayer.find_all("td")[2].text
                except:
                    PlayingMatch=" played match is not available"
                try:
                    innings = Teamplayer.find_all("td")[3].text
                except:
                    innings="innings are not available "
                try:
                    Notout=Teamplayer.find_all("td")[4].text
                except:
                    Notout="Notout stats is not found in this player"
                try:
                    runs =Teamplayer.find_all("td")[5].text
                except:
                    runs = "run stats is not found in this player"
                try:
                    HighstScores =Teamplayer.find_all("td")[6].text
                except:
                    HighstScores =" HighstScores stats is not found in this player"
                try:
                    avarage = Teamplayer.find_all("td")[7].text
                except:
                    avarage ="average stats is not available  in this player"
                try:
                    ballsFaced = Teamplayer.find_all("td")[8].text
                except:
                    ballsFaced ="ballsFaced  stats is not available in this player"
                try:
                    BattingSR = Teamplayer.find_all("td")[9].text
                except:
                    BattingSR ="Strike rate is not avavilable in this player"
                try:
                    Hundreds = Teamplayer.find_all("td")[10].text
                except:
                    Hundreds ="  Hundreds list is not found in this player"
                try:
                    fiftes = Teamplayer.find_all("td")[11].text
                except:
                    fiftes ="fiftes list is not found in this player"
                try:
                    ducks = Teamplayer.find_all("td")[12].text
                except:
                    ducks ="duck_out list is not found in this player"
                try:
                    four = Teamplayer.find_all("td")[13].text
                except:
                    four ="list of fours is not available in this player"
                try:
                    sixes = Teamplayer.find_all("td")[14].text
                except:
                    sixes ="list of sixes is not available in this player"

                Allplayers={"PlayerName":PlayerName,"playYear": playYear,"PlayingMatch":PlayingMatch,"innings":innings,"Notout":Notout,"runs":runs,"HighstScores":HighstScores,"avarage":avarage,"ballsFaced": ballsFaced,"BattingSR":BattingSR,"Hundreds":Hundreds,"fiftes":fiftes,"ducks": ducks,"four":four,"sixes":sixes}
                TeamAllPlayer.append(Allplayers)
                filename = searching+'  players.csv'
                with open(filename, 'w') as f:
                    w = csv.DictWriter(f, ["PlayerName", "playYear", "PlayingMatch", "innings", "Notout", "runs",
                                           "HighstScores", "avarage", "ballsFaced", "BattingSR", "Hundreds", "fiftes",
                                           "ducks", "four", "sixes"])
                    w.writeheader()
                    for i in TeamAllPlayer:
                        w.writerow(i)

            return render_template("cricResult.html",player=TeamAllPlayer[0:len(TeamAllPlayer)-1])
                # TeamAllPlayer.append({
                # "PlayerName":PlayerName,"playYear": playYear,"PlayingMatch":PlayingMatch,"innings":innings,"Notout":Notout,"runs":runs,"HighstScores":HighstScores,"avarage":avarage,"ballsFaced": ballsFaced,"BattingSR":BattingSR,"Hundreds":Hundreds,"fiftes":fiftes,"ducks": ducks,"four":four,"sixes":sixes
                # })

        except:
            return  "check team name once"
app.run()