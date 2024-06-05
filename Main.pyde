from menus import TutoMenu
from utils import loadSpriteSheet, loadMapSheet

class MainClass:
    #Variables
    WIDTH, HEIGHT = 1280, 720
    FPS = 60.0
    
    def __init__(self):
        """
        Appelle à la creation du jeu
        """
        self.assets = {}
        self.actualScreen = TutoMenu(self.WIDTH, self.HEIGHT, self.FPS) #The screen 
        
    def clearScreen(self):
        """
        Dessine l'arrière-plan
        """
        self.actualScreen.clearScreen()
        
    def drawScreen(self):
        """
        Dessine les objets sur l'ecran
        """
        self.actualScreen.drawScreen()
    
    def loadAssets(self):
        """
        Charge les images et les sons
        """
        self.assets['BACKGROUND_IMAGE'] = loadImage("Others/Menu.png")
        self.assets['LOGO'] = loadImage("Others/Logo.png")
        
        #Player
        self.assets['PLAYER_APEX_SPRITES_LEFT'] = loadSpriteSheet("Player/left/apex.png", 32)
        self.assets['PLAYER_DOUBLEJUMP_SPRITES_LEFT'] = loadSpriteSheet("Player/left/double_jump.png", 32)
        self.assets['PLAYER_FALL_SPRITES_LEFT'] = loadSpriteSheet("Player/left/fall.png", 32)
        self.assets['PLAYER_IDLE_SPRITES_LEFT'] = loadSpriteSheet("Player/left/idle.png", 32)
        self.assets['PLAYER_JUMP_SPRITES_LEFT'] = loadSpriteSheet("Player/left/jump.png", 32)
        self.assets['PLAYER_WALLSLIDE_SPRITES_LEFT'] = loadSpriteSheet("Player/left/wall_slide.png", 32)
        self.assets['PLAYER_DASH_SPRITES_LEFT'] = loadSpriteSheet("Player/left/wall_slide.png", 32)
        self.assets['PLAYER_RUN_SPRITES_LEFT'] = loadSpriteSheet("Player/left/run.png", 64)
        self.assets['PLAYER_ATTACK_SPRITES_LEFT1'] = loadSpriteSheet("Player/left/Character 1 - Attack1_1.png", 64)
        self.assets['PLAYER_ATTACK_SPRITES_LEFT2'] = loadSpriteSheet("Player/left/Character 1 - Attack1_2.png", 64)
        #
        self.assets['PLAYER_APEX_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/apex.png", 32)
        self.assets['PLAYER_DOUBLEJUMP_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/double_jump.png", 32)
        self.assets['PLAYER_FALL_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/fall.png", 32)
        self.assets['PLAYER_IDLE_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/idle.png", 32)
        self.assets['PLAYER_JUMP_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/jump.png", 32)
        self.assets['PLAYER_WALLSLIDE_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/wall_slide.png", 32)
        self.assets['PLAYER_DASH_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/wall_slide.png", 32)
        self.assets['PLAYER_RUN_SPRITES_RIGHT'] = loadSpriteSheet("Player/right/run.png", 64)
        self.assets['PLAYER_ATTACK_SPRITES_RIGHT1'] = loadSpriteSheet("Player/right/Character 1 - Attack1_1.png", 64)
        self.assets['PLAYER_ATTACK_SPRITES_RIGHT2'] = loadSpriteSheet("Player/right/Character 1 - Attack1_2.png", 64)
        
        #Grounded Enemy
        self.assets['ENEMY_IDLE_LEFT'] = loadSpriteSheet("Enemies/walking/left/idle.png", 64)
        self.assets['ENEMY_IDLE_RIGHT'] = loadSpriteSheet("Enemies/walking/right/idle.png", 64)
        self.assets['ENEMY_RUN_LEFT'] = loadSpriteSheet("Enemies/walking/left/run.png", 64)
        self.assets['ENEMY_RUN_RIGHT'] = loadSpriteSheet("Enemies/walking/right/run.png", 64)
        
        #Flying Enemy
        self.assets['FLYENEMY_IDLE_LEFT'] = loadSpriteSheet("Enemies/flying/left/idle.png", 32)
        self.assets['FLYENEMY_IDLE_RIGHT'] = loadSpriteSheet("Enemies/flying/right/idle.png", 32)
        self.assets['FLYENEMY_RUN_LEFT'] = loadSpriteSheet("Enemies/flying/left/run.png", 32)
        self.assets['FLYENEMY_RUN_RIGHT'] = loadSpriteSheet("Enemies/flying/right/run.png", 32)
        
        #Boss
        self.assets['BOSS_IDLE_LEFT'] = loadSpriteSheet("Enemies/boss/left/run.png", 32)
        self.assets['BOSS_IDLE_RIGHT'] = loadSpriteSheet("Enemies/boss/right/run.png", 32)
        self.assets['BOSS_RUN_LEFT'] = loadSpriteSheet("Enemies/boss/left/run.png", 32)
        self.assets['BOSS_RUN_RIGHT'] = loadSpriteSheet("Enemies/boss/right/run.png", 32)
        
        #Projectile
        self.assets['PROJECTILE_IDLE_LEFT'] = loadSpriteSheet("Others/knife/left/idle.png", 32)
        self.assets['PROJECTILE_IDLE_RIGHT'] = loadSpriteSheet("Others/knife/right/idle.png", 32)
        
        self.assets['MAP_SPRITE_SHEET'] = loadMapSheet("TileSets/BlockSheet.png", 16)
        self.assets['GOAL'] = loadSpriteSheet("Others/Goal.png", 64)
        self.assets['HEART'] = loadSpriteSheet("Others/Heart.png", 16)
    
    def onStart(self):
        """
        Appele au debut de la partie
        """
        self.loadAssets()
        
        self.actualScreen.onStart(self.assets)
        
    def onUpdate(self):
        """
        Appele à chaque frame
        """
        self.actualScreen.onUpdate()
        
        if self.actualScreen.newScreen: #Si il y a un nouveau ecran (lors d'un click sur un bouton par exemple)
            self.actualScreen = self.actualScreen.newScreen #change d'ecran
            self.actualScreen.onStart(self.assets) #demarre l'ecran

jeu = MainClass()

def setup():
    """
    Appele lors du lancement du jeu
    """
    global jeu, img
    
    size(jeu.WIDTH, jeu.HEIGHT)
    noStroke() #Pas de contour
    noSmooth() #Pas d'anti-aliasing
    
    frameRate(jeu.FPS) #Calibre les fps à ceux definis
    jeu.onStart() #Demarre la partie
    
def draw():
    """
    Appele à chaque frame
    """
    global jeu, img
    
    jeu.clearScreen() #Dessine l'arriere-plan
    jeu.onUpdate()
    jeu.drawScreen() #Dessine les objets

def keyPressed():
    """
    Appele quand une touche est pressee
    """
    global jeu
    jeu.actualScreen.onKeyPressed(key, keyCode)

def keyReleased():
    """
    Appele quand une touche est relachee
    """
    global jeu
    jeu.actualScreen.onKeyReleased(key, keyCode)

def mouseClicked():
    """
    Appele quand la souris est cliquee
    """
    global jeu
    jeu.actualScreen.onMouseClicked()

def mousePressed():
    """
    Appele quand la souris est pressee
    """
    global jeu
    jeu.actualScreen.onMousePressed()

def mouseReleased():
    """
    Appele quand la souris est relachee
    """
    global jeu
    jeu.actualScreen.onMouseReleased()

def mouseWheel(event):
    """
    Appele quand la molette de la souris est actionne
    """
    global jeu
    jeu.actualScreen.onMouseScroll(event)
