import pytest
from server.smurfcalculation import (
    score_account_age,
    score_account_games,
    score_account_bans,
    score_total_playtime,
    score_last_2_weeks_versus_average,
    score_account_value,
    score_account_friends,
    score_average_achievement_percentage
)

def test_score_account_age():
    assert score_account_age(0) == 20
    assert score_account_age(7) == 17.538707465237135
    assert score_account_age(14) == 16.147540772732704
    assert score_account_age(30) == 14.231162349197133
    assert score_account_age(60) == 12.06705661382456
    assert score_account_age(100) == 10.174470791454793
    assert score_account_age(180) == 7.645263082492488
    assert score_account_age(260) == 5.855584102627643
    assert score_account_age(365) == 4.054607708450419
    assert score_account_age(500) == 2.250307633873001
    assert score_account_age(730) == 0

def test_score_account_games():
    assert score_account_games(0) == 15.0
    assert score_account_games(3) == 13.386151128245793
    assert score_account_games(5) == 11.98212639629295
    assert score_account_games(8) == 10.275028183611543
    assert score_account_games(10) == 9.33819866499711
    assert score_account_games(15) == 7.490180480608814
    assert score_account_games(20) == 6.127052539308202
    assert score_account_games(30) == 4.252214939041655
    assert score_account_games(40) == 3.024368470060726
    assert score_account_games(60) == 1.514805259436846
    assert score_account_games(100) == 0.03404853814267739

def test_score_account_bans_no_bans():
    assert score_account_bans(0) == 0.0

def test_score_account_bans_one_ban():
    assert score_account_bans(1) == 16.0

def test_score_account_bans_two_bans():
    assert score_account_bans(2) == 18.0

def test_score_account_bans_three_or_more_bans():
    assert score_account_bans(3) == 20.0
    assert score_account_bans(10) == 20.0

def test_score_total_playtime():
    assert score_total_playtime(0) == 15.0
    assert score_total_playtime(10) == 13.30257395935523
    assert score_total_playtime(20) == 11.917370097973553
    assert score_total_playtime(30) == 10.768962346815538
    assert score_total_playtime(50) == 8.954719291257199
    assert score_total_playtime(70) == 7.575783166512215
    assert score_total_playtime(100) == 6.02408176428122
    assert score_total_playtime(150) == 4.254904262193963
    assert score_total_playtime(200) == 3.0633838574320666
    assert score_total_playtime(300) == 1.552838910217017
    assert score_total_playtime(500) ==  0.007961158534050482

def test_score_account_value():
    assert score_account_value(0) == 10.0
    assert score_account_value(5) == 8.796069623601294
    assert score_account_value(10) == 7.799766613851841
    assert score_account_value(15) == 6.995068718527493
    assert score_account_value(20) == 6.326932482135351
    assert score_account_value(30) == 5.27566062023261
    assert score_account_value(50) == 3.8604551637163533
    assert score_account_value(80) == 2.5979182323719323
    assert score_account_value(100) == 2.0467133753703317
    assert score_account_value(150) == 1.1598299530154035
    assert score_account_value(300) == 0.026032479425647993

