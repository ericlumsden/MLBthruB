import numpy as np
import os
import pandas as pd
import pybaseball
import sys
sys.path.append('/mnt/c/Users/airiq/MLBthruB/extra_bits')
from gathering_team_ids import gather_team_ids

"""
GOAL: Collect data that can be used in linear regression, KNNs, etc.
For linear regression: run differential vs win total (?)
For KNNs: Launch angle and exit velo for HRs (?) Might be better for stats organizing...
"""
def collect_runs_for_against_win_total(year: int=2023, teams: dict=gather_team_ids()):
    wp_rfa_2023 = {}
    team_count = 1
    for team, acronym in teams.items():
        print(f"Gathering data from {team} ... {team_count} out of {len(teams.keys())}")
        temp_team = pybaseball.schedule_and_record(year, acronym)
        wp_rfa_2023[acronym] = {}
        wp_rfa_2023[acronym]['win_percentage'] = (len(temp_team[temp_team['R'] > temp_team['RA']]) / len(temp_team)) * 100
        wp_rfa_2023[acronym]['runs_for'] = temp_team['R'].sum()
        wp_rfa_2023[acronym]['runs_against'] = temp_team['RA'].sum()
        team_count += 1
    return wp_rfa_2023

def collect_run_win_total(year: int=2023, teams: dict=gather_team_ids()):
    wp_rd_2023 = {}
    team_count = 1
    for team, acronym in teams.items():
        print(f"Gathering data from {team} ... {team_count} out of {len(teams.keys())}")
        temp_team = pybaseball.schedule_and_record(year, acronym)
        wp_rd_2023[acronym] = {}
        wp_rd_2023[acronym]['win_percentage'] = (len(temp_team[temp_team['R'] > temp_team['RA']]) / len(temp_team)) * 100
        wp_rd_2023[acronym]['runs'] = temp_team['R'].sum()
        team_count += 1
    return wp_rd_2023

def collect_batting_stats(year: int=2023):
    batting_stats = pybaseball.batting_stats(year, year+1)
    """The next three lines generate + stats for Barrel%, EV and LA since those do not already come in the dataset as well as a series of 1s to generate for the intercept"""
    batting_stats["ones"] = [1] * len(batting_stats.axes[0])
    batting_stats["Barrel%+"] = batting_stats["Barrel%"] / (batting_stats["Barrel%"].sum() / len(batting_stats.axes[0]))
    batting_stats["EV+"] = batting_stats["EV"] / (batting_stats["EV"].sum() / len(batting_stats.axes[0]))
    batting_stats["LA+"] = batting_stats["LA"] / (batting_stats["LA"].sum() / len(batting_stats.axes[0]))
    batting_stats = batting_stats[batting_stats['AB'] >= 502] # We only want players that qualify for awards
    batting_stats = batting_stats[["ones", "Barrel%+", "EV+", "LA+", "Pull%+", "Cent%+", "Oppo%+", "Soft%+", "Hard%+", "BB%+", "K%+", "BABIP+"]]
    return batting_stats

if __name__ == "__main__":
    import json
    #json.dump( collect_run_win_total(), (open( "wp_r_2023.json", "w" )) )
    #json.dump( collect_runs_for_against_win_total(), (open( "wp_rfa_2023.json", "w" )) )
    collect_batting_stats().to_csv('./batting_stats.csv')
