# statHandler.py
import config as cfg
import pygame, sys, math, copy, random
from pygame.locals import *
from time import sleep

def readStats():
    '''Loads stats from file "stats.txt" into dictionary "stats"

    Return paramters:
        stats -- dictionary containing retrieved stats
    '''
    stats = {}
    f = open('stats.txt', 'r')
    for line in f:
        line = line.split(': ')
        stats[line[0]] = int(line[1])

    f.close()
    ##print('stats:',stats)
    return stats

def writeStats(stats, win):
    '''Writes newStats into the file "stats.txt"
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