import draw, logic, statHandler, config as cfg
import pygame
from pygame.locals import *
from time import sleep

def resultsScreen(win):
    '''Displays game results screen.
    This function passes on to winScreen() or loseScreen() based on game outcome.

    win -- boolean; whether or not the human player won the game
    '''
    # Write stats to file
    stats = statHandler.readJson()
    statHandler.writeJson(stats, win)
    print('Stats written to file.')

    # Stop music playback
    pygame.mixer.music.fadeout(500)

    if win:
        winScreen()
    else:
        loseScreen()

def winScreen():
    '''Displays the win screen.'''
    inResultsScreen = True
    while inResultsScreen:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw heading
        text = pygame.font.SysFont('segoeui', 80, bold=True)
        textSurf, textRect = draw.textObjects('Victory!', text, cfg.black)
        textRect.center = ((cfg.displayWidth/2, 80))
        cfg.gameDisplay.blit(textSurf, textRect)

        text = pygame.font.SysFont('segoeui', 25, bold=True)

        textSurf, textRect = draw.textObjects('You took ' + str(cfg.newStats['Turns']) + ' turns', text, cfg.black)
        textRect.topleft = ((25, 180))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('You dealt a total of ' + str(cfg.newStats['Damage']) + ' damage in this battle', text, cfg.black)
        textRect.topleft = ((25, 220))
        cfg.gameDisplay.blit(textSurf, textRect)

        draw.button('Main Menu',610,520,150,50, cfg.waterBlue, cfg.iceBlue, cfg.black, logic.resetGame)

        pygame.display.update()
        cfg.clock.tick(30)

def loseScreen():
    '''Displays the lose screen.'''
    inResultsScreen = True
    while inResultsScreen:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw heading
        text = pygame.font.SysFont('segoeui', 80, bold=True)
        textSurf, textRect = draw.textObjects('You lost...', text, cfg.black)
        textRect.center = ((cfg.displayWidth/2, 80))
        cfg.gameDisplay.blit(textSurf, textRect)

        text = pygame.font.SysFont('segoeui', 25, bold=True)

        textSurf, textRect = draw.textObjects('You took ' + str(cfg.newStats['Turns']) + ' turns', text, cfg.black)
        textRect.topleft = ((25, 180))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('You dealt a total of ' + str(cfg.newStats['Damage']) + ' damage in this battle', text, cfg.black)
        textRect.topleft = ((25, 220))
        cfg.gameDisplay.blit(textSurf, textRect)

        draw.button('Main Menu',610,520,150,50, cfg.waterBlue, cfg.iceBlue, cfg.black, logic.resetGame)

        pygame.display.update()
        cfg.clock.tick(30)

def titleScreen():
    '''Displays the Pius Mon title screen.'''
    inTitleScreen = True
    while inTitleScreen:
        for event in pygame.event.get():
            ##print(event)
            if event.type == pygame.QUIT:
                logic.quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                if event.key == pygame.K_ESCAPE:
                    logic.quitGame()
        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw logo
        rect = cfg.logo.get_rect()
        rect.center = (cfg.displayWidth/2, cfg.displayHeight/2)
        cfg.gameDisplay.blit(cfg.logo, rect)

        # Draw buttons
        # NOTE: Change action to test out selection screen
        draw.button('Start Game',300,450,200,50, cfg.darkGreen, cfg.green, cfg.white,gameLoop)
        draw.button('Quit',300,520,200,50, cfg.red, cfg.brightRed, cfg.white, logic.quitGame)
        draw.button('View Stats',610,30,150,50, cfg.waterBlue, cfg.iceBlue, cfg.black, statsScreen)

        pygame.display.update()
        cfg.clock.tick(30)

def statsScreen():
    '''Displays the stats screen.'''
    stats = statHandler.readJson()
    winRatio = logic.winRatio(stats['BattlesWon'], stats['GamesPlayed'])

    inStatsScreen = True
    while inStatsScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw heading
        text = pygame.font.SysFont('segoeui', 60, bold=True)
        textSurf, textRect = draw.textObjects('Career Stats', text, cfg.black)
        textRect.center = ((cfg.displayWidth/2, 60))
        cfg.gameDisplay.blit(textSurf, textRect)

        # Draw stat text
        text = pygame.font.SysFont('segoeui', 25, bold=True)

        textSurf, textRect = draw.textObjects('Battles won: ' + str(stats['BattlesWon']), text, cfg.black)
        textRect.topleft = ((40, 140))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('Games played: ' + str(stats['GamesPlayed']), text, cfg.black)
        textRect.topleft = ((40, 180))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('Win ratio: ' + str(winRatio) + '%', text, cfg.black)
        textRect.topleft = ((40, 220))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('Total damage: ' + str(stats['TotalDamage']), text, cfg.black)
        textRect.topleft = ((40, 260))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('Total turns: ' + str(stats['TotalTurns']), text, cfg.black)
        textRect.topleft = ((40, 300))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('Fastest game: ' + str(stats['FastestGame']) + ' turns', text, cfg.black)
        textRect.topleft = ((40, 340))
        cfg.gameDisplay.blit(textSurf, textRect)

        # Draw back button
        draw.button('Main Menu', 560,520,200,50, cfg.waterBlue, cfg.iceBlue, cfg.black, titleScreen)
        draw.button('Reset Stats', 40,520,150,50, cfg.red, cfg.brightRed, cfg.white, confirmStatReset)

        pygame.display.update()
        cfg.clock.tick(30)

def confirmStatReset():
    '''Confirmation screen for resetting player stats.'''
    cfg.gameDisplay.fill(cfg.white)
    cfg.gameDisplay.blit(cfg.titleBackground, (0,0))
    draw.shadedSurface()
    pygame.draw.rect(cfg.gameDisplay, cfg.black,(50,50,700,500),2)

    text = pygame.font.SysFont('segoeui', 25, bold=True)
    textSurf, textRect = draw.textObjects('Are you sure you want to erase your career statistics?', text, cfg.black)
    textRect.center = ((cfg.displayWidth/2, 200))
    cfg.gameDisplay.blit(textSurf, textRect)

    textSurf, textRect = draw.textObjects('This action can not be undone.', text, cfg.black)
    textRect.center = ((cfg.displayWidth/2, 240))
    cfg.gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    sleep(1.5)

    pygame.draw.rect(cfg.gameDisplay, cfg.brightRed,(50,50,700,500),2)
    pygame.display.update()
    sleep(1.5)

    inScreen = True
    while inScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))
        draw.shadedSurface()
        pygame.draw.rect(cfg.gameDisplay, cfg.brightRed,(50,50,700,500),2)

        text = pygame.font.SysFont('segoeui', 25, bold=True)
        textSurf, textRect = draw.textObjects('Are you sure you want to erase your career statistics?', text, cfg.black)
        textRect.center = ((cfg.displayWidth/2, 200))
        cfg.gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = draw.textObjects('This action can not be undone.', text, cfg.black)
        textRect.center = ((cfg.displayWidth/2, 240))
        cfg.gameDisplay.blit(textSurf, textRect)

        # Button resets stats
        draw.button('Erase Stats', 100,450,150,50, cfg.red, cfg.brightRed, cfg.white, statHandler.resetJson)

        # Button to cancel
        draw.button('Cancel', 500,450,200,50, cfg.waterBlue, cfg.iceBlue, cfg.black, statsScreen)

        pygame.display.update()
        cfg.clock.tick(30)

def gameIntro(trainerName):
    '''Displays the game intro scene.
    This scene introduces the opponent and the two Mon who will be fighting.

    trainerName -- nickname of the human player
    '''
    inIntro = True
    while inIntro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logic.quitGame()
        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
        x = cfg.displayWidth
        rect = cfg.TrainerEthan.get_rect()
        rect.center = ((cfg.displayWidth/2), (cfg.displayHeight/2))
        cfg.gameDisplay.blit(cfg.TrainerEthan, rect)

        # Trainer moves to center of screen
        cinematic = True
        while cinematic:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logic.quitGame()
            x -= 20
            cfg.gameDisplay.fill(cfg.white)
            cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
            rect = cfg.TrainerEthan.get_rect()
            rect.center = ((x), (cfg.displayHeight/2))
            cfg.gameDisplay.blit(cfg.TrainerEthan,rect)
            draw.messageBox('Trainer Ethan challenges you to a battle!', '')
            pygame.display.update()
            cfg.clock.tick(60)

            # Stop moving when image is at center of screen
            if x <= cfg.displayWidth/2:
                cinematic = False

        draw.messageBox('Trainer Ethan challenges you to a battle!', '')
        draw.pausePrompt(600)

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
        draw.platform(2)
        draw.character('normal', 2)
        draw.messageBox('Trainer Ethan sent out ' + cfg.p2Primary['Name'] + '!', '')
        draw.pausePrompt(200)

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.gameBackground, (0,0))
        draw.platform(1)
        draw.character('normal', 1)
        draw.messageBox(trainerName + ' sent out ' + cfg.p1Primary['Name'] + '!', '')

        draw.platform(2)
        draw.character('normal', 2)

        draw.pausePrompt(200)

        inIntro = False


def gameLoop():
    '''This scene comprises the main Pius Mon game flow.'''
    # timesSwapped variable moved to config.py

    # Music
    pygame.mixer.music.load('Sounds\BattleMusic.mp3')
    pygame.mixer.music.play(-1)

    # Hardcoding values for testing
    p1PrimaryPick = 'Megabite'
    p1BackupPick = 'Drogon'
    p2PrimaryPick = 'Snowbro'
    p2BackupPick = 'Megabite'
    logic.setMon(p1PrimaryPick, p1BackupPick, p2PrimaryPick, p2BackupPick)
    cfg.trainerName = 'Trainer Pat'

    gameIntro(cfg.trainerName)

    cfg.newStats['Turns'] += 1 # Add turn to stats

    draw.resetGameDisplay()
    draw.character('normal', 2)
    draw.character('normal', 1)
    draw.movePrompt('What will ' + cfg.p1Primary['Name'] + ' do?')
    pygame.display.update()
    sleep(0.5)

    inGame = True
    while inGame:
        for event in pygame.event.get():
            ##print(event)
            if event.type == QUIT:
                logic.quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Player chooses to attack
                    logic.initiateAttack()

                    draw.resetGameDisplay()
                    draw.character('normal', 2)
                    draw.character('normal', 1)
                    draw.movePrompt('What will ' + cfg.p1Primary['Name'] + ' do?')
                    pygame.display.update()
                    sleep(0.5)

                # Player chooses to swap
                if event.key == pygame.K_s:
                    logic.initiateSwap()

                    draw.resetGameDisplay()
                    draw.character('normal', 2)
                    draw.character('normal', 1)
                    draw.movePrompt('What will ' + cfg.p1Primary['Name'] + ' do?')
                    pygame.display.update()
                    sleep(0.5)


        draw.resetGameDisplay()

        # Draw characters
        draw.character('normal', 2)
        draw.character('normal', 1)

        draw.movePrompt('What will ' + cfg.p1Primary['Name'] + ' do?')

        # Buttons
        draw.button('Attack', 390, 520, 150, 50, cfg.red, cfg.brightRed, cfg.white, logic.initiateAttack)
        draw.button('Swap', 560, 520, 150, 50, cfg.waterBlue, cfg.iceBlue, cfg.black, logic.initiateSwap)

        pygame.display.update()
        cfg.clock.tick(30)