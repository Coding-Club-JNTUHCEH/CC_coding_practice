

def extract_leaderboardData(user,rank):
    return {
        "username" : user.user.username ,
        "rating"   : user.rating,
        "rank"     : rank, 
        "solved_problems" : user.sloved_problems_count

    }