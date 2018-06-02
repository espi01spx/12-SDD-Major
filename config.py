# config.py
import pygame
from pygame.locals import *

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

# Times swapped
timesSwapped = 0