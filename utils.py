from objects import *
from enemies import *
from entity import *
from player import Player

def loadMap(assets, mapList):
    blockSize = 64
    MAP_SPRITES = assets['MAP_SPRITE_SHEET']
    platforms = []
    entities = []
    player = None
    for y in range(len(mapList)):
        for x in range(len(mapList[y])):
            tileType = mapList[y][x][0:-1]
            imgInclinaison = int(mapList[y][x][-1])
            if tileType != "0":
                if tileType == "5":
                    entities.append(Boss(x * blockSize, y * blockSize, blockSize, blockSize - 1, 1 if imgInclinaison%2==0 else -1))
                elif tileType == "4":
                    entities.append(FlyEnemy(x * blockSize, y * blockSize, blockSize, blockSize - 1, 1 if imgInclinaison%2==0 else -1))
                elif tileType == "3":
                    entities.append(Enemy(x * blockSize, y * blockSize, blockSize, blockSize - 1, 1 if imgInclinaison%2==0 else -1))
                elif tileType == "2":
                    platforms.append(Goal(x * blockSize, y * blockSize, blockSize, blockSize - 1, assets['GOAL'][0]))
                elif tileType == "1":
                    player = Player(x * blockSize, y * blockSize, blockSize/2, blockSize)
                    entities.append(player)
                else:
                    imgIndex = int(tileType) - 6
                    platforms.append(Block(x * blockSize, y * blockSize, blockSize, blockSize, MAP_SPRITES[imgIndex][imgInclinaison]))
    
    return entities, platforms, player

def loadSpriteSheet(sheetPath, size):
    sheet = loadImage(sheetPath)
    sheet.loadPixels()
    
    all_actualSprites = []
    w, h = int(sheet.width / size), int(sheet.height / size)
    for y in range(h):
        for x in range(w):
            all_actualSprites.append(sheet.get(x*size, y*size, size, size))
    
    return all_actualSprites

def loadMapSheet(sheetPath, size):
    sheet = loadImage(sheetPath)
    sheet.loadPixels()
    
    all_actualSprites = []
    w, h = int(sheet.width / size), int(sheet.height / size)
    for x in range(w):
        piece = []
        for y in range(h):
            piece.append(sheet.get(x*size, y*size, size, size))
        all_actualSprites.append(piece)
    
    return all_actualSprites
