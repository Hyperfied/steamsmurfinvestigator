import math


def score_account_age(days: int):
    score = -452.8427 + (114.4774 - -452.8427)/(1 + math.pow(days/35874.48,0.3517686))
    score = max(0, min(100, score))
    
    return score

if __name__ == '__main__':
    print(score_account_age(700))
    pass