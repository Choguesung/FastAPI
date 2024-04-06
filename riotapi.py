import requests
from urllib import parse

apiKey = 'RGAPI-01757a88-9b2d-4d20-98d5-d9324b68adc4'

def search(nickname,tagline):
    # 랭크 n경기 매치아이디 가져오기
    username = nickname

    id = parse.quote(username) # 아이디를 URL 인코딩

    # url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + id +'?api_key=' + apiKey #puuid값을 가져오기 위한 주소
    url = 'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + id +'/'+ tagline + '?api_key=' + apiKey #puuid값을 가져오기 위한 주소
    r = requests.get(url)
    r = r.json()
    puuid = r['puuid'] # 해당 유저의 puuid 값 가져오기

    n = str(10)
    rankUrl = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?queue=420&type=ranked&start=0&count='+n+'&api_key='+ apiKey
    r = requests.get(rankUrl)
    r = r.json()

    rankId = r

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
                    win.append(part[j]['win'])
                    deaths.append(part[j]['deaths'])
                    kills.append(part[j]['kills'])
                    # 승리, 킬뎃값 넣어주기

    return win

def is_played(nickname,tagline):
     # 랭크 n경기 매치아이디 가져오기
    username = nickname

    id = parse.quote(username) # 아이디를 URL 인코딩

    # url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + id +'?api_key=' + apiKey #puuid값을 가져오기 위한 주소
    url = 'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + id +'/'+ tagline + '?api_key=' + apiKey #puuid값을 가져오기 위한 주소
    r = requests.get(url)
    r = r.json()
    puuid = r['puuid'] # 해당 유저의 puuid 값 가져오기

    rankUrl = 'https://kr.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/' + puuid + '?api_key='+ apiKey
    r = requests.get(rankUrl)
    r = r.json()

    return r