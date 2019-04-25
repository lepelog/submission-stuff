import requests
from collections import defaultdict
import datetime

def parsetimedelta(s):
     s=s.split(':')
     if len(s) == 3:
             hour=int(s[0])
     else:
             hour=0
     minute=int(s[-2])
     second=int(s[-1])
     return datetime.timedelta(seconds=second, minutes=minute, hours=hour)

games_to_times=defaultdict(list)

submissions = requests.get('https://submissions.bingothon.com/api/submissions').json()
for submission in submissions['submissions'].values():
    games_to_times[submission['game']['name']].append(parsetimedelta(submission['game']['estimate']))

totaltime = datetime.timedelta()
for game, times in games_to_times.items():
    totaltime += max(times) + datetime.timedelta(minutes=8)

print(totaltime)
