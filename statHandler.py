import config as cfg
import json

def readStats():
    '''NOTE: Depreciated function.

    Loads stats from file "stats.txt" into dictionary "stats"

    Return paramters:
        stats -- dictionary containing retrieved stats
    '''
    stats = {}
    f = open('stats.txt', 'r')
    for line in f:
        line = line.split(': ')
        stats[line[0]] = int(line[1])

    f.close()
    return stats

def writeStats(stats, win):
    '''NOTE: Depreciated function.

    Writes newStats into the file "stats.txt"
    Usually called after the readStats() function

    stats -- stats retrieved from readStats()
    win -- boolean; whether or not the human player won the game.
    '''
    print('newStats =', cfg.newStats)
    print('stats =',stats)
    if cfg.newStats['Turns'] < stats['Fastest Game']:
        print('New turn record!')
        newRecord = True
    else:
        newRecord = False

    f = open('stats.txt', 'w')

    if win:
        # If player won
        print('Added 1 to win counter')
        value = stats['Battles Won'] + 1
        f.write('Battles Won: ' + str(value) + '\n')
    else:
        # If player lost
        value = stats['Battles Won']
        f.write('Battles Won: ' + str(value) + '\n')

    value = stats['Games Played'] + 1
    f.write('Games Played: ' + str(value) + '\n')

    value = stats['Total Damage'] + cfg.newStats['Damage']
    f.write('Total Damage: ' + str(value) + '\n')

    value = stats['Total Turns'] + cfg.newStats['Turns']
    f.write('Total Turns: ' + str(value) + '\n')

    # If player sets a new move record, change the "Fastest Game" value to the new record
    if newRecord:
        f.write('Fastest Game: ' + str(cfg.newStats['Turns']))
    else:
        f.write('Fastest Game: ' + str(stats['Fastest Game']))
    f.close()

def readJson():
    '''Loads stats from file "stats.json" into dictionary "stats"

    Return paramters:
        stats -- dictionary containing retrieved stats
    '''
    stats = {}
    with open('stats.json', 'r') as f:
        stats = json.load(f)

    return stats

def processStats(stats, win):
    '''Increments stats, based on game outcome.
    Called during the writeJson() function

    stats -- stats retrieved from readStats()
    win -- boolean; whether or not the human player won the game.

    Return parameters:
        stats -- processed stats dictionary
    '''
    if cfg.newStats['Turns'] < stats['FastestGame']:
        print('New turn record!')
        newRecord = True
    else:
        newRecord = False

    # Modify "fastest game" attribute, only if new turn record
    if newRecord:
        stats['FastestGame'] = cfg.newStats['Turns']

    # Add 1 to win counter, if player won the battle
    if win:
        print('Added 1 to win counter')
        stats['BattlesWon'] += 1

    # Increment other stats
    stats['GamesPlayed'] += 1
    stats['TotalDamage'] += cfg.newStats['Damage']
    stats['TotalTurns'] += cfg.newStats['Turns']
    return stats

def writeJson(stats, win):
    '''Writes newStats into the file "stats.json"
    Usually called after the readJson() function

    stats -- stats retrieved from readStats()
    win -- boolean; whether or not the human player won the game.
    '''
    stats = processStats(stats, win)

    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)

def resetJson():
    '''Resets the game stats located in the file "stats.json"
    Essentially rewrites all of the stats with 0 value
    '''
    data = {'BattlesWon': 0,
            'GamesPlayed': 0,
            'TotalDamage': 0,
            'TotalTurns': 0,
            'FastestGame': 999}

    with open('stats.json', 'w') as f:
        json.dump(data, f, indent=4)