

def extract_leaderboardData(user,rank):
    count = user.sloved_problems.all().count()
    return {
        "username" : user.user.username ,
        "rating"   : user.rating,
        "rank"     : rank, 
        "solved_problems" :count

    }