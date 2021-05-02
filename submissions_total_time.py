import requests
from collections import defaultdict
import datetime
# parse 8601 duration
from re import findall

def parsetimedelta(s):
     s=s.split(':')
     if len(s) == 3:
             hour=int(s[0])
     else:
             hour=0
     minute=int(s[-2])
     second=int(s[-1])
     return datetime.timedelta(seconds=second, minutes=minute, hours=hour)

def calc_total_time():
    games_to_times=defaultdict(list)

    submissions = requests.get('https://submissions.bingothon.com/api/submissions').json()
    for submission in submissions['submissions'].values():
        games_to_times[submission['game']['name']].append(parsetimedelta(submission['game']['estimate']))

    totaltime = datetime.timedelta()
    for game, times in games_to_times.items():
        totaltime += max(times) + datetime.timedelta(minutes=8)

    print(totaltime)

def print_all_games():
    all_games = set(submission['game']['name'] for submission in requests.get('https://submissions.bingothon.com/api/submissions').json()['submissions'].values())
    print('\n'.join(all_games))

def calc_total_time_oengus():
    games_to_times=defaultdict(list)
    
    submissions = requests.get('https://oengus.io/api/marathon/bingos21/submissions').json()
    for submission in submissions:
        for game_submission in submission["games"]:
            for category_submission in game_submission["categories"]:
                games_to_times[game_submission["name"]].append(datetime.timedelta(seconds=iso8601_duration_as_seconds(category_submission["estimate"])))
    
    totaltime = datetime.timedelta()
    for game, times in games_to_times.items():
        totaltime += max(times) + datetime.timedelta(minutes=10)

    print(totaltime)

def iso8601_duration_as_seconds( d ):
    if d[0] != 'P':
        raise ValueError('Not an ISO 8601 Duration string')
    seconds = 0
    # split by the 'T'
    for i, item in enumerate(d.split('T')):
        for number, unit in findall( '(?P<number>\d+)(?P<period>S|M|H|D|W|Y)', item ):
            # print '%s -> %s %s' % (d, number, unit )
            number = int(number)
            this = 0
            if unit == 'Y':
                this = number * 31557600 # 365.25
            elif unit == 'W': 
                this = number * 604800
            elif unit == 'D':
                this = number * 86400
            elif unit == 'H':
                this = number * 3600
            elif unit == 'M':
                # ambiguity ellivated with index i
                if i == 0:
                    this = number * 2678400 # assume 30 days
                    # print "MONTH!"
                else:
                    this = number * 60
            elif unit == 'S':
                this = number
            seconds = seconds + this
    return seconds

calc_total_time_oengus()
