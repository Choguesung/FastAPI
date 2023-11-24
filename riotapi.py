import pandas as pd
import requests
from urllib import parse

apiKey = 'RGAPI-14f4bfae-0c4f-4731-931c-792b868acd69'
# username = 'Zealot'
champ = 'Thresh' # 원하는 챔프(머신러닝결과값)

def search(nickname):
    # 랭크 n경기 매치아이디 가져오기
    username = nickname

    id = parse.quote(username) # 아이디를 URL 인코딩

    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + id +'?api_key=' + apiKey #puuid값을 가져오기 위한 주소
    r = requests.get(url)
    r = r.json()
    puuid = r['puuid'] # 해당 유저의 puuid 값 가져오기

    n = str(10)
    rankUrl = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?queue=420&type=ranked&start=0&count='+n+'&api_key='+ apiKey
    r = requests.get(rankUrl)
    r = r.json()

    rankId = r
    print(rankId)

    win = []
    deaths = []
    kills = []
    for i in rankId:
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i + '?api_key=' + apiKey
        r = requests.get(url)
        r = r.json()
        info = r['info']  # 전체 데이터에서 info를 추출
        part = info['participants'] # info 데이터에서 유저들의 정보 추출
        for j in range(0,10): # 총 10명의 유저중 내가 원하는 puuid값을 가진 유저를 추출
              if part[j]['puuid'] == puuid:
                 if part[j]['championName'] == champ: # 유저가 champ를 플레이했던 매치데이터를 추출
                    win.append(part[j]['win'])
                    deaths.append(part[j]['deaths'])
                    kills.append(part[j]['kills'])
                    # 승리, 킬뎃값 넣어주기

    return win