import psycopg2
import os
from .mlb_class import Team, Match, Pitcher
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PWD")
db_port = os.getenv("DB_PORT")

Table_name_game = "api_game"
Table_name_pitcher = "api_pitcher"
Table_name_pitcher_stat = "api_pitcherstat"
Table_name_team = "api_team"
Table_name_team_stat = "api_teamstat"


conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host)
cursor = conn.cursor()


def commit():
    conn.commit()

def close_connection():
    conn.close()

def fetch_table(table_name):
    '''Select the whole table by the input name'''
    cursor.execute(f'select * from {table_name}')
    print(cursor.fetchall())


def add_table_game_row(match:Match):
    '''Add new game in table'''
    query = "select game_pk from "+Table_name_game+f" where game_pk={match.id}"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("insert into "+Table_name_game+" (game_pk, game_date, winner_t_id, home_team_power, away_team_power, is_winner_home_team, home_starter_id, away_starter_id, home_team_id, away_team_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (match.id, match.date, match.winner_team_id, match.home_team.win_points ,match.away_team.win_points,match.is_winner_home_team,match.home_team.starter.id,match.away_team.starter.id, match.home_team.id, match.away_team.id))
        commit()

def add_table_pitcher_stat_row(pitcher: Pitcher, date):
    '''Add new pitcher_stat in table'''
    query = "select p_id,stat_date from "+Table_name_pitcher_stat+f" where p_id='{pitcher.id}' and stat_date='{date}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("insert into "+Table_name_pitcher_stat+" (p_id, stat_date, wins, losses, era, so) values(%s,%s,%s,%s,%s,%s)",
                       (pitcher.id, date, pitcher.winning.win, pitcher.winning.loss, pitcher.era, pitcher.so))
        commit()

def add_table_pitcher_row(p_id, p_name, handed):
    '''Add new pitcher in table'''
    query = "select p_name from "+Table_name_pitcher+f" where p_id='{p_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("insert into "+Table_name_pitcher+" (p_id, p_name, handed) values(%s,%s,%s)",
                    (p_id, p_name, handed))
        commit()

def add_table_team_row(t_id, t_name):
    '''Add new team in table'''
    query = "select t_name from "+Table_name_team+f" where t_id='{t_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("insert into "+Table_name_team+" (t_id, t_name) values(%s,%s)",
                    (t_id, t_name,))
        commit()

def add_table_team_stat_row(team: Team, date: str):
    '''Add new team_stat in table'''
    query = "select t_id, stat_date from "+Table_name_team_stat+f" where t_id='{team.id}' and stat_date='{date}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("insert into "+Table_name_team_stat+" (t_id, stat_date, overall_wins, overall_losses, home_wins, home_losses, away_wins, away_losses, left_handed_wins, left_handed_losses, right_handed_wins, right_handed_losses, last_10_wins, last_10_losses, diff, streak_is_win, streak) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (team.id, date,
                        team.overall_winning.win,team.overall_winning.loss,
                        team.home_winning.win, team.home_winning.loss,
                        team.away_winning.win, team.away_winning.loss,
                        team.vs_l_winning.win, team.vs_l_winning.loss,
                        team.vs_r_winning.win, team.vs_r_winning.loss,
                        team.l10.win, team.l10.loss,
                        team.diff, team.streak.is_win, team.streak.streak_num))
        commit()