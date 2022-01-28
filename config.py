from pprint import pprint as print
import os
import pygame as pg

TILE_SIZE = 64
WIN_SIZE = (800, 600)
# WIN_SIZE = (1920, 1080)
FPS = 60


current_dir = os.path.dirname(__file__)
assets = os.path.join(current_dir, 'assets')
lvls = os.path.join(current_dir, 'lvls')

ASSETS_MENU_DIR = os.path.join(assets, "menu")

MENU_BACKGROUND = os.path.join(ASSETS_MENU_DIR, "1.jpeg")

BUTTONS_DIR = os.path.join(ASSETS_MENU_DIR, "buttons")

BUTTONS = dict()

for button in sorted(os.listdir(BUTTONS_DIR), key=lambda x: len(x)):
    name = button.split("_")
    try:
        if len(name) == 3:
            BUTTONS[name[1]].append(os.path.join(BUTTONS_DIR, button))
        else:
            BUTTONS[name[1].rstrip(".png")].append(os.path.join(BUTTONS_DIR, button))
    except:
        if len(name) == 3:
            BUTTONS[name[1]] = [os.path.join(BUTTONS_DIR, button)]
        else:
            BUTTONS[name[1].rstrip(".png")] = [os.path.join(BUTTONS_DIR, button)]
        

blocks = os.path.join(assets, 'blocks')

consumables = os.path.join(assets, 'consumables')

PLAYER_DIR = os.path.join(assets, 'player')

MISSING = os.path.join(assets, 'pepga.png')
SPIKE = os.path.join(assets, 'spike.png')

PLAYER_ASSETS = dict()

for asset_dir in os.listdir(PLAYER_DIR):
    PLAYER_ASSETS[asset_dir.lstrip("/")] = [os.path.join(os.path.join(PLAYER_DIR, asset_dir), elem) for elem in os.listdir(os.path.join(PLAYER_DIR, asset_dir))]


coins = os.path.join(consumables, 'coins')
COINS = [os.path.join(coins, 'Coin_Purple.png'),
         os.path.join(coins, 'Coin_Blue.png'),
         os.path.join(coins, 'Coin_Gold.png'),
         os.path.join(coins, 'Coin_Green.png'),
         os.path.join(coins, 'Coin_Red.png')]

LEVELS = [os.path.join(lvls, f'lvl{n}.txt') for n in range(len([f for f in os.listdir(lvls)]))]

BLOCK_ASSETS = {'-': os.path.join(blocks, 'stone.png'),
                '0': os.path.join(blocks, 'trail.png'),
                '*': os.path.join(blocks, 'sand.png'),
                '1': os.path.join(blocks, 'stone_2.png'),
                '2': os.path.join(blocks, 'trail_2.png'),
                '&': os.path.join(blocks, 'water.png'),
                '?': os.path.join(blocks, 'water_with_stone.png'),
                '=': os.path.join(blocks, 'lava.png'),
                '#': os.path.join(blocks, 'bush.png'),
                '3': os.path.join(blocks, 'snow.png'),
                '+': os.path.join(blocks, 'grass.png')
                }




MAP = {
    'C': COINS[0],
    '@': PLAYER_ASSETS['idle'],
    '-': BLOCK_ASSETS['-'],
    '0': BLOCK_ASSETS['0'],
    '*': BLOCK_ASSETS['*'],
    '1': BLOCK_ASSETS['1'],
    '2': BLOCK_ASSETS['2'],
    '&': BLOCK_ASSETS['&'],
    '?': BLOCK_ASSETS['?'],
    '=': BLOCK_ASSETS['='],
    '#': BLOCK_ASSETS['#'],
    '3': BLOCK_ASSETS['3'],
    '+': BLOCK_ASSETS['+'],
    }

SOLID_BLOCKS = '&?=#-+1'
UNSOLID_BLOCKS = '*320'