import math


def score_account_age(days: int):
    score = -452.8427 + (114.4774 - -452.8427)/(1 + math.pow(days/35874.48,0.3517686))
    score = max(0, min(100, score))
    
    return score

def score_account_games(numOfGames: int):
    score = -18.8532 + (106.9959 - -18.8532)/(1 + math.pow(numOfGames/18.0617,1.006217))
    score = max(0, min(100, score))
    
    return score

if __name__ == '__main__':
    
    pass