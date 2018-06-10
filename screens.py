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
    headerFont = pygame.font.SysFont('segoeui', 80, bold=True)
    font = pygame.font.SysFont('segoeui', 25, bold=True)
    inResultsScreen = True
    while inResultsScreen:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw heading
        draw.drawText('Victory!', headerFont, cfg.black, 'center', cfg.displayWidth/2, 80)

        # Draw text
        draw.drawText('You took ' + str(cfg.newStats['Turns']) + ' turns', font, cfg.black, 'topleft', 25, 180)
        draw.drawText('You dealt a total of ' + str(cfg.newStats['Damage']) + ' damage in this battle', font, cfg.black, 'topleft', 25, 220)

        # Draw button
        draw.button('Main Menu',610,520,150,50, cfg.waterBlue, cfg.iceBlue, cfg.black, logic.resetGame)

        pygame.display.update()
        cfg.clock.tick(30)

def loseScreen():
    '''Displays the lose screen.'''
    headerFont = pygame.font.SysFont('segoeui', 80, bold=True)
    font = pygame.font.SysFont('segoeui', 25, bold=True)
    inResultsScreen = True
    while inResultsScreen:
        for event in pygame.event.get():
            click = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw heading
        draw.drawText('You lost...', headerFont, cfg.black, 'center', cfg.displayWidth/2, 80)

        # Draw text
        draw.drawText('You took ' + str(cfg.newStats['Turns']) + ' turns', font, cfg.black, 'topleft', 25, 180)
        draw.drawText('You dealt a total of ' + str(cfg.newStats['Damage']) + ' damage in this battle', font, cfg.black, 'topleft', 25, 220)

        # Draw button
        draw.button('Main Menu',610,520,150,50, cfg.waterBlue, cfg.iceBlue, cfg.black, logic.resetGame)

        pygame.display.update()
        cfg.clock.tick(30)

def titleScreen():
    '''Displays the Pius Mon title screen.'''
    rect = cfg.logo.get_rect()
    rect.center = (cfg.displayWidth/2, cfg.displayHeight/2)
    inTitleScreen = True
    while inTitleScreen:
        for event in pygame.event.get():
            ##print(event)
            if event.type == pygame.QUIT:
                logic.quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selectionScreen()
        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw logo
        cfg.gameDisplay.blit(cfg.logo, rect)

        # Draw buttons
        draw.button('New Game',300,450,200,50, cfg.darkGreen, cfg.green, cfg.white,selectionScreen)
        draw.button('Quit',300,520,200,50, cfg.red, cfg.brightRed, cfg.white, logic.quitGame)
        draw.button('View Stats',610,30,150,50, cfg.waterBlue, cfg.iceBlue, cfg.black, statsScreen)

        pygame.display.update()
        cfg.clock.tick(30)

def statsScreen():
    '''Displays the stats screen.'''
    stats = statHandler.readJson()
    winRatio = logic.winRatio(stats['BattlesWon'], stats['GamesPlayed'])

    headerFont = pygame.font.SysFont('segoeui', 60, bold=True)
    font = pygame.font.SysFont('segoeui', 25, bold=True)

    inStatsScreen = True
    while inStatsScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))

        # Draw heading
        draw.drawText('Career Stats', headerFont, cfg.black, 'center', cfg.displayWidth/2, 60)

        # Draw stat text
        draw.drawText('Battles won: ' + str(stats['BattlesWon']), font, cfg.black, 'topleft', 40, 140)
        draw.drawText('Games played: ' + str(stats['GamesPlayed']), font, cfg.black, 'topleft', 40, 180)
        draw.drawText('Win ratio: ' + str(winRatio) + '%', font, cfg.black, 'topleft', 40, 220)
        draw.drawText('Total damage: ' + str(stats['TotalDamage']), font, cfg.black, 'topleft', 40, 260)
        draw.drawText('Total turns: ' + str(stats['TotalTurns']), font, cfg.black, 'topleft', 40, 300)
        draw.drawText('Fastest game: ' + str(stats['FastestGame']) + ' turns', font, cfg.black, 'topleft', 40, 340)

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

    font = pygame.font.SysFont('segoeui', 25, bold=True)
    draw.drawText('Are you sure you want to erase your career statistics?', font, cfg.black, 'center', cfg.displayWidth/2, 200)
    draw.drawText('This action can not be undone.', font, cfg.black, 'center', cfg.displayWidth/2, 240)
    pygame.display.update()
    sleep(1)

    pygame.draw.rect(cfg.gameDisplay, cfg.brightRed,(50,50,700,500),2)
    pygame.display.update()
    sleep(1)

    inScreen = True
    while inScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logic.quitGame()

        cfg.gameDisplay.fill(cfg.white)
        cfg.gameDisplay.blit(cfg.titleBackground, (0,0))
        draw.shadedSurface()
        pygame.draw.rect(cfg.gameDisplay, cfg.brightRed,(50,50,700,500),2)

        draw.drawText('Are you sure you want to erase your career statistics?', font, cfg.black, 'center', cfg.displayWidth/2, 200)
        draw.drawText('This action can not be undone.', font, cfg.black, 'center', cfg.displayWidth/2, 240)

        # Button resets stats
        draw.button('Erase Stats', 100,450,150,50, cfg.red, cfg.brightRed, cfg.white, statHandler.resetJson)

        # Button to cancel
        draw.button('Cancel', 500,450,200,50, cfg.waterBlue, cfg.iceBlue, cfg.black, statsScreen)

        pygame.display.update()
        cfg.clock.tick(30)

def selectionScreen():
    '''Displays the Mon selection screen.'''
    cfg.gameDisplay.fill(cfg.pokemonYellow)
    headerFont = pygame.font.SysFont('segoeui', 40, bold=True)
    font = pygame.font.SysFont('segoeui', 25, bold=True)
    draw.drawText('Select your Primary Mon!', headerFont, cfg.black, 'center', cfg.displayWidth/2, 40)
    pygame.display.update()
    sleep(0.5)

    inScreen = True
    while inScreen:
        for event in pygame.event.get():
            ##print(event)
            if event.type == pygame.QUIT:
                logic.quitGame()
        cfg.gameDisplay.fill(cfg.pokemonYellow)

        headerFont = pygame.font.SysFont('segoeui', 40, bold=True)
        draw.drawText('Select your Primary Mon!', headerFont, cfg.black, 'center', cfg.displayWidth/2, 40)

        draw.thumbnail('Snowbro', 40, 100, 1)
        draw.thumbnail('Megabite', 160, 100, 1)
        draw.thumbnail('None', 280, 100, 1)

        draw.thumbnail('Drogon', 40, 220, 1)
        draw.thumbnail('None', 160, 220, 1)
        draw.thumbnail('None', 280, 220, 1)

        draw.thumbnail('None', 40, 340, 1)
        draw.thumbnail('None', 160, 340, 1)
        draw.thumbnail('None', 280, 340, 1)

        draw.drawText('Your Party:', font, cfg.black, 'topleft', 440, 460)
        draw.drawText('1. (selecting...)', font, cfg.black, 'topleft', 440, 500)
        draw.drawText('2. ---', font, cfg.black, 'topleft', 440, 540)

        # Back button
        draw.button('Back', 40,520,100,50, cfg.waterBlue, cfg.iceBlue, cfg.black, titleScreen)

        pygame.display.update()
        cfg.clock.tick(30)

def selectionScreen2():
    '''Displays the backup selection screen.'''
    cfg.gameDisplay.fill(cfg.pokemonYellow)
    headerFont = pygame.font.SysFont('segoeui', 40, bold=True)
    font = pygame.font.SysFont('segoeui', 25, bold=True)
    draw.drawText('Select your Backup Mon!', headerFont, cfg.black, 'center', cfg.displayWidth/2, 40)
    pygame.display.update()
    sleep(0.5)

    inScreen = True
    while inScreen:
        for event in pygame.event.get():
            ##print(event) #debug
            if event.type == pygame.QUIT:
                logic.quitGame()
        cfg.gameDisplay.fill(cfg.pokemonYellow)

        headerFont = pygame.font.SysFont('segoeui', 40, bold=True)
        draw.drawText('Select your Backup Mon!', headerFont, cfg.black, 'center', cfg.displayWidth/2, 40)

        draw.thumbnail('Snowbro', 40, 100, 2)
        draw.thumbnail('Megabite', 160, 100, 2)
        draw.thumbnail('None', 280, 100, 2)

        draw.thumbnail('Drogon', 40, 220, 2)
        draw.thumbnail('None', 160, 220, 2)
        draw.thumbnail('None', 280, 220, 2)

        draw.thumbnail('None', 40, 340, 2)
        draw.thumbnail('None', 160, 340, 2)
        draw.thumbnail('None', 280, 340, 2)

        draw.drawText('Your Party:', font, cfg.black, 'topleft', 440, 460)
        draw.drawText('1. ' + cfg.primaryPick, font, cfg.black, 'topleft', 440, 500)
        draw.drawText('2. (selecting...)', font, cfg.black, 'topleft', 440, 540)

        # Back button
        draw.button('Back', 40,520,100,50, cfg.waterBlue, cfg.iceBlue, cfg.black, selectionScreen)

        pygame.display.update()
        cfg.clock.tick(30)

def confirmSelection():
    '''Displays the Mon confirmation screen.'''

    cfg.gameDisplay.fill(cfg.pokemonYellow)
    headerFont = pygame.font.SysFont('segoeui', 40, bold=True)
    font = pygame.font.SysFont('segoeui', 25, bold=True)
    draw.drawText('Proceed to Battle?', headerFont, cfg.black, 'center', cfg.displayWidth/2, 40)
    pygame.display.update()
    sleep(0.5)

    inScreen = True
    while inScreen:
        for event in pygame.event.get():
            ##print(event) #debug
            if event.type == pygame.QUIT:
                logic.quitGame()
        cfg.gameDisplay.fill(cfg.pokemonYellow)

        draw.drawText('Proceed to Battle?', headerFont, cfg.black, 'center', cfg.displayWidth/2, 40)
        draw.drawText('You have chosen the following Pius Mon:', font, cfg.black, 'topleft', 40, 90)

        draw.character2(cfg.primaryPick, 40, 120)
        draw.drawText('1. ' + cfg.primaryPick, font, cfg.black, 'topleft', 40, 430)
        draw.character2(cfg.backupPick, 380, 120)
        draw.drawText('2. ' + cfg.backupPick, font, cfg.black, 'topleft', 380, 430)

        draw.button("Start the Battle!", 460,520,300,50, cfg.darkGreen, cfg.green, cfg.white, gameLoop)
        draw.button('Choose Again', 40,520,200,50, cfg.waterBlue, cfg.iceBlue, cfg.black, selectionScreen)

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
    # Music
    pygame.mixer.music.load('Sounds\BattleMusic.mp3')
    pygame.mixer.music.play(-1)

    # Set Mon and trainer name
    logic.setMon(cfg.primaryPick, cfg.backupPick)
    cfg.trainerName = 'Trainer Pat'

    # Start game intro cinematic
    gameIntro(cfg.trainerName)

    # Add turn to stats
    cfg.newStats['Turns'] += 1

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
                # Player chooses to attack
                if event.key == pygame.K_RETURN:
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