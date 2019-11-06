import csv
import requests
from re import findall
from datetime import timedelta

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
    
def format_player(player):
    if player['twitchName'] != None:
        return '[{}](https://twitch.tv/{})'.format(player['username'],player['twitchName'])
    else:
        print('twitch name for '+player['username']+' is missing!')
        return player['username']

oengus_schedule = requests.get('https://oengus.io/api/marathon/bingow19/schedule').json()

with open('schedule.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(('Game','Estimate','Player(s)','Platform','Category','Bingotype','Layout'))
    for line in oengus_schedule['lines']:
        players=(format_player(player) for player in line['runners'])
        if line['type'] == "RACE":
            player_string = ' vs. '.join(players)
        else:
            player_string = ','.join(players)
            
        category = line['categoryName']
        if category != None:
            category = category.lower()
        else:
            category = ''
            
        if 'blackout' in category:
            bingotype = 'blackout'
            
        elif 'lockout' in category:
            bingotype = 'lockout'
        else:
            bingotype = 'single'
        
        if line['ratio'] != None and '/' in line['ratio']:
            line['ratio'] = line['ratio'].replace('/',':')
        if line['setupBlock']:
            # bad hacky stuff
            line['estimate'] = line['setupTime']
            line['gameName'] = 'Setup'
            line['categoryName'] = 'Setup'
            player_string = 'Bingothon'
        estimate = str(timedelta(seconds=iso8601_duration_as_seconds(line['estimate'])))
        writer.writerow((line['gameName'], estimate, player_string, line['console'], line['categoryName'], bingotype, line['ratio']))
