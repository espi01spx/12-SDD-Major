import pygame, sys, math, copy, random
from pygame.locals import *
from time import sleep

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

# Display config
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Pius Mon')
gameIcon = pygame.image.load('Images\Icon.PNG')
pygame.display.set_icon(gameIcon)

# Animation config
##FPS = 30
clock = pygame.time.Clock()

# Preset colours
pokemonYellow = (255, 204, 0)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (200, 0, 0)
green = (0, 200, 0)
darkGreen = (0, 153, 51)
brightRed = (255, 0, 0)
brightGreen = (0, 255, 0)
blue = (0, 0, 255)
waterBlue = (0, 204, 255)
iceBlue = (179, 240, 255)
orange = (255, 102, 0)
lightGrey = (190, 190, 190)
cream = (255, 250, 205)
forestBlue = (0, 92, 132)

# Images to load
logo = pygame.image.load('Images\Logo.png')
titleBackground = pygame.image.load('Images\SkyBackground.png')
gameBackground = pygame.image.load('Images\LandscapeBackground.png')

# Character images
SnowbroNormal = pygame.image.load('Images\YetiNormal.png')
SnowbroNormal = pygame.transform.scale(SnowbroNormal, (300, 300))
SnowbroAttack1 = pygame.image.load('Images\YetiAttack1.png')
SnowbroAttack1 = pygame.transform.scale(SnowbroAttack1, (300,300))
SnowbroAttack2 = pygame.image.load('Images\YetiAttack2.png')
SnowbroAttack2 = pygame.transform.scale(SnowbroAttack2, (300,300))
SnowbroHit = pygame.image.load('Images\YetiHit.png')
SnowbroHit = pygame.transform.scale(SnowbroHit, (300, 300))

MegabiteNormal = pygame.image.load('Images\Shark2Normal.png')
MegabiteNormal = pygame.transform.scale(MegabiteNormal, (300, 300))
MegabiteAttack = pygame.image.load('Images\Shark2Attack.png')
MegabiteAttack = pygame.transform.scale(MegabiteAttack, (300, 300))
MegabiteHit = pygame.image.load('Images\Shark2Hit.png')
MegabiteHit = pygame.transform.scale(MegabiteHit, (300,300))

DrogonNormal = pygame.image.load('Images\DragonNormal.png')
DrogonNormal = pygame.transform.scale(DrogonNormal, (300, 300))
DrogonAttack = pygame.image.load('Images\DragonAttack.png')
DrogonAttack = pygame.transform.scale(DrogonAttack, (300, 300))
DrogonHit = pygame.image.load('Images\DragonHit.png')
DrogonHit = pygame.transform.scale(DrogonHit, (300,300))

TrainerEthan = pygame.image.load('Images\TrainerEthan.png')

# Pius Mon stat values
Drogon =   {'Name': 'Drogon', 'Type': 'F', 'SPD': 25, 'MaxHP': 40, 'ATK': 35, 'CurrentHP': 40}
Snowbro =  {'Name': 'Snowbro', 'Type': 'C', 'SPD': 10, 'MaxHP': 50, 'ATK': 40, 'CurrentHP': 50}
Megabite = {'Name': 'Megabite','Type': 'W', 'SPD': 50, 'MaxHP': 30, 'ATK': 20, 'CurrentHP': 30}
p1Primary = {}
p1Backup = {}
p2Primary = {}
p2Backup = {}

# Moves
moveTypes = {'Sharp Teeth': 'W', 'Ice Shards': 'C', 'Fireball': 'F'}
moveBaseDmg = {'Sharp Teeth': 10, 'Ice Shards': 10, 'Fireball': 10}

# Stats setup
newStats = {'Damage': 0, 'Turns': 0}

# SFX
hitSFX = pygame.mixer.Sound('Sounds\SharpPunchSFX.wav')
selectSFX = pygame.mixer.Sound('Sounds\SelectSFX.wav')


def textObjects(text, font, textColour):
    textSurface = font.render(text, True, textColour)
    return textSurface, textSurface.get_rect()

def messageDisplay(text, size):
    largeText = pygame.font.SysFont('segoeui', size)
    TextSurf, TextRect = textObjects(text, largeText, black)
    TextRect.center = ((displayWidth/2),((displayHeight/2))-50)
    gameDisplay.blit(TextSurf, TextRect)

def quitGame():
    # Called when the Close button is clicked
    print('quitGame')
    pygame.quit()
    sys.exit()

def button(msg,x,y,w,h,ic,ac,tc,action=None):
    # msg = button label
    # x,y = top-left coordinates of the button box
    # w,h = button width/height
    # ic,ac = inactive colour, active colour (on mouse hover)
    # tc = text colour
    # action = function to trigger on button click

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        pygame.draw.rect(gameDisplay, black,(x,y,w,h),2)

        if click[0] == 1 and action != None:
            pygame.mixer.Sound.play(selectSFX)
            action()
            if msg in ['Attack','Swap']:
                resetGameDisplay()
                drawCharacter('normal', 2)
                drawCharacter('normal', 1)
                drawMovePrompt('What will ' + p1Primary['Name'] + ' do?')
                pygame.display.update()
                sleep(0.5)

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
        pygame.draw.rect(gameDisplay, black,(x,y,w,h),2)

    smallText = pygame.font.SysFont('segoeui',20,bold=True)
    textSurf, textRect = textObjects(msg, smallText, tc)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)

def drawMessageBox(line1, line2):
    # Draws a message box
    pygame.draw.rect(gameDisplay, forestBlue, (0, 486, displayWidth, 114))
    pygame.draw.rect(gameDisplay, white, (0, 486, displayWidth, 114), 1)

    # Draw line 1
    text = pygame.font.SysFont('verdana', 20, bold=True)
    textSurf, textRect = textObjects(line1, text, white)
    textRect.topleft = ((25, 502))
    gameDisplay.blit(textSurf, textRect)

    # Draw line 2
    if line2:
        textSurf, textRect = textObjects(line2, text, white)
        textRect.topleft = ((25, 550))
        gameDisplay.blit(textSurf, textRect)

    pygame.display.update()

def drawMovePrompt(line1):
    # Basically the same as drawMessageBox
    # Prompts the user to Attack or Swap

    pygame.draw.rect(gameDisplay, forestBlue, (0, 486, displayWidth, 114))
    pygame.draw.rect(gameDisplay, white, (0, 486, displayWidth, 114), 1)

    # Draw line 1
    text = pygame.font.SysFont('verdana', 20, bold=True)
    textSurf, textRect = textObjects(line1, text, white)
    textRect.topleft = ((25, 502))
    gameDisplay.blit(textSurf, textRect)


def healthBar(player):
    # x,y = top-left coordinates of the HP bar's background
    healthBarWidth = 200

    if player == 1:
        x = 550
        y = 400
        currentHP = p1Primary['CurrentHP']
        maxHP = p1Primary['MaxHP']
        monName = p1Primary['Name']
    else:
        x = 50
        y = 50
        currentHP = p2Primary['CurrentHP']
        maxHP = p2Primary['MaxHP']
        monName = p2Primary['Name']

    # Draw health bar background box
    pygame.draw.rect(gameDisplay, cream, (x-5, y-35, healthBarWidth+10, 85))
    pygame.draw.rect(gameDisplay, black, (x-5, y-35, healthBarWidth+10,85),1)

    # Draw max health bar
    for HP in range(healthBarWidth):
        pygame.draw.rect(gameDisplay, black, (x+HP, y, 1, 16), 0)

    ratio = int(max(min(currentHP/float(maxHP)*healthBarWidth,healthBarWidth),0))

    drawPointer(player)

    # Colour selection
    if ratio >= 100:
        barColour = green
    elif ratio >= 50:
        barColour = pokemonYellow
    else:
        barColour = brightRed

    # Draw current health bar
    for HP in range(ratio):
        pygame.draw.rect(gameDisplay, barColour, (x+HP, y, 1, 16), 0)
        HP += 1

    # Draw HP text
    msg = 'HP ' + str(currentHP) + ' / ' + str(maxHP)
    text = pygame.font.SysFont('verdana', 15, bold=True)
    textSurf, textRect = textObjects(msg, text, black)
    textRect.center = ((x+healthBarWidth-50, y+30))
    gameDisplay.blit(textSurf, textRect)

    # Draw Mon name label
    msg = monName
    text = pygame.font.SysFont('verdana', 15, bold=True)
    textSurf, textRect = textObjects(msg, text, black)
    textRect.topleft = ((x+5, y-28))
    gameDisplay.blit(textSurf, textRect)

def drawPointer(player):
    # Pointers to be attatched to end of health bar
    if player == 2:
        pygame.draw.polygon(gameDisplay, cream, ((256,16), (256,98), (280,58)), 0)
    else:
        pygame.draw.polygon(gameDisplay, cream, ((542,364), (542,448), (520,406)), 0)

def drawArrowPrompt():
    pygame.draw.polygon(gameDisplay, yellow, ((754, 562), (780, 562), (767, 584)), 0)
    pygame.display.update()

def drawPlatform(player):
    # Define colour based on monType
    if player == 1:
        monType = p1Primary['Type']
    else:
        monType = p2Primary['Type']

    if monType == 'F':
        colour = red
    elif monType == 'W':
        colour = waterBlue
    else:
        colour = iceBlue

    # Draw platform
    if player == 1:
        pygame.draw.ellipse(gameDisplay, colour, (30,380,300,100),0)
    else:
        pygame.draw.ellipse(gameDisplay, colour, (530,200,300,100),0)

def drawCharacter(state, player):
    # Determine mon's name
    if player == 1:
        mon = p1Primary['Name']
        rect = MegabiteNormal.get_rect()
        rect.bottomleft = (32,430)
        flip = False
    else:
        mon = p2Primary['Name']
        rect = SnowbroNormal.get_rect()
        rect.bottomleft = (530,234)
        flip = True

    # Now draw sprite, based on Mon name and state
    if mon == 'Megabite':
        if state == 'attack':
            if flip:
                MegabiteAttackR = pygame.transform.flip(MegabiteAttack, True, False)
                gameDisplay.blit(MegabiteAttackR, rect)
            else:
                gameDisplay.blit(MegabiteAttack, rect)
        elif state == 'hit':
            if flip:
                MegabiteHitR = pygame.transform.flip(MegabiteHit, True, False)
                gameDisplay.blit(MegabiteHitR, rect)
            else:
                gameDisplay.blit(MegabiteHit, rect)
        else:
            if flip:
                MegabiteNormalR = pygame.transform.flip(MegabiteNormal, True, False)
                gameDisplay.blit(MegabiteNormalR, rect)
            else:
                gameDisplay.blit(MegabiteNormal, rect)
    elif mon == 'Snowbro':
        if state == 'attack':
            if flip:
                SnowbroAttack1R = pygame.transform.flip(SnowbroAttack1, True, False)
                gameDisplay.blit(SnowbroAttack1R, rect)
            else:
                gameDisplay.blit(SnowbroAttack1, rect)
        elif state == 'hit':
            if flip:
                SnowbroHitR = pygame.transform.flip(SnowbroHit, True, False)
                gameDisplay.blit(SnowbroHitR, rect)
            else:
                gameDisplay.blit(SnowbroHit, rect)
        else:
            if flip:
                SnowbroNormalR = pygame.transform.flip(SnowbroNormal, True, False)
                gameDisplay.blit(SnowbroNormalR, rect)
            else:
                gameDisplay.blit(SnowbroNormal, rect)
    elif mon == 'Drogon':
        if state == 'attack':
            if flip:
                DrogonAttackR = pygame.transform.flip(DrogonAttack, True, False)
                gameDisplay.blit(DrogonAttackR, rect)
            else:
                gameDisplay.blit(DrogonAttack, rect)
        elif state == 'hit':
            if flip:
                DrogonHitR = pygame.transform.flip(DrogonHit, True, False)
                gameDisplay.blit(DrogonHitR, rect)
            else:
                gameDisplay.blit(DrogonHit, rect)
        else:
            if flip:
                DrogonNormalR = pygame.transform.flip(DrogonNormal, True, False)
                gameDisplay.blit(DrogonNormalR, rect)
            else:
                gameDisplay.blit(DrogonNormal, rect)

def swapMon(player):
    # Swap Mon by swapping the dictionaries
    print('swapping...')
    global p1Primary, p1Backup, p2Primary, p2Backup

    if player == 1:
        temp = copy.deepcopy(p1Primary)
        temp2 = copy.deepcopy(p1Backup)
        print('temp:', temp)
        print('temp2:', temp2)
        p1Primary = copy.deepcopy(temp2)
        p1Backup = copy.deepcopy(temp)
    else:
        temp = copy.deepcopy(p2Primary)
        p2Primary = copy.deepcopy(p2Backup)
        p2Backup = copy.deepcopy(temp)

    # For debugging
    print('p1Primary:', p1Primary)
    print('p1Backup:', p1Backup)
    print('p2Primary:', p2Primary)
    print('p2Backup:', p2Backup)
    print('swap complete')

def playerMove(action, player):
    # Called when player 1 OR player 2 moves
    if player == 1:
        p1rect = MegabiteNormal.get_rect()
        p1rect.bottomleft = (32,430)
        p2rect = SnowbroNormal.get_rect()
        p2rect.bottomleft = (530,234)

        # In case player cannot swap
        p1Move, p2Move = defineMoves()

        # Player 1 attacks
        if len(action) > 1 or p1Backup['CurrentHP'] <= 0:
            if action == 'S':
                action = p1Move

            # Reset display
            resetGameDisplay()
            drawCharacter('normal', 2)
            drawMessageBox(p1Primary['Name'] + ' used ' + action + '!', '')

            # Player attack animation
            drawCharacter('attack', 1)
            pausePrompt(200)

            # Reset display
            resetGameDisplay()
            drawCharacter('normal', 1)

            # Only performs attack
            damage, powerMsg, fainted = playerAttacks(action, 1)
            if fainted:
                return

            # Reset display
            resetGameDisplay()
            drawCharacter('normal', 1)

            if powerMsg == 'SuperE':
                print('Super effective attack')
                drawMessageBox(p1Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's super effective!")
            elif powerMsg == 'NotVE':
                print('Not very effective attack')
                drawMessageBox(p1Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's not very effective...")
            else:
                drawMessageBox(p1Primary['Name'] + " attacks for " + str(damage) + " damage.", '')

            # Update health bars
            healthBar(1)
            healthBar(2)

            # Enemy hit animation
            drawCharacter('hit', 2)
            pausePrompt(200)

        # Player 1 swaps
        else:
            resetGameDisplay()
            drawCharacter('normal', 1)
            drawCharacter('normal', 2)
            drawMessageBox('Come back, ' + p1Primary['Name'] + '!', '')
            pausePrompt(200)

            # Swap occurs
            swapMon(1)

            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            drawPlatform(2)
            drawCharacter('normal', 2)
            healthBar(2)

            pygame.display.update()
            ##pygame.time.delay(600)
            sleep(0.6)

            drawMessageBox('Go, ' + p1Primary['Name'] + '!', '')
            pausePrompt(200)

            resetGameDisplay()
            drawCharacter('normal', 1)
            drawCharacter('normal', 2)
            pygame.display.update()
            ##pygame.time.delay(400)
            sleep(0.2)

    else:
        # Player 2 attacks
        if len(action) > 1 or p2Backup['CurrentHP'] <= 0:
            if action == 'S':
                action = p2Move

            # Reset display
            resetGameDisplay()
            drawCharacter('normal', 1)
            drawMessageBox(p2Primary['Name'] + ' used ' + action + '!', '')

            # Player attack animation
            drawCharacter('attack', 2)
            pausePrompt(200)

            # Reset display
            resetGameDisplay()
            drawCharacter('normal', 2)

            # Only performs attack
            damage, powerMsg, fainted = playerAttacks(action, 2)
            if fainted:
                return

            # Reset display
            resetGameDisplay()
            drawCharacter('normal', 2)

            if powerMsg == 'SuperE':
                print('Super effective attack')
                drawMessageBox(p2Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's super effective!")
            elif powerMsg == 'NotVE':
                print('Not very effective attack')
                drawMessageBox(p2Primary['Name'] + " attacks for " + str(damage) + " damage.", "It's not very effective...")
            else:
                drawMessageBox(p2Primary['Name'] + " attacks for " + str(damage) + " damage.", '')

            # Update health bars
            healthBar(1)
            healthBar(2)

            # Enemy hit animation
            drawCharacter('hit', 1)
            pausePrompt(200)

        # Player 2 swaps
        else:
            resetGameDisplay()
            drawCharacter('normal', 1)
            drawCharacter('normal', 2)
            drawMessageBox('Trainer Ethan is calling back ' + p2Primary['Name'] + '!', '')
            pausePrompt(200)

            # Swap occurs
            swapMon(2)

            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            drawPlatform(1)
            drawCharacter('normal', 1)
            healthBar(1)

            pygame.display.update()
            ##pygame.time.delay(600)
            sleep(0.6)

            drawMessageBox('Trainer Ethan sent out ' + p2Primary['Name'] + '!', '')
            pausePrompt(200)

            resetGameDisplay()
            drawCharacter('normal', 1)
            drawCharacter('normal', 2)
            pygame.display.update()
            ##pygame.time.delay(400)
            sleep(0.2)


def playerAttacks(move, player):
    if player == 1:
        # Inflicting damage to player 2
        damage, powerMsg = calculateDamage(p1Primary['ATK'], moveTypes[move], p1Primary['Type'], moveBaseDmg[move], p2Primary['Type'])
        pygame.mixer.Sound.play(hitSFX)
        if p2Primary['CurrentHP'] < damage:
            p2Primary['CurrentHP'] = 0
            newStats['Damage'] += damage # Add damage to stats
            fainted = checkIfFainted()
        else:
            p2Primary['CurrentHP'] = p2Primary['CurrentHP'] - damage
            newStats['Damage'] += damage # Add damage to stats
            fainted = checkIfFainted()
    else:
        # Inflicting damage to player 1
        damage, powerMsg = calculateDamage(p2Primary['ATK'], moveTypes[move], p2Primary['Type'], moveBaseDmg[move], p1Primary['Type'])
        pygame.mixer.Sound.play(hitSFX)
        if p1Primary['CurrentHP'] < damage:
            p1Primary['CurrentHP'] = 0
            fainted = checkIfFainted()
        else:
            p1Primary['CurrentHP'] = p1Primary['CurrentHP'] - damage
            fainted = checkIfFainted()

    print(str(damage) + ' dealt')
    return damage, powerMsg, fainted


def calculateDamage(AtkStat, moveType, monType, baseDamage, oppType):
    print('running calculateDamage')

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
    if p1Primary['CurrentHP'] == 0:
        fainted = True
        print('p1 primary mon fainted')

        # Perform swap if fainted
        resetGameDisplay()
        drawCharacter('normal', 1)
        drawCharacter('normal', 2)
        drawMessageBox(p1Primary['Name'] + ' fainted!', '')
        pausePrompt(200)

        if p1Backup['CurrentHP'] == 0:
            # Player loses, AI wins
            print('p1 loses')
            win = False

            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            drawPlatform(2)
            healthBar(2)
            drawCharacter('normal', 2)
            drawMessageBox('You have lost the battle!', '')
            pausePrompt(600)
            resultsScreen(win)

        # Swap occurs
        else:
            swapMon(1)

            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            drawPlatform(2)
            drawCharacter('normal', 2)
            healthBar(2)

            pygame.display.update()
            ##pygame.time.delay(600)
            sleep(0.6)

            drawMessageBox('Go, ' + p1Primary['Name'] + '!', '')
            pausePrompt(200)

            resetGameDisplay()
            drawCharacter('normal', 1)
            drawCharacter('normal', 2)
            pygame.display.update()
            ##pygame.time.delay(400)
            sleep(0.2)

    elif p2Primary['CurrentHP'] == 0:
        fainted = True
        print('p2 primary mon fainted')

        # Perform swap if fainted

        resetGameDisplay()
        drawCharacter('normal', 1)
        drawCharacter('normal', 2)
        drawMessageBox(p2Primary['Name'] + ' fainted!', '')
        pausePrompt(200)

        if p2Backup['CurrentHP'] == 0:
            # Player wins
            print('p1 wins')
            win = True

            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            drawPlatform(1)
            healthBar(1)
            drawCharacter('normal', 1)
            drawMessageBox('You have won the battle!', '')
            pausePrompt(600)
            resultsScreen(win)

        # Swap occurs
        else:
            swapMon(2)

            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            drawPlatform(1)
            drawCharacter('normal', 1)
            healthBar(1)

            pygame.display.update()
            ##pygame.time.delay(600)
            sleep(0.6)

            drawMessageBox('Trainer Ethan brought out ' + p2Primary['Name'] + '!', '')
            pausePrompt(200)

            resetGameDisplay()
            drawCharacter('normal', 1)
            drawCharacter('normal', 2)
            pygame.display.update()
            ##pygame.time.delay(400)
            sleep(0.2)

    return fainted


def resetGameDisplay():
    # Excludes character sprites and message box
    gameDisplay.fill(white)
    gameDisplay.blit(gameBackground, (0,0))
    drawPlatform(1)
    drawPlatform(2)
    healthBar(1)
    healthBar(2)

def pausePrompt(waitTime):
    # Draws the arrow prompt and sleeps the program for a short time
    pygame.display.update()

    waitTime = waitTime / 1000
    sleep(waitTime)

    ##pygame.time.delay(waitTime)
    drawArrowPrompt()
    paused()

def setMon(p1P_Pick, p1B_Pick, p2P_Pick, p2B_Pick):
    # Copy dictionaries
    global p1Primary, p2Primary, p1Backup, p2Backup
    p1Primary = copy.deepcopy(Megabite)
    p1Backup = copy.deepcopy(Drogon)
    p2Primary = copy.deepcopy(Snowbro)
    p2Backup = copy.deepcopy(Megabite)

    # For debugging
    print('p1Primary:', p1Primary)
    print('p1Backup:', p1Backup)
    print('p2Primary:', p2Primary)
    print('p2Backup:', p2Backup)

def defineMoves():
    # Returns the Mons' moves
    if p1Primary['Name'] == 'Megabite':
        p1Move = 'Sharp Teeth'
    elif p1Primary['Name'] == 'Snowbro':
        p1Move = 'Ice Shards'
    else:
        p1Move = 'Fireball'

    if p2Primary['Name'] == 'Megabite':
        p2Move = 'Sharp Teeth'
    elif p2Primary['Name'] == 'Snowbro':
        p2Move = 'Ice Shards'
    else:
        p2Move = 'Fireball'
    return p1Move, p2Move

def initiateAttack():
    # Called when player clicks Attack
    p1Move, p2Move, = defineMoves()

    if p1Primary['SPD'] > p2Primary['SPD']:
        print('P1 moves first')
        playerMove(p1Move, 1)
        p1Move, p2Move, = defineMoves()
        playerMove(p2Move, 2)
    elif p2Primary['SPD'] > p1Primary['SPD']:
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

    newStats['Turns'] += 1 # Add turn to stats


def initiateSwap():
    # Called when player clicks Swap

    global timesSwapped
    # If backup mon is fainted, Player cannot swap
    if p1Backup['CurrentHP'] == 0:
        resetGameDisplay()
        drawCharacter('normal', 1)
        drawCharacter('normal', 2)
        drawMessageBox("You can't swap right now!", "Your backup Mon is already fainted.")
        pausePrompt(200)
        return
        ##continue
    # If player has used all three swaps, Player cannot swap
    elif timesSwapped >= 3:
        resetGameDisplay()
        drawCharacter('normal', 1)
        drawCharacter('normal', 2)
        drawMessageBox("You can't swap right now!", "You have used all three of your swaps.")
        pausePrompt(200)
        return
        ##continue

    p1Move, p2Move, = defineMoves()

    if p1Primary['SPD'] > p2Primary['SPD']:
        print('P1 moves first')
        playerMove('S', 1)
        timesSwapped += 1
        p1Move, p2Move, = defineMoves()
        playerMove(p2Move, 2)

    elif p2Primary['SPD'] > p1Primary['SPD']:
        print('P2 moves first')
        playerMove(p2Move, 2)
        p1Move, p2Move, = defineMoves()
        playerMove('S', 1)
        timesSwapped += 1

    else:
        print('Both Pius Mon have same SPD stat! Starting coin toss...')
        coinToss = random.choice([1,2])
        if coinToss == 1:
            print('P1 moves first')
            playerMove('S', 1)
            timesSwapped += 1
            p1Move, p2Move, = defineMoves()
            playerMove(p2Move, 2)
        else:
            print('P2 moves first')
            playerMove(p2Move, 2)
            p1Move, p2Move, = defineMoves()
            playerMove('S', 1)
            timesSwapped += 1

    print('Times swapped:', timesSwapped)
    newStats['Turns'] += 1 # Add turn to stats

def readStats():
    # Load stats from file "stats.txt" into dictionary "stats"
    stats = {}
    f = open('stats.txt', 'r')
    for line in f:
        line = line.split(': ')
        stats[line[0]] = int(line[1])

    f.close()
    ##print('stats:',stats)
    return stats

def writeStats(stats, win):
    print('newStats =',newStats)
    print('stats =',stats)
    if newStats['Turns'] < stats['Fastest Game']:
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

    value = stats['Total Damage'] + newStats['Damage']
    f.write('Total Damage: ' + str(value) + '\n')

    value = stats['Total Turns'] + newStats['Turns']
    f.write('Total Turns: ' + str(value) + '\n')

    # If player sets a new move record, change the "Fastest Game" value to the new record
    if newRecord:
        f.write('Fastest Game: ' + str(newStats['Turns']))
    else:
        f.write('Fastest Game: ' + str(stats['Fastest Game']))
    f.close()

def paused():
    # Wait for user input (key press OR mouse click) to unpause game
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
    print('resetGame')

    # Reset global variables

    global p1Primary, p1Backup, p2Primary, p2Backup, timesSwapped
    p1Primary = {}
    p1Backup = {}
    p2Primary = {}
    p2Backup = {}
    newStats = {'Damage': 0, 'Turns': 0}
    timesSwapped = 0

    titleScreen()

def resultsScreen(win):
    # Write stats to file
    stats = readStats()
    writeStats(stats, win)
    print('Stats written to file.')

    pygame.mixer.music.fadeout(500) # Stop music

    if win:
        winScreen()
    else:
        loseScreen()


def winScreen():
    inResultsScreen = True
    while inResultsScreen:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.fill(white)
        gameDisplay.blit(titleBackground, (0,0))

        # Draw heading
        text = pygame.font.SysFont('segoeui', 80, bold=True)
        textSurf, textRect = textObjects('Victory!', text, black)
        textRect.center = ((displayWidth/2, 80))
        gameDisplay.blit(textSurf, textRect)

        text = pygame.font.SysFont('segoeui', 25, bold=True)

        textSurf, textRect = textObjects('You took ' + str(newStats['Turns']) + ' turns', text, black)
        textRect.topleft = ((25, 180))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = textObjects('You dealt a total of ' + str(newStats['Damage']) + ' damage in this battle', text, black)
        textRect.topleft = ((25, 220))
        gameDisplay.blit(textSurf, textRect)

        button('Main Menu',610,520,150,50,waterBlue,iceBlue,black,resetGame)

        pygame.display.update()
        clock.tick(30)

def loseScreen():
    inResultsScreen = True
    while inResultsScreen:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.fill(white)
        gameDisplay.blit(titleBackground, (0,0))

        # Draw heading
        text = pygame.font.SysFont('segoeui', 80, bold=True)
        textSurf, textRect = textObjects('You lost...', text, black)
        textRect.center = ((displayWidth/2, 80))
        gameDisplay.blit(textSurf, textRect)

        text = pygame.font.SysFont('segoeui', 25, bold=True)

        textSurf, textRect = textObjects('You took ' + str(newStats['Turns']) + ' turns', text, black)
        textRect.topleft = ((25, 180))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = textObjects('You dealt a total of ' + str(newStats['Damage']) + ' damage in this battle', text, black)
        textRect.topleft = ((25, 220))
        gameDisplay.blit(textSurf, textRect)

        button('Main Menu',610,520,150,50,waterBlue,iceBlue,black,resetGame)

        pygame.display.update()
        clock.tick(30)

def titleScreen():
    print('running titleScreen')
    inTitleScreen = True
    while inTitleScreen:
        for event in pygame.event.get():
            ##print(event)
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                if event.key == pygame.K_ESCAPE:
                    quitGame()
        gameDisplay.fill(white)
        gameDisplay.blit(titleBackground, (0,0))

        # Draw logo
        rect = logo.get_rect()
        rect.center = (displayWidth/2, displayHeight/2)
        gameDisplay.blit(logo, rect)

        # Draw buttons
        button('Start Game',300,450,200,50,darkGreen,green,white,gameLoop)
        button('Quit',300,520,200,50,red,brightRed,white,quitGame)
        button('View Stats',610,30,150,50,waterBlue,iceBlue,black, statsScreen)

        pygame.display.update()
        clock.tick(30)

def statsScreen():
    print('running statsScreen')
    stats = readStats()

    inStatsScreen = True
    while inStatsScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        gameDisplay.fill(white)
        gameDisplay.blit(titleBackground, (0,0))

        # Draw heading
        text = pygame.font.SysFont('segoeui', 60, bold=True)
        textSurf, textRect = textObjects('Statistics', text, black)
        textRect.center = ((displayWidth/2, 60))
        gameDisplay.blit(textSurf, textRect)

        # Draw stat text
        text = pygame.font.SysFont('segoeui', 25, bold=True)

        textSurf, textRect = textObjects('Battles won: ' + str(stats['Battles Won']), text, black)
        textRect.topleft = ((25, 140))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = textObjects('Games played: ' + str(stats['Games Played']), text, black)
        textRect.topleft = ((25, 180))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = textObjects('Total damage: ' + str(stats['Total Damage']), text, black)
        textRect.topleft = ((25, 220))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = textObjects('Total turns: ' + str(stats['Total Turns']), text, black)
        textRect.topleft = ((25, 260))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = textObjects('Fastest game: ' + str(stats['Fastest Game']) + ' turns', text, black)
        textRect.topleft = ((25, 300))
        gameDisplay.blit(textSurf, textRect)

        # Draw back button
        button('Main Menu',610,520,150,50,waterBlue,iceBlue,black,titleScreen)

        pygame.display.update()
        clock.tick(30)

def gameIntro(trainerName):
    print('running gameIntro')

    inIntro = True
    while inIntro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(white)
        gameDisplay.blit(gameBackground, (0,0))
        x = displayWidth
        rect = TrainerEthan.get_rect()
        rect.center = ((displayWidth/2), (displayHeight/2))
        gameDisplay.blit(TrainerEthan, rect)

        # Trainer moves to center of screen
        cinematic = True
        while cinematic:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame()
            x -= 20
            gameDisplay.fill(white)
            gameDisplay.blit(gameBackground, (0,0))
            rect = TrainerEthan.get_rect()
            rect.center = ((x), (displayHeight/2))
            gameDisplay.blit(TrainerEthan,rect)
            drawMessageBox('Trainer Ethan challenges you to a battle!', '')
            pygame.display.update()
            clock.tick(60)

            # Stop moving when image is at center of screen
            if x <= displayWidth/2:
                cinematic = False

        drawMessageBox('Trainer Ethan challenges you to a battle!', '')
        pausePrompt(600)

        gameDisplay.fill(white)
        gameDisplay.blit(gameBackground, (0,0))
        drawPlatform(2)
        drawCharacter('normal', 2)
        drawMessageBox('Trainer Ethan sent out ' + p2Primary['Name'] + '!', '')
        pausePrompt(200)

        gameDisplay.fill(white)
        gameDisplay.blit(gameBackground, (0,0))
        drawPlatform(1)
        drawCharacter('normal', 1)
        drawMessageBox(trainerName + ' sent out ' + p1Primary['Name'] + '!', '')

        drawPlatform(2)
        drawCharacter('normal', 2)

        pausePrompt(200)

        inIntro = False


def gameLoop():
    print('running gameLoop')
    global timesSwapped
    timesSwapped = 0

    # Music
    pygame.mixer.music.load('Sounds\BattleMusic.mp3')
    pygame.mixer.music.play(-1)

    # Hardcoding values for testing
    p1PrimaryPick = 'Megabite'
    p1BackupPick = 'Drogon'
    p2PrimaryPick = 'Snowbro'
    p2BackupPick = 'Megabite'
    setMon(p1PrimaryPick, p1BackupPick, p2PrimaryPick, p2BackupPick)
    trainerName = 'Trainer Pat'

    gameIntro(trainerName)

    newStats['Turns'] += 1 # Add turn to stats

    resetGameDisplay()
    drawCharacter('normal', 2)
    drawCharacter('normal', 1)
    drawMovePrompt('What will ' + p1Primary['Name'] + ' do?')
    pygame.display.update()
    sleep(0.5)

    inGame = True
    while inGame:
        for event in pygame.event.get():
            ##print(event)
            if event.type == QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Player chooses to attack
                    initiateAttack()

                    resetGameDisplay()
                    drawCharacter('normal', 2)
                    drawCharacter('normal', 1)
                    drawMovePrompt('What will ' + p1Primary['Name'] + ' do?')
                    pygame.display.update()
                    sleep(0.5)

                # Player chooses to swap
                if event.key == pygame.K_s:
                    initiateSwap()

                    resetGameDisplay()
                    drawCharacter('normal', 2)
                    drawCharacter('normal', 1)
                    drawMovePrompt('What will ' + p1Primary['Name'] + ' do?')
                    pygame.display.update()
                    sleep(0.5)


        resetGameDisplay()

        # Draw characters
        drawCharacter('normal', 2)
        drawCharacter('normal', 1)

        drawMovePrompt('What will ' + p1Primary['Name'] + ' do?')

        # Buttons
        button('Attack', 390, 520, 150, 50, red, brightRed, white, initiateAttack)
        button('Swap', 560, 520, 150, 50, waterBlue, iceBlue, black, initiateSwap)

        pygame.display.update()
        clock.tick(30)


# Main program

titleScreen()
gameLoop()

quitGame()
