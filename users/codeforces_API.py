import time
import requests

def fetchCFProfileInfo(username):
    url = 'https://codeforces.com/api/user.info?handles='+str(username)
    JSONdata = fetchURL(url)
    
    if JSONdata["status"] != 'OK' :
        return {}
    profile = JSONdata["result"][0]
    lastOnline = convertTime(profile["lastOnlineTimeSeconds"])

    p = {
        "rating"    :   profile["rating"] , 
        "maxRating" :   profile["maxRating"],
        "titlePhoto":   profile["titlePhoto"],
        "lastonline" :  lastOnline
    }

    return p


def getSolvedProblems(username):
        url = "https://codeforces.com/api/user.status?handle="+str(username)
        data = requests.get(url)
        JSONdata = data.json()
        if JSONdata["status"]!= 'OK':
                return []
        return JSONdata["result"]


def fetchAllProblems():
    url = 'https://codeforces.com/api/problemset.problems'
    JSONdata = fetchURL(url)
    
    if JSONdata["status"] != 'OK':    
        return []
    return JSONdata['result']['problems']


def convertTime(seconds):
    now = time.time()
    diff  = now - seconds
    return round( diff/3600, 2)


def getRating(username):
    try:
        return fetchCFProfileInfo(username)["rating"]
    except:
        return 800


def fetchURL(url):
    data = requests.get(url)
    return data.json()