# draw.py
import logic, screens, statHandler, config as cfg
import pygame, sys, math, copy, random
from pygame.locals import *
from time import sleep

def textObjects(text, font, textColour):
    textSurface = font.render(text, True, textColour)
    return textSurface, textSurface.get_rect()

def messageDisplay(text, size):
    largeText = pygame.font.SysFont('segoeui', size)
    TextSurf, TextRect = textObjects(text, largeText, cfg.black)
    TextRect.center = ((cfg.displayWidth/2),((cfg.displayHeight/2))-50)
    cfg.gameDisplay.blit(TextSurf, TextRect)

def button(msg,x,y,w,h,ic,ac,tc,action=None):
    '''
    msg = button label
    x,y = top-left coordinates of the button box
    w,h = button width/height
    ic,ac = inactive colour, active colour (on mouse hover)
    tc = text colour
    action = function to trigger on button click
    '''

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(cfg.gameDisplay, ac,(x,y,w,h))
        pygame.draw.rect(cfg.gameDisplay, cfg.black,(x,y,w,h),2)

        if click[0] == 1 and action != None:
            pygame.mixer.Sound.play(cfg.selectSFX)
            action()
            if msg in ['Attack','Swap']:
                resetGameDisplay()
                character('normal', 2)
                character('normal', 1)
                movePrompt('What will ' + cfg.p1Primary['Name'] + ' do?')
                pygame.display.update()
                sleep(0.5)

    else:
        pygame.draw.rect(cfg.gameDisplay, ic,(x,y,w,h))
        pygame.draw.rect(cfg.gameDisplay, cfg.black,(x,y,w,h),2)

    smallText = pygame.font.SysFont('segoeui',20,bold=True)
    textSurf, textRect = textObjects(msg, smallText, tc)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    cfg.gameDisplay.blit(textSurf, textRect)

def messageBox(line1, line2):
    # Draws a message box
    pygame.draw.rect(cfg.gameDisplay, cfg.forestBlue, (0, 486, cfg.displayWidth, 114))
    pygame.draw.rect(cfg.gameDisplay, cfg.white, (0, 486, cfg.displayWidth, 114), 1)

    # Draw line 1
    text = pygame.font.SysFont('verdana', 20, bold=True)
    textSurf, textRect = textObjects(line1, text, cfg.white)
    textRect.topleft = ((25, 502))
    cfg.gameDisplay.blit(textSurf, textRect)

    # Draw line 2
    if line2:
        textSurf, textRect = textObjects(line2, text, cfg.white)
        textRect.topleft = ((25, 550))
        cfg.gameDisplay.blit(textSurf, textRect)

    pygame.display.update()

def movePrompt(line1):
    # Basically the same as drawMessageBox
    # Prompts the user to Attack or Swap

    pygame.draw.rect(cfg.gameDisplay, cfg.forestBlue, (0, 486, cfg.displayWidth, 114))
    pygame.draw.rect(cfg.gameDisplay, cfg.white, (0, 486, cfg.displayWidth, 114), 1)

    # Draw line 1
    text = pygame.font.SysFont('verdana', 20, bold=True)
    textSurf, textRect = textObjects(line1, text, cfg.white)
    textRect.topleft = ((25, 502))
    cfg.gameDisplay.blit(textSurf, textRect)


def healthBar(player):
    # x,y = top-left coordinates of the HP bar's background
    healthBarWidth = 200

    if player == 1:
        x = 550
        y = 400
        currentHP = cfg.p1Primary['CurrentHP']
        maxHP = cfg.p1Primary['MaxHP']
        monName = cfg.p1Primary['Name']
    else:
        x = 50
        y = 50
        currentHP = cfg.p2Primary['CurrentHP']
        maxHP = cfg.p2Primary['MaxHP']
        monName = cfg.p2Primary['Name']

    # Draw health bar background box
    pygame.draw.rect(cfg.gameDisplay, cfg.cream, (x-5, y-35, healthBarWidth+10, 85))
    pygame.draw.rect(cfg.gameDisplay, cfg.black, (x-5, y-35, healthBarWidth+10,85),1)

    # Draw max health bar
    for HP in range(healthBarWidth):
        pygame.draw.rect(cfg.gameDisplay, cfg.black, (x+HP, y, 1, 16), 0)

    ratio = int(max(min(currentHP/float(maxHP)*healthBarWidth,healthBarWidth),0))

    pointer(player)

    # Colour selection
    if ratio >= 100:
        barColour = cfg.green
    elif ratio >= 50:
        barColour = cfg.pokemonYellow
    else:
        barColour = cfg.brightRed

    # Draw current health bar
    for HP in range(ratio):
        pygame.draw.rect(cfg.gameDisplay, barColour, (x+HP, y, 1, 16), 0)
        HP += 1

    # Draw HP text
    msg = 'HP ' + str(currentHP) + ' / ' + str(maxHP)
    text = pygame.font.SysFont('verdana', 15, bold=True)
    textSurf, textRect = textObjects(msg, text, cfg.black)
    textRect.center = ((x+healthBarWidth-50, y+30))
    cfg.gameDisplay.blit(textSurf, textRect)

    # Draw Mon name label
    msg = monName
    text = pygame.font.SysFont('verdana', 15, bold=True)
    textSurf, textRect = textObjects(msg, text, cfg.black)
    textRect.topleft = ((x+5, y-28))
    cfg.gameDisplay.blit(textSurf, textRect)

def pointer(player):
    # Pointers to be attatched to end of health bar
    if player == 2:
        pygame.draw.polygon(cfg.gameDisplay, cfg.cream, ((256,16), (256,98), (280,58)), 0)
    else:
        pygame.draw.polygon(cfg.gameDisplay, cfg.cream, ((542,364), (542,448), (520,406)), 0)

def arrowPrompt():
    pygame.draw.polygon(cfg.gameDisplay, cfg.yellow, ((754, 562), (780, 562), (767, 584)), 0)
    pygame.display.update()

def platform(player):
    # Define colour based on monType
    if player == 1:
        monType = cfg.p1Primary['Type']
    else:
        monType = cfg.p2Primary['Type']

    if monType == 'F':
        colour = cfg.red
    elif monType == 'W':
        colour = cfg.waterBlue
    else:
        colour = cfg.iceBlue

    # Draw platform
    if player == 1:
        pygame.draw.ellipse(cfg.gameDisplay, colour, (30,380,300,100),0)
    else:
        pygame.draw.ellipse(cfg.gameDisplay, colour, (530,200,300,100),0)

def character(state, player):
    # Determine mon's name
    if player == 1:
        mon = cfg.p1Primary['Name']
        rect = cfg.MegabiteNormal.get_rect()
        rect.bottomleft = (32,430)
        flip = False
    else:
        mon = cfg.p2Primary['Name']
        rect = cfg.SnowbroNormal.get_rect()
        rect.bottomleft = (530,234)
        flip = True

    # Now draw sprite, based on Mon name and state
    if mon == 'Megabite':
        if state == 'attack':
            if flip:
                cfg.MegabiteAttackR = pygame.transform.flip(cfg.MegabiteAttack, True, False)
                cfg.gameDisplay.blit(cfg.MegabiteAttackR, rect)
            else:
                cfg.gameDisplay.blit(cfg.MegabiteAttack, rect)
        elif state == 'hit':
            if flip:
                cfg.MegabiteHitR = pygame.transform.flip(cfg.MegabiteHit, True, False)
                cfg.gameDisplay.blit(cfg.MegabiteHitR, rect)
            else:
                cfg.gameDisplay.blit(cfg.MegabiteHit, rect)
        else:
            if flip:
                cfg.MegabiteNormalR = pygame.transform.flip(cfg.MegabiteNormal, True, False)
                cfg.gameDisplay.blit(cfg.MegabiteNormalR, rect)
            else:
                cfg.gameDisplay.blit(cfg.MegabiteNormal, rect)
    elif mon == 'Snowbro':
        if state == 'attack':
            if flip:
                cfg.SnowbroAttack1R = pygame.transform.flip(cfg.SnowbroAttack1, True, False)
                cfg.gameDisplay.blit(cfg.SnowbroAttack1R, rect)
            else:
                cfg.gameDisplay.blit(cfg.SnowbroAttack1, rect)
        elif state == 'hit':
            if flip:
                cfg.SnowbroHitR = pygame.transform.flip(cfg.SnowbroHit, True, False)
                cfg.gameDisplay.blit(cfg.SnowbroHitR, rect)
            else:
                cfg.gameDisplay.blit(cfg.SnowbroHit, rect)
        else:
            if flip:
                cfg.SnowbroNormalR = pygame.transform.flip(cfg.SnowbroNormal, True, False)
                cfg.gameDisplay.blit(cfg.SnowbroNormalR, rect)
            else:
                cfg.gameDisplay.blit(cfg.SnowbroNormal, rect)
    elif mon == 'Drogon':
        if state == 'attack':
            if flip:
                cfg.DrogonAttackR = pygame.transform.flip(cfg.DrogonAttack, True, False)
                cfg.gameDisplay.blit(cfg.DrogonAttackR, rect)
            else:
                cfg.gameDisplay.blit(cfg.DrogonAttack, rect)
        elif state == 'hit':
            if flip:
                cfg.DrogonHitR = pygame.transform.flip(cfg.DrogonHit, True, False)
                cfg.gameDisplay.blit(cfg.DrogonHitR, rect)
            else:
                cfg.gameDisplay.blit(cfg.DrogonHit, rect)
        else:
            if flip:
                cfg.DrogonNormalR = pygame.transform.flip(cfg.DrogonNormal, True, False)
                cfg.gameDisplay.blit(cfg.DrogonNormalR, rect)
            else:
                cfg.gameDisplay.blit(cfg.DrogonNormal, rect)

def resetGameDisplay():
    # Excludes character sprites and message box
    cfg.gameDisplay.fill(cfg.white)
    cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
    platform(1)
    platform(2)
    healthBar(1)
    healthBar(2)

def pausePrompt(waitTime):
    '''
    wait time in milliseconds (ms)
    '''
    # Draws the arrow prompt and sleeps the program for a short time
    pygame.display.update()

    waitTime = waitTime / 1000
    sleep(waitTime)

    arrowPrompt()
    logic.paused()
