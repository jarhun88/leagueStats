import requests

numMatches = 20
myId = "Ry-EABKsOzN8GMcayrr_8zA7t1JzaSm51SZ6LZxj_ykj0w"
endIndex = "10"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-1b16f2df-df32-4907-8af8-a1c33cc8e021"
}

matchlist_url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + myId + "?endIndex=" + endIndex + "&api_key=RGAPI-1b16f2df-df32-4907-8af8-a1c33cc8e021"
response = requests.get(matchlist_url, headers=headers)
response = response.json()["matches"]
retVal = []

for match in response:
    matchId = str(match["gameId"])
    # print(matchId)
    match_url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + matchId
    matchResponse = requests.get(match_url, headers=headers)
    matchResponse = matchResponse.json()
    # print(matchResponse)
    retVal.append(matchResponse)

print(retVal)


