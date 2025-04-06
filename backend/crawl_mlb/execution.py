from .crawl import GetContent, Filter
from .database import add_table_game_row, add_table_pitcher_row, add_table_team_row,add_table_team_stat_row,add_table_pitcher_stat_row
import datetime


import sys
from datetime import date, timedelta

print(len(sys.argv))
f = Filter()

def date_range(start_date, end_date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

def insert_db(match_list, match_date):
    ''''''
    for m in match_list:
        if hasattr(m.status, "detailed_state") and m.status.detailed_state == "Postponed":
            continue
        add_table_game_row(m)
        add_table_pitcher_stat_row(m.home_team.starter, match_date)
        add_table_pitcher_stat_row(m.away_team.starter, match_date)
        add_table_team_stat_row(m.home_team, match_date)
        add_table_team_stat_row(m.away_team, match_date)
        add_table_pitcher_row(m.home_team.starter.id, m.home_team.starter.name, m.home_team.starter.handed)
        add_table_pitcher_row(m.away_team.starter.id, m.away_team.starter.name, m.away_team.starter.handed)
        # don't need to execute below all the time
        add_table_team_row(m.home_team.id, m.home_team.name)
        add_table_team_row(m.away_team.id, m.away_team.name)

def fetch_data_to_db(date:str):
    '''The date format should be 2024-08-01'''
    print('data is',date)
    matches = GetContent("object", f.item, date)
    print('matches is',matches)
    for m in matches:
        print("mmm", m.status)
    now = datetime.datetime.now()
    target_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    if (now.date() == target_date.date() and now.hour >= 4) == False:
        insert_db(matches, date)

# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         mode = sys.argv[1]
#         if mode == "history":
#             start_date = date(2024, 8, 1)
#             end_date = date(2024, 8, 10)
#             for single_date in date_range(start_date, end_date):
#                 date = single_date.strftime("%Y-%m-%d")
#                 print(GetContent("result", f.item, date))
#                 matches = GetContent("object", f.item, date)
#                 insert_db(matches)
#     elif len(sys.argv) == 3:
#         mode = sys.argv[1]
#         if mode == "single":
#             date = sys.argv[2]
#             print(GetContent("result", f.item, date))
#             matches = GetContent("object", f.item, date)
#             insert_db(matches)
#     else:
#         print(GetContent("result", f.item, ""))
