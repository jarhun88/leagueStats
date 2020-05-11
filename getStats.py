import requests
import json
import numpy as np

# stephlovesbecca summoner ID
myId = "Ry-EABKsOzN8GMcayrr_8zA7t1JzaSm51SZ6LZxj_ykj0w"
# number of matches to look back on 
endIndex = "1"
# LoL game version
version = "10.9.1"
api_key = "RGAPI-61b16149-1db0-42a1-ad5e-2b7e222b1195"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

# requesting json of champion data on LoL
champions = requests.get("http://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/champion.json")
champions = champions.json()
champions = champions["data"]

matchlist_url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + myId + "?endIndex=" + endIndex + "&api_key=" + api_key
response = requests.get(matchlist_url, headers=headers)
response = response.json()["matches"]
retVal = []

for match in response:
    matchId = str(match["gameId"])
    match_url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + matchId
    matchResponse = requests.get(match_url, headers=headers)
    matchResponse = matchResponse.json()

    matchResponse.pop("queueId")
    matchResponse.pop("gameCreation")
    matchResponse.pop("gameDuration")
    matchResponse.pop("mapId")
    matchResponse.pop("platformId")
    matchResponse.pop("gameType")
    matchResponse.pop("gameVersion")

    for player in matchResponse["participants"]:
        player.pop("stats")
        player.pop("timeline")
        player.pop("spell1Id")
        player.pop("spell2Id")
    
    for team in matchResponse["teams"]:
        team.pop("vilemawKills")
        team.pop("dominionVictoryScore")

        for cid in team["bans"]:
            championId = cid["championId"]
            print(championId)
            for name, championInfo in champions.items():
                if int(championInfo["key"]) == int(championId):
                    champName = championInfo["id"]
                    cid["championId"] = champName
    
    for participants in matchResponse["participants"]:
        championId = participants["championId"]

        for name, championInfo in champions.items():
            if int(championId) == int(championInfo["key"]):
                champName = championInfo["id"]
                participants["championId"] = champName

    participants = matchResponse["participants"].copy()

    for i in range(0, len(participants)):
        participants[i]["summonerName"] = matchResponse["participantIdentities"][i]["player"]["summonerName"]

    matchResponse.pop("participantIdentities")

    participants1 = np.array(participants.copy())
    participants1 = participants1[0:5].tolist()

    participants2 = np.array(participants.copy())
    participants2 = participants2[5: len(participants)].tolist()

    matchResponse.pop("participants")

    matchResponse["teams"][0].update({"participants" : participants1})
    matchResponse["teams"][1]["participants"] = participants2

    retVal.append(matchResponse)

print(retVal)

with open("league-stats.json", "w") as f:
    json.dump(retVal, f)



