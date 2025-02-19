import math


def score_account_age(days: float):
    score = -452.8427 + (114.4774 - -452.8427)/(1 + math.pow(days/35874.48,0.3517686))
    score = max(0, min(100, score))
    
    return score

def score_account_games(numOfGames: int):
    score = -18.8532 + (106.9959 - -18.8532)/(1 + math.pow(numOfGames/18.0617,1.006217))
    score = max(0, min(100, score))
    
    return score

def score_account_bans(numOfBans: int):
    if numOfBans == 0:
        return 0
    if numOfBans == 1:
        return 80
    if numOfBans == 2:
        return 90
    if numOfBans >= 3:
        return 100
    
def score_total_playtime(hours: float):
    score = -22.14958 + (100.5163 - -22.14958)/(1 + math.pow(hours/103.3833,0.9577552))
    score = max(0, min(100, score))
    
    return score

def score_last_2_weeks_versus_average(last2Weeks: float, average2Weeks: float):
    percentage = (last2Weeks/average2Weeks) * 100
    
    score = 167.9669 + (-0.2194044 - 167.9669)/(1 + math.pow(percentage/218.2696,1.150048))
    score = max(0, min(100, score))
    
    return score

def score_account_value(value: float):
    score = -15.39933 + (101.1556 - -15.39933)/(1 + math.pow(value/42.889,0.957756))
    score = max(0, min(100, score))
    
    return score

def score_account_friends(numOfFriends: int):
    score = -7.734675 + (101.146 - -7.734675)/(1 + math.pow(numOfFriends/6.178119,2.069771))
    score = max(0, min(100, score))
    
    return score

def score_average_achievement_percentage(numOfCompleted: int, totalAchievementsPossible: int):
    percentage = (numOfCompleted/totalAchievementsPossible) * 100
    
    score = -34.81428 + (100.493 - -34.81428)/(1 + math.pow(percentage/23.93659,1.064883))
    score = max(0, min(100, score))
    
    return score
    
if __name__ == '__main__':
    
    pass