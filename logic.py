# logic.py
import draw, screens, statHandler, config as cfg
import pygame, sys, math, copy, random
from pygame.locals import *
from time import sleep

def quitGame():
    '''Called when the Close button is clicked. (Window bar or in-game)
    '''
    print('quitGame')
    pygame.quit()
    sys.exit()

def swapMon(player):
    '''Swaps the player's primary and secondary Mon.

    player -- 1 (human) or 2 (AI)
    '''
    # Swap Mon by swapping the dictionaries
    print('swapping...')

    if player == 1:
        temp = copy.deepcopy(cfg.p1Primary)
        temp2 = copy.deepcopy(cfg.p1Backup)
        print('temp:', temp)
        print('temp2:', temp2)
        cfg.p1Primary = copy.deepcopy(temp2)
        cfg.p1Backup = copy.deepcopy(temp)
    else:
        temp = copy.deepcopy(cfg.p2Primary)
        cfg.p2Primary = copy.deepcopy(cfg.p2Backup)
        cfg.p2Backup = copy.deepcopy(temp)

    # For debugging
    print('p1Primary:', cfg.p1Primary)
    print('p1Backup:', cfg.p1Backup)
    print('p2Primary:', cfg.p2Primary)
    print('p2Backup:', cfg.p2Backup)
    print('swap complete')

def playerMove(action, player):
    '''
    action = A1/A2/A3 (attack) or S (for swap)
    player = 1 or 2
    '''
    # Called when player 1 OR player 2 moves
    if player == 1:
        p1rect = cfg.MegabiteNormal.get_rect()
        p1rect.bottomleft = (32,430)
        p2rect = cfg.SnowbroNormal.get_rect()
        p2rect.bottomleft = (530,234)

        # In case player cannot swap
        p1Move, p2Move = defineMoves()

        # Player 1 attacks
        if len(action) > 1 or cfg.p1Backup['CurrentHP'] <= 0:
            if action == 'S':
                action = p1Move

            # Reset display
            draw.resetGameDisplay()
            draw.character('normal', 2)
            draw.messageBox(cfg.p1Primary['Name'] + ' used ' + action + '!', '')

            # Player attack animation
            draw.character('attack', 1)
            draw.pausePrompt(200)

            # Reset display
            draw.resetGameDisplay()
            draw.character('normal', 1)

            # Only performs attack
            damage, powerMsg, fainted = playerAttacks(action, 1)
            if fainted:
                return

            # Reset display
            draw.resetGameDisplay()
            draw.character('normal', 1)

            if powerMsg == 'SuperE':
                print('Super effective attack')
                draw.messageBox(cfg.p1Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's super effective!")
            elif powerMsg == 'NotVE':
                print('Not very effective attack')
                draw.messageBox(cfg.p1Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's not very effective...")
            else:
                draw.messageBox(cfg.p1Primary['Name'] + " attacks for " + str(damage) + " damage.", '')

            # Update health bars
            draw.healthBar(1)
            draw.healthBar(2)

            # Enemy hit animation
            draw.character('hit', 2)
            draw.pausePrompt(200)

        # Player 1 swaps
        else:
            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.character('normal', 2)
            draw.messageBox('Come back, ' + cfg.p1Primary['Name'] + '!', '')
            draw.pausePrompt(200)

            # Swap occurs
            swapMon(1)

            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            draw.platform(2)
            draw.character('normal', 2)
            draw.healthBar(2)

            pygame.display.update()
            sleep(0.6)

            draw.messageBox('Go, ' + cfg.p1Primary['Name'] + '!', '')
            draw.pausePrompt(200)

            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.character('normal', 2)
            pygame.display.update()
            sleep(0.2)

    else:
        # Player 2 attacks
        if len(action) > 1 or cfg.p2Backup['CurrentHP'] <= 0:
            if action == 'S':
                action = p2Move

            # Reset display
            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.messageBox(cfg.p2Primary['Name'] + ' used ' + action + '!', '')

            # Player attack animation
            draw.character('attack', 2)
            draw.pausePrompt(200)

            # Reset display
            draw.resetGameDisplay()
            draw.character('normal', 2)

            # Only performs attack
            damage, powerMsg, fainted = playerAttacks(action, 2)
            if fainted:
                return

            # Reset display
            draw.resetGameDisplay()
            draw.character('normal', 2)

            if powerMsg == 'SuperE':
                print('Super effective attack')
                draw.messageBox(cfg.p2Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's super effective!")
            elif powerMsg == 'NotVE':
                print('Not very effective attack')
                draw.messageBox(cfg.p2Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's not very effective...")
            else:
                draw.messageBox(cfg.p2Primary['Name'] + " attacks for " + str(damage) + " damage.", '')

            # Update health bars
            draw.healthBar(1)
            draw.healthBar(2)

            # Enemy hit animation
            draw.character('hit', 1)
            draw.pausePrompt(200)

        # Player 2 swaps
        else:
            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.character('normal', 2)
            draw.messageBox('Trainer Ethan is calling back ' + cfg.p2Primary['Name'] + '!', '')
            draw.pausePrompt(200)

            # Swap occurs
            swapMon(2)

            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            draw.platform(1)
            draw.character('normal', 1)
            draw.healthBar(1)

            pygame.display.update()
            ##pygame.time.delay(600)
            sleep(0.6)

            draw.messageBox('Trainer Ethan sent out ' + cfg.p2Primary['Name'] + '!', '')
            draw.pausePrompt(200)

            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.character('normal', 2)
            pygame.display.update()
            ##pygame.time.delay(400)
            sleep(0.2)


def playerAttacks(move, player):
    if player == 1:
        # Inflicting damage to player 2's primary Mon
        damage, powerMsg = calculateDamage(cfg.p1Primary['ATK'], cfg.moveTypes[move], cfg.p1Primary['Type'], cfg.moveBaseDmg[move], cfg.p2Primary['Type'])
        pygame.mixer.Sound.play(cfg.hitSFX)

        # Mon's HP must never dip below zero
        if cfg.p2Primary['CurrentHP'] < damage:
            cfg.p2Primary['CurrentHP'] = 0

            # Add damage to stats
            cfg.newStats['Damage'] += damage
            fainted = checkIfFainted()
        else:
            cfg.p2Primary['CurrentHP'] = cfg.p2Primary['CurrentHP'] - damage

            # Add damage to stats
            cfg.newStats['Damage'] += damage
            fainted = checkIfFainted()
    else:
        # Inflicting damage to player 1's primary Mon
        damage, powerMsg = calculateDamage(cfg.p2Primary['ATK'], cfg.moveTypes[move], cfg.p2Primary['Type'], cfg.moveBaseDmg[move], cfg.p1Primary['Type'])
        pygame.mixer.Sound.play(cfg.hitSFX)
        if cfg.p1Primary['CurrentHP'] < damage:
            cfg.p1Primary['CurrentHP'] = 0
            fainted = checkIfFainted()
        else:
            cfg.p1Primary['CurrentHP'] = cfg.p1Primary['CurrentHP'] - damage
            fainted = checkIfFainted()

    print(str(damage) + ' dealt')
    return damage, powerMsg, fainted


def calculateDamage(AtkStat, moveType, monType, baseDamage, oppType):
    '''Calculates the amount of damage that one Mon will inflict on the opposing Mon.
    Returns damage and powerMsg (super effective, not very effective, etc.)

    The following parameters relate to the Attacking Mon:
        AtkStat -- their attack stat
        moveType -- the move's type
        monType -- their type/element
        baseDamage -- the move's base damage

    The following parameter relates to the Defending Mon:
        oppType -- their type/element
    '''

    damage = baseDamage * (AtkStat * 0.02)

    # Modify damage based on types
    if moveType == monType:
        damage = damage * 1.25
    if moveType == 'F':
        if oppType == 'C':
            damage = damage * 2
            powerMsg = 'SuperE'
        elif oppType == 'W':
            damage = damage / 2
            powerMsg = 'NotVE'
        else:
            powerMsg = 'Normal'
    elif moveType == 'W':
        if oppType == 'F':
            damage = damage * 2
            powerMsg = 'SuperE'
        elif oppType == 'C':
            damage = damage / 2
            powerMsg = 'NotVE'
        else:
            powerMsg = 'Normal'
    elif moveType == 'C':
        if oppType == 'W':
            damage = damage * 2
            powerMsg = 'SuperE'
        elif oppType == 'F':
            damage = damage / 2
            powerMsg = 'NotVE'
        else:
            powerMsg = 'Normal'

    # Round damage value down to nearest whole number
    damage = math.floor(damage)
    return damage, powerMsg

def checkIfFainted():
    fainted = False
    if cfg.p1Primary['CurrentHP'] == 0:
        fainted = True
        print('p1 primary mon fainted')

        # Perform swap if fainted
        draw.resetGameDisplay()
        draw.character('hit', 1)
        draw.character('normal', 2)
        draw.messageBox(cfg.p1Primary['Name'] + ' fainted!', '')
        draw.pausePrompt(200)

        if cfg.p1Backup['CurrentHP'] <= 0:
            # Player loses, AI wins
            print('p1 loses')
            win = False

            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            draw.platform(2)
            draw.healthBar(2)
            draw.character('normal', 2)
            draw.messageBox('You have lost the battle!', '')
            draw.pausePrompt(600)
            screens.resultsScreen(win)

        # Swap occurs
        else:
            swapMon(1)

            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            draw.platform(2)
            draw.character('normal', 2)
            draw.healthBar(2)

            pygame.display.update()
            sleep(0.6)

            draw.messageBox('Go, ' + cfg.p1Primary['Name'] + '!', '')
            draw.pausePrompt(200)

            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.character('normal', 2)
            pygame.display.update()
            sleep(0.2)

    elif cfg.p2Primary['CurrentHP'] <= 0:
        fainted = True
        print('p2 primary mon fainted')

        # Perform swap if fainted

        draw.resetGameDisplay()
        draw.character('normal', 1)
        draw.character('hit', 2)
        draw.messageBox(cfg.p2Primary['Name'] + ' fainted!', '')
        draw.pausePrompt(200)

        if cfg.p2Backup['CurrentHP'] == 0:
            # Player wins
            print('p1 wins')
            win = True

            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            draw.platform(1)
            draw.healthBar(1)
            draw.character('normal', 1)
            draw.messageBox('You have won the battle!', '')
            draw.pausePrompt(600)
            screens.resultsScreen(win)

        # Swap occurs
        else:
            swapMon(2)

            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            draw.platform(1)
            draw.character('normal', 1)
            draw.healthBar(1)

            pygame.display.update()
            sleep(0.6)

            draw.messageBox('Trainer Ethan brought out ' + cfg.p2Primary['Name'] + '!', '')
            draw.pausePrompt(200)

            draw.resetGameDisplay()
            draw.character('normal', 1)
            draw.character('normal', 2)
            pygame.display.update()
            sleep(0.2)

    return fainted

def setMon(p1P_Pick, p1B_Pick, p2P_Pick, p2B_Pick):
    # Copy dictionaries
    ##global p1Primary, p2Primary, p1Backup, p2Backup
    cfg.p1Primary = copy.deepcopy(cfg.Megabite)
    cfg.p1Backup = copy.deepcopy(cfg.Drogon)
    cfg.p2Primary = copy.deepcopy(cfg.Snowbro)
    cfg.p2Backup = copy.deepcopy(cfg.Megabite)

    # For debugging
    print('p1Primary:', cfg.p1Primary)
    print('p1Backup:', cfg.p1Backup)
    print('p2Primary:', cfg.p2Primary)
    print('p2Backup:', cfg.p2Backup)

def defineMoves():
    '''Returns the moves of both players' Primary Mons

    Return parameters: p1Move, p2Move
    '''
    if cfg.p1Primary['Name'] == 'Megabite':
        p1Move = 'Sharp Teeth'
    elif cfg.p1Primary['Name'] == 'Snowbro':
        p1Move = 'Ice Shards'
    else:
        p1Move = 'Fireball'

    if cfg.p2Primary['Name'] == 'Megabite':
        p2Move = 'Sharp Teeth'
    elif cfg.p2Primary['Name'] == 'Snowbro':
        p2Move = 'Ice Shards'
    else:
        p2Move = 'Fireball'
    return p1Move, p2Move

def initiateAttack():
    '''Called when player clicks Attack'''
    p1Move, p2Move, = defineMoves()

    if cfg.p1Primary['SPD'] > cfg.p2Primary['SPD']:
        print('P1 moves first')
        playerMove(p1Move, 1)
        p1Move, p2Move, = defineMoves()
        playerMove(p2Move, 2)
    elif cfg.p2Primary['SPD'] > cfg.p1Primary['SPD']:
        print('P2 moves first')
        playerMove(p2Move, 2)
        p1Move, p2Move, = defineMoves()
        playerMove(p1Move, 1)
    else:
        print('Both Pius Mon have same SPD stat! Starting coin toss...')
        coinToss = random.randint(1,2)
        if coinToss == 1:
            print('P1 moves first')
            playerMove(p1Move, 1)
            p1Move, p2Move, = defineMoves()
            playerMove(p2Move, 2)
        else:
            print('P2 moves first')
            playerMove(p2Move, 2)
            p1Move, p2Move, = defineMoves()
            playerMove(p1Move, 1)

    cfg.newStats['Turns'] += 1 # Add turn to stats


def initiateSwap():
    '''Called when player clicks Swap'''

    # If backup mon is fainted, Player cannot swap
    if cfg.p1Backup['CurrentHP'] == 0:
        draw.resetGameDisplay()
        draw.character('normal', 1)
        draw.character('normal', 2)
        draw.messageBox("You can't swap right now!", "Your backup Mon is already fainted.")
        draw.pausePrompt(200)
        return
        ##continue
    # If player has used all three swaps, Player cannot swap
    elif cfg.timesSwapped >= 3:
        draw.resetGameDisplay()
        draw.character('normal', 1)
        draw.character('normal', 2)
        draw.messageBox("You can't swap right now!", "You have used all three of your swaps.")
        draw.pausePrompt(200)
        return
        ##continue

    p1Move, p2Move, = defineMoves()

    if cfg.p1Primary['SPD'] > cfg.p2Primary['SPD']:
        print('P1 moves first')
        playerMove('S', 1)
        cfg.timesSwapped += 1
        p1Move, p2Move, = defineMoves()
        playerMove(p2Move, 2)

    elif cfg.p2Primary['SPD'] > cfg.p1Primary['SPD']:
        print('P2 moves first')
        playerMove(p2Move, 2)
        p1Move, p2Move, = defineMoves()
        playerMove('S', 1)
        cfg.timesSwapped += 1

    else:
        print('Both Pius Mon have same SPD stat! Starting coin toss...')
        coinToss = random.choice([1,2])
        if coinToss == 1:
            print('P1 moves first')
            playerMove('S', 1)
            cfg.timesSwapped += 1
            p1Move, p2Move, = defineMoves()
            playerMove(p2Move, 2)
        else:
            print('P2 moves first')
            playerMove(p2Move, 2)
            p1Move, p2Move, = defineMoves()
            playerMove('S', 1)
            cfg.timesSwapped += 1

    print('Times swapped:', cfg.timesSwapped)
    cfg.newStats['Turns'] += 1 # Add turn to stats

def paused():
    '''When called, paused() waits for user input (key press OR mouse click) to resume the game'''
    pause = True
    while pause:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pause = False
                if event.key == pygame.K_SPACE:
                    pause = False
            if click[0] == 1:
                pause = False

def resetGame():
    '''Resets all global variables'''
    print('called resetGame')

    cfg.p1Primary = {}
    cfg.p1Backup = {}
    cfg.p2Primary = {}
    cfg.p2Backup = {}
    cfg.newStats = {'Damage': 0, 'Turns': 0}
    cfg.timesSwapped = 0

    print('newStats:', cfg.newStats)
    screens.titleScreen()