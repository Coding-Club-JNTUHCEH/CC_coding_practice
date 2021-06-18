import time
import requests


def fetchCFProfileInfo(username):
    url = 'https://codeforces.com/api/user.info?handles='+str(username)
    JSONdata = fetchURL(url)

    if JSONdata["status"] != 'OK':
        return {}
    profile = JSONdata["result"][0]
    lastOnline,format = convertTime(profile["lastOnlineTimeSeconds"])
    try:
        rating = profile['rating']
    except:
        rating = 0
    try:
        maxRating = profile['maxRating']
    except:
        maxRating = 0

    p = {
        "rating"    :   rating,
        "maxRating" :   maxRating,
        "titlePhoto":   profile["titlePhoto"],
        "lastonline":   lastOnline,
        "format"    :   format
    }

    return p


def getSolvedProblems(username):
    url = "https://codeforces.com/api/user.status?handle="+str(username)

    JSONdata = fetchURL(url)
    if JSONdata["status"] != 'OK':
        return []
    return JSONdata["result"]


def fetchAllProblems():
    url = 'https://codeforces.com/api/problemset.problems'
    JSONdata = fetchURL(url)

    if JSONdata["status"] != 'OK':
        return []
    return JSONdata['result']['problems']


def fetchAllUsers(users_str):
    url = "https://codeforces.com/api/user.info?handles=" + users_str
    JSONdata = fetchURL(url)
    if JSONdata["status"] != "OK":
        return []

    return JSONdata["result"]


def fetchAllContests():
    url = 'https://codeforces.com/api/contest.list'
    JSONdata = fetchURL(url)

    if JSONdata["status"] != 'OK':
        return []
    return JSONdata['result']


def convertTime(seconds):
    now = time.time()
    diff = now - seconds
    hours = round(diff/3600, 2)

    if hours >= 48:
        days = hours//24
        if days>60:
            months = days//30
            if months>=24:
                years = months//12
                return years,"Years"
            return months,"Months"
        return days,"Days"
    return hours,"Hours"


def getRating(username):
    try:
        return fetchCFProfileInfo(username)["rating"]
    except:
        return 800


def fetchURL(url):
    try:
        data = requests.get(url, timeout=8)
        return data.json()
    except:
        return {"status": "FAILED"}
