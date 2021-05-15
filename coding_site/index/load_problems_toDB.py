from .models import Problem
import requests


def fetchProblemsForDB():
    url = 'https://codeforces.com/api/problemset.problems'
    data = requests.get(url)
    JSONdata = data.json()
    problemSet = []

    if JSONdata["status"] != 'OK':
        return problemSet
    a = True
    for problem in JSONdata['result']['problems']:
        p = ExtractProblem(problem)
        if a:
            p_db = Problem(p)
            print(p_db)
            a=False
        problemSet.append(p)
        
    return True

def ExtractProblemForDB(problem):
    if 'rating' in problem:
        rating = problem["rating"]
    else:
        rating = 0
    if 'tags' in problem:
        tags = problem["rating"]
    else:
        tags = []

    p = {'contestID' : problem["contestId"],
            'index'  : problem["index"],
            'name'   : problem["name"],
            'rating' : rating,
            'tags'   : tags,
            'link'   : 'https://codeforces.com/problemset/problem/' + str(problem["contestId"]) + '/' + problem["index"],
        }
    return p


if __name__ == "__main__":
    fetchProblems()