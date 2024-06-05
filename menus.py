from objects import Goal, Block
from player import Player
from enemies import Enemy
from utils import loadMap
import levels

class Button:
    """
    Classe definissant un bouton
    """
    def __init__(self, id, x, y, w, h, txt):
        """
        Quand le bouton est cree
        """
        self.id = id
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.firstColor = (175, 175, 175, 150) #Couleur normale
        self.secColor = (200, 200, 200, 175) #Couleur qaund le bouton est survole
        self.text = txt
        self.textSize = 30
        
        self.color = self.firstColor
        self.hovered = False
    
    def drawButton(self):
        """
        Quand le bouton est dessine
        """
        #Dessine le bouton
        fill(self.color[0], self.color[1], self.color[2])
        rect(self.x, self.y, self.width, self.height)
        
        #Dessine le texte
        fill(0, 0, 0)
        rectMode(CENTER)
        textAlign(CENTER)
        textSize(self.textSize)
        text(self.text, self.x + self.width/2, self.y + self.height/2 + 10)
        rectMode(CORNER)
    
    def updateButton(self, mouseX, mouseY):
        self.hovered = self.x < mouseX and mouseX < self.x + self.width and self.y < mouseY and mouseY < self.y + self.height
        self.color = self.secColor if self.hovered else self.firstColor

class Menu(object):
    """
    Classe definissant un ecran
    """
    def __init__(self, WIDTH, HEIGHT, FPS, bg, prevMenu):
        """
        Quand l'ecran est cree
        """
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.FPS = FPS
        
        self.bg = bg #Couleur de l'arriere-plan sous la forme d'un tuple (r, g, b)
        self.all_buttons = [] #Liste de tous les boutons
        self.keys = [False, False, False, False, False] #touches Gauche, Droite, Haut, SHIFT, E ou Q, D, SHIFT, E
        self.newScreen = None #Nouvel ecran (quand un bouton a ete clique)
        
        self.prevMenu = prevMenu #Menu precedent
    
    def drawScreen(self):
        """
        Dessine les objects
        """
        for button in self.all_buttons:
            button.drawButton() #Dessine chaque bouton dans all_buttons
        
    def onStart(self, assets):
        """
        Appele au debut de la partie
        """
        self.assets = assets

    def onUpdate(self):
        """
        Appele a chaque frame
        """
        self.isHovering = False #Detecte si un bouton est survole
        for button in self.all_buttons:
            button.updateButton(mouseX, mouseY)
            if button.hovered: #Si le bouton est survole
                self.isHovering = True
        
        if self.newScreen: #Si il y a un nouvel ecran
            return self.newScreen
    
    def clearScreen(self):
        """
        Dessine l'arriere-plan
        """
        background(self.bg[0], self.bg[1], self.bg[2])
        
    def onKeyPressed(self, key, keyCode):
        """
        Called when a key is pressed
        """
        if key == CODED:
            if keyCode == LEFT: self.keys[0] = True
            if keyCode == RIGHT: self.keys[1] = True

            if keyCode == UP: self.keys[2] = True
            
            if keyCode == SHIFT: self.keys[3] = True
        else:
            if key == 'q': self.keys[0] = True
            if key == 'd': self.keys[1] = True
            
            if key == 'z': self.keys[2] = True
            
            #Attack
            if key == 'e': self.keys[4] = True
        
    def onKeyReleased(self, key, keyCode):
        """
        Called when a key is released
        """
        if key == CODED:
            if keyCode == LEFT: self.keys[0] = False
            if keyCode == RIGHT: self.keys[1] = False
            
            if keyCode == UP: self.keys[2] = False
            
            if keyCode == SHIFT: self.keys[3] = False
        else:
            if key == 'q': self.keys[0] = False
            if key == 'd': self.keys[1] = False
            
            if key == 'z': self.keys[2] = False
            
            #Attack
            if key == 'e': self.keys[4] = False

    def onMouseClicked(self):
        """
        Appele quand la souris est cliquee
        """
        pass #Ne fait rien (modifie en fonction de l'ecran)
    
    def onMousePressed(self):
        """
        Appele quand la souris est pressee
        """
        pass #Ne fait rien (modifie en fonction de l'ecran)
    
    def onMouseReleased(self):
        """
        Appele quand la souris est relachee
        """
        pass #Ne fait rien (modifie en fonction de l'ecran)
    
    def onMouseScroll(self, event):
        """
        Appele quand la molette de la souris est actionne
        """
        pass #Ne fait rien (modifie en fonction de l'ecran)

class MainMenu(Menu):
    """
    Classe du menu principal (herite de la classe Menu)
    """
    def __init__(self, WIDTH, HEIGHT, FPS, actualLevel):
        super(MainMenu, self).__init__(WIDTH, HEIGHT, FPS, (150, 150, 150), None)
        
        #Ajoute les boutons
        self.all_buttons.append(Button(0, self.WIDTH/2 - 100, self.HEIGHT/2 - 30 + 85, 200, 60, "Start"))
        self.all_buttons.append(Button(1, self.WIDTH - 200 - 10, self.HEIGHT - 60 - 10, 200, 60, "Map Builder"))
        self.all_buttons.append(Button(2, 10, self.HEIGHT - 60 - 10, 200, 60, "Levels"))
        
        self.actualLevel = actualLevel #index du level dans all_levels
    
    def onMouseClicked(self):
        for button in self.all_buttons:
            if button.hovered:
                #Regarde l'id du bouton clique pour savoit quoi faire
                if button.id == 0: #Start
                    self.newScreen = Game(self.WIDTH, self.HEIGHT, self.FPS, levels.all_levels[self.actualLevel], self)
                if button.id == 1: #Map Builder
                    self.newScreen = MapBuilder(self.WIDTH, self.HEIGHT, self.FPS, self)
                if button.id == 2: #Levels
                    self.newScreen = LevelMenu(self.WIDTH, self.HEIGHT, self.FPS, self)
        
    def clearScreen(self):
        """
        Dessine l'arriere-plan
        """
        super(MainMenu, self).clearScreen()
        image(self.assets['BACKGROUND_IMAGE'], 0, 0, self.WIDTH, self.HEIGHT)
    
    def drawScreen(self):
        """
        Dessine les elements
        """
        super(MainMenu, self).drawScreen() #Dessine les boutons
        image(self.assets['LOGO'], self.WIDTH/2 - 85, self.HEIGHT/2 - 105, 170, 170)

class Game(Menu):
    #Variables statiques
    SCROLL_WIDTH, SCROLL_HEIGHT = 500, 300 #Limites de l'ecran a partir desquelles il bouge
    BOUNDS_X = (-2560, 2560) #Decalage de la map en X
    BOUNDS_Y = (-569, 569) #Decalage de la map en Y
    PLAYER_VEL = 7 #vitesse du joueur
    PLAYER_DASH = 20 #vitesse du joueur en dash
    
    def __init__(self, WIDTH, HEIGHT, FPS, mapList, prevMenu):
        super(Game, self).__init__(WIDTH, HEIGHT, FPS, (150, 150, 150), prevMenu)
        
        #Boutons
        self.all_buttons.append(Button(0, self.WIDTH - 100 - 10, 10, 100, 30, "Back"))
        
        # Layers
        self.all_platforms = []
        self.all_entities = []
        
        #Decalage de l'ecran
        self.offsetX = 0
        self.offsetY = 0
        
        #Matrice correspondant a la map
        self.mapList = mapList
    
    def onMouseClicked(self):
        """
        Appele quand la souris est cliquee
        """
        if self.player.attackBox.actualAttackCooldown > self.player.attackBox.attackCooldown: #Peut attaquer
            #Donne une impression de combo en changeant d'animation 1/2 coup
            if self.player.attackBox.attackCount < 1:
                self.player.attackBox.attackCount += 1
            else:
                self.player.attackBox.attackCount = 0
            
            #Reset son cooldown
            self.player.attackBox.actualAttackCooldown = 0.0
            self.player.attackBox.animState = 0.0
            self.player.attackBox.isAttacking = True
            
            #Attaque
            self.player.attackBox.attack(self.all_entities)
        
        for button in self.all_buttons:
            if button.hovered:
                if button.id == 0:
                    self.newScreen = self.prevMenu #Retourne sur le menu precedent
        
    def onStart(self, assets):
        """
        Called at the start of the game
        """
        #Transforme la martice avec des nombres en objets
        self.all_entities, self.all_platforms, self.player = loadMap(assets, self.mapList)
        
        #Deplace l'ecran sur le joueur
        self.offsetX = self.player.x - self.WIDTH / 2
        self.offsetY = self.player.y - self.HEIGHT / 2
        
        #Ajuste l'ecran pour qu'il ne depasse pas la map
        if self.offsetX < 0:
            self.offsetX = 0
        if self.offsetX > len(self.mapList[0]) * 64 - self.WIDTH:
            self.offsetX = len(self.mapList[0]) * 64 - self.WIDTH
        if self.offsetY < 0:
            self.offsetY = 0
        if self.offsetY > len(self.mapList) * 64 - self.HEIGHT:
            self.offsetY = len(self.mapList) * 64 - self.HEIGHT
        
        #Platforms
        for platform in self.all_platforms:
            platform.start()
        
        #Entites
        for entity in self.all_entities:
            entity.loadAssets(assets)
            entity.start(self.all_platforms, self.all_entities)
        
        self.prevMenu.newScreen = None #Reset l'ecran precedent
        
        super(Game, self).onStart(assets)
    
    def onUpdate(self):
        """
        Called once per frame
        """
        if self.player.invincibilityTime >= self.player.maxInvincibilityTime: #Si le joueur n'est pas invincible
            self.checkInput() #Recupere les touches et apllique une force au joueur
        
        #Platforms
        for platform in self.all_platforms:
            platform.update(self.FPS)
        
        for entity in self.all_entities:
            if entity.x + entity.velocity[0] < 0: #Evite de le faire sortir de la map
                entity.x = 0
                entity.velocity[0] = 0
                if not isinstance(entity, Player):
                    entity.direction = 1
            
            if entity.x + entity.velocity[0] + entity.width > len(self.mapList[0]) * 64: #Evite de le faire sortir de la map
                entity.x = len(self.mapList[0]) * 64 - entity.width
                entity.velocity[0] = 0
                if not isinstance(entity, Player):
                    entity.direction = -1

            if entity.y + entity.velocity[1] + entity.height > len(self.mapList) * 64: #Si le joueur tombe de la map
                entity.die()
            
            entity.update(self.player, self.FPS)
        
        #Entities
        for shadow in self.player.all_shadows:
            if shadow.isEnabled:
                shadow.update(self.FPS)
        
        #Suis l'abscisse du joueur
        if ((self.player.x + self.player.width - self.offsetX >= self.WIDTH - self.SCROLL_WIDTH) and self.player.velocity[0] > 0) or (
                (self.player.x - self.offsetX <= self.SCROLL_WIDTH) and self.player.velocity[0] < 0):
            self.offsetX += self.player.velocity[0] * 60/self.FPS
            
            #Ajuste l'ecran pour qu'il ne depasse pas la map
            if self.offsetX < 0:
                self.offsetX = 0
            if self.offsetX > len(self.mapList[0]) * 64 - self.WIDTH:
                self.offsetX = len(self.mapList[0]) * 64 - self.WIDTH
        
        #Suis l'ordonnee du joueur
        if ((self.player.y + self.player.height - self.offsetY >= self.HEIGHT - self.SCROLL_HEIGHT) and self.player.velocity[1] > 0) or (
                (self.player.y - self.offsetY <= self.SCROLL_HEIGHT) and self.player.velocity[1] < 0):
            self.offsetY += self.player.velocity[1] * 60/self.FPS
            
            #Ajuste l'ecran pour qu'il ne depasse pas la map
            if self.offsetY < 0:
                self.offsetY = 0
            if self.offsetY > len(self.mapList) * 64 - self.HEIGHT:
                self.offsetY = len(self.mapList) * 64 - self.HEIGHT
        
        for collision in self.player.all_collided_objects:
            if isinstance(collision, Goal): #Si le joueur touche l'arrivee
                if isinstance(self.prevMenu, MainMenu):
                    if self.prevMenu.actualLevel < len(levels.all_levels) - 1:
                        self.prevMenu.actualLevel += 1
                        self.newScreen = Game(self.WIDTH, self.HEIGHT, self.FPS, levels.all_levels[self.prevMenu.actualLevel], self.prevMenu) #Cree le niveau suivant
                    else:
                        #self.prevMenu.actualLevel = 0
                        #self.newScreen = self.prevMenu #Retourne sur l'ecran precedent
                        self.newScreen = WinMenu(self.WIDTH, self.HEIGHT, self.FPS, self.prevMenu) #Affiche l'ecran de victoire
                
                else:
                    self.newScreen = self.prevMenu #Retourne sur l'ecran precedent
        
        if self.player.isDead:
            self.newScreen = Game(self.WIDTH, self.HEIGHT, self.FPS, self.mapList, self.prevMenu) #Reset la partie
            
        super(Game, self).onUpdate()
    
    def drawUI(self):
        """
        Dessine l'UI du jeu
        """
        #Barre du cooldown du dash
        width = (self.player.actualDashingCooldown / self.player.dashingCooldown) * 200
        stroke(0, 0, 0)
        fill(255, 255, 255)
        rect((self.WIDTH - width)/2, self.HEIGHT - 50, width, 20)
        noStroke()
    
    def drawScreen(self):
        """
        Dessine les objets
        """
        #Platforms
        for platform in self.all_platforms:
            platform.drawObject(self.offsetX, self.offsetY, self.WIDTH, self.HEIGHT)
        
        #Ombres (lors du dash)
        for shadow in self.player.all_shadows:
            if shadow.isEnabled:
                shadow.drawObject(self.offsetX, self.offsetY, self.WIDTH, self.HEIGHT)
        
        #Entites
        for entity in self.all_entities:
            entity.drawObject(self.offsetX, self.offsetY, self.WIDTH, self.HEIGHT)
        
        self.drawUI()
        
        super(Game, self).drawScreen()
    
    def checkInput(self):
        """
        Recupere les touches et donne des forces au joueur
        """
        velocity = self.player.velocity
        
        if self.keys[2]: #Jump (Z / UP)
            self.keys[2] = False
            self.player.jump()
        
        if self.keys[3]: #Dash (SHIFT)
            self.keys[3] = False
            self.player.dash()
        
        if self.keys[4]: #Attaque (E)
            self.keys[4] = False
            if self.player.attackBox.actualAttackCooldown > self.player.attackBox.attackCooldown:
                if self.player.attackBox.attackCount < 1:
                    self.player.attackBox.attackCount += 1
                else:
                    self.player.attackBox.attackCount = 0
                self.player.attackBox.actualAttackCooldown = 0.0
                self.player.attackBox.animState = 0.0
                self.player.attackBox.isAttacking = True
                self.player.attackBox.attack(self.all_entities)
        
        if self.player.isDashing: #Fait dash le joueur
            velocity[0] = self.player.direction * self.PLAYER_DASH
        
        elif self.keys[0] and not self.keys[1]: #Deplace a gauche
            self.player.direction = -1
            velocity[0] = self.player.direction * self.PLAYER_VEL
        
        elif self.keys[1] and not self.keys[0]: #Deplace a droite
            self.player.direction = 1
            velocity[0] = self.player.direction * self.PLAYER_VEL
        
        elif self.player.invincibilityTime >= self.player.maxInvincibilityTime: #Si il peut bouger et que rien n'est presse
            velocity[0] = 0
        
        if self.player.canMove: #Donne la velocite au joueur
            self.player.velocity = velocity

class MapBuilder(Menu):
    #Variables statiques
    SCROLL_WIDTH, SCROLL_HEIGHT = 100, 100 #Limites de l'ecran a partir desquelles il bouge
    SCROLL_SPEED = 10 #Vitesse de deplacement de l'ecran
    BLOCK_SIZE = 64 #taille des blocs
    
    BOUNDS_X = (-2560, 2560) #Decalage de la map en X (identique a celle de Game)
    BOUNDS_Y = (-569, 569) #Decalage de la map en Y (identique a celle de Game)
    
    def __init__(self, WIDTH, HEIGHT, FPS, prevMenu):
        super(MapBuilder, self).__init__(WIDTH, HEIGHT, FPS, (150, 150, 150), prevMenu)
        
        #Boutons
        self.all_buttons.append(Button(0, 10, 10, 200, 60, "Back"))
        self.all_buttons.append(Button(1, 10, self.HEIGHT - 60 - 10, 200, 60, "Save"))
        self.all_buttons.append(Button(2, self.WIDTH - 200 - 10, self.HEIGHT - 60 - 10, 200, 60, "Play"))
        
        #Map decompressee
        self.all_object = [[0 for _ in range((self.BOUNDS_X[1] - self.BOUNDS_X[0] + self.WIDTH) // self.BLOCK_SIZE + 1)] for _ in range((self.BOUNDS_Y[1] - self.BOUNDS_Y[0] + self.HEIGHT) // self.BLOCK_SIZE + 1)]
        
        #Map compressee
        self.mapList = [["00" for _ in range((self.BOUNDS_X[1] - self.BOUNDS_X[0] + self.WIDTH) // self.BLOCK_SIZE + 1)] for _ in range((self.BOUNDS_Y[1] - self.BOUNDS_Y[0] + self.HEIGHT) // self.BLOCK_SIZE + 1)]
        
        #Decalage de l'ecran
        self.offsetX = 0
        self.offsetY = 0
        
        self.cursorCoords = [0, 0] #Coordonee de la souris sur la map compressee
        self.isMousePressed = False #souris appuyee
        
    def onStart(self, assets):
        """
        Called at the start of the game
        """
        self.assets = assets
        
        self.actualBlock = 1 #Nombre correspondant au bloc choisi
        self.inclinaison = 0 #Nombre correspondant a l'inclinaison (de 0 a 3)
        
        self.blocks = {}
        self.blocks[1] = [self.assets['PLAYER_IDLE_SPRITES_RIGHT'][0] for _ in range(4)] #Joueur
        self.blocks[2] = [self.assets['GOAL'][0] for _ in range(4)] #But
        self.blocks[3] = [self.assets['ENEMY_RUN_RIGHT'][0] for _ in range(2)] + [self.assets['ENEMY_RUN_LEFT'][0] for _ in range(2)] #Ennemi standard
        self.blocks[4] = [self.assets['FLYENEMY_RUN_RIGHT'][0] for _ in range(2)] + [self.assets['FLYENEMY_RUN_LEFT'][0] for _ in range(2)] #Ennemi volant
        self.blocks[5] = [self.assets['BOSS_IDLE_RIGHT'][0] for _ in range(2)] + [self.assets['BOSS_IDLE_LEFT'][0] for _ in range(2)] #Ennemi qui lance des projectiles
        
        addLen = len(self.blocks) + 1
        for i in range(len(self.assets['MAP_SPRITE_SHEET'])):
            self.blocks[i + addLen] = self.assets['MAP_SPRITE_SHEET'][i] #Autres blocs non speciaux
    
    def onMouseClicked(self):
        for button in self.all_buttons:
            if button.hovered:
                if button.id == 0: #retourne au menu principal
                    self.prevMenu.newScreen = None
                    self.newScreen = self.prevMenu
                
                if button.id == 1: #sauvegarde la map
                    for y in range(len(self.mapList)):
                        for x in range(len(self.mapList[y])):
                            if self.mapList[y][x][0] == "1" and len(self.mapList[y][x][0]) == 2:
                                levels.all_levels_build.append(self.mapList)
                                print(self.mapList)
                                break
                
                if button.id == 2: #teste la map
                    for y in range(len(self.mapList)):
                        for x in range(len(self.mapList[y])):
                            if self.mapList[y][x][0] == "1" and len(self.mapList[y][x][0]) == 2:
                                self.newScreen = Game(self.WIDTH, self.HEIGHT, self.FPS, self.mapList, self)
                                break
        
    def onMouseReleased(self):
        self.isMousePressed = False
        
    def onMousePressed(self):
        self.isMousePressed = True
    
    def onMouseScroll(self, event):
        if event.getCount() > 0: #Si on scroll vers le bas
            if self.inclinaison < 3:
                self.inclinaison += 1
            else:
                self.inclinaison = 0
        elif event.getCount() < 0: #Si on scroll vers le haut
            if self.inclinaison > 0:
                self.inclinaison -= 1
            else:
                self.inclinaison = 3
    
        
    def onKeyPressed(self, key, keyCode):
        """
        Called when a key is pressed
        """
        if key != CODED:
            if key == 'a': #Change de bloc
                if self.actualBlock > 1:
                    self.actualBlock -= 1
                else:
                    self.actualBlock = len(self.blocks)
            if key == 'e': #Change de bloc
                if self.actualBlock < len(self.blocks):
                    self.actualBlock += 1
                else:
                    self.actualBlock = 1
    
    def drawScreen(self):
        #dessine les objets
        for row in self.all_object:
            for object in row:
                if object != 0:
                    object.drawObject(-self.offsetX, -self.offsetY, self.WIDTH, self.HEIGHT)
        
        #Dessine le curseur
        fill(200, 200, 200, 100)
        rect(self.cursorCoords[0] * self.BLOCK_SIZE + self.offsetX + self.BOUNDS_X[0], self.cursorCoords[1] * self.BLOCK_SIZE + self.offsetY + self.BOUNDS_Y[0], self.BLOCK_SIZE, self.BLOCK_SIZE)
        
        image(self.blocks[self.actualBlock][self.inclinaison], self.WIDTH - 64 - 10, 10, 64, 64) #image du block choisi en haut a droite
        
        super(MapBuilder, self).drawScreen()
    
    def onUpdate(self):
        """
        Called once per frame
        """
        #Suis l'abscisse de la souris
        if (mouseX >= self.WIDTH - self.SCROLL_WIDTH) and self.offsetX - (self.SCROLL_SPEED * 60/self.FPS) >= self.BOUNDS_X[0]:
            self.offsetX -= self.SCROLL_SPEED * 60/self.FPS
        if (mouseX <= self.SCROLL_WIDTH) and self.offsetX + (self.SCROLL_SPEED * 60/self.FPS) <= self.BOUNDS_X[1]:
            self.offsetX += self.SCROLL_SPEED * 60/self.FPS
        
        #Suis l'ordonnee de la souris
        if (mouseY >= self.HEIGHT - self.SCROLL_HEIGHT) and self.offsetY - (self.SCROLL_SPEED * 60/self.FPS) >= self.BOUNDS_Y[0]:
            self.offsetY -= self.SCROLL_SPEED * 60/self.FPS
        if (mouseY <= self.SCROLL_HEIGHT) and self.offsetY + (self.SCROLL_SPEED * 60/self.FPS) <= self.BOUNDS_Y[1]:
            self.offsetY += self.SCROLL_SPEED * 60/self.FPS
        
        #Deplace le curseur dans la matrice
        self.cursorCoords[0] = int(mouseX - self.BOUNDS_X[0] - self.offsetX) // self.BLOCK_SIZE
        self.cursorCoords[1] = int(mouseY - self.BOUNDS_Y[0] - self.offsetY) // self.BLOCK_SIZE
        
        if self.isMousePressed:
            if not self.isHovering and 0 < mouseX < self.WIDTH and 0 < mouseY < self.HEIGHT:
                if mouseButton == LEFT:
                    #Place un bloc
                    self.all_object[self.cursorCoords[1]][self.cursorCoords[0]] = (
                        Block(self.cursorCoords[0] * self.BLOCK_SIZE + self.BOUNDS_X[0], self.cursorCoords[1] * self.BLOCK_SIZE + self.BOUNDS_Y[0], self.BLOCK_SIZE, self.BLOCK_SIZE, self.blocks[self.actualBlock][self.inclinaison])
                    )
                    self.mapList[self.cursorCoords[1]][self.cursorCoords[0]] = str(self.actualBlock) + str(self.inclinaison)
                if mouseButton == RIGHT:
                    #Retire un bloc
                    self.all_object[self.cursorCoords[1]][self.cursorCoords[0]] = 0
                    self.mapList[self.cursorCoords[1]][self.cursorCoords[0]] = "00"
        
        super(MapBuilder, self).onUpdate()

class LevelMenu(Menu):
    def __init__(self, WIDTH, HEIGHT, FPS, prevMenu):
        super(LevelMenu, self).__init__(WIDTH, HEIGHT, FPS, (150, 150, 150), prevMenu)
        
        #Boutons
        self.all_buttons.append(Button(0, 10, 10, 200, 60, "Back"))
        self.all_buttons.append(Button(1, self.WIDTH - 200 - 10, self.HEIGHT - 60 - 10, 200, 60, "Custom -->"))
        
        self.buttonSize = 60
        self.sizeBetween = 20
        self.startW = self.WIDTH / 6 + self.sizeBetween
        self.startH = self.HEIGHT / 3
        self.dispoW = self.WIDTH - 2 * self.startW
        self.maxB = int(self.dispoW / (self.buttonSize + self.sizeBetween))
        
        #Dessine les boutons des niveaux
        for i in range(len(levels.all_levels)):
            self.all_buttons.append(Button(i + 2, self.startW + (i % self.maxB) * (self.buttonSize + self.sizeBetween), self.startH + (i // self.maxB) * (self.buttonSize + self.sizeBetween), self.buttonSize, self.buttonSize, str(i + 1)))
        
        self.actualPage = 0 #Page selectionnee
        
    def clearScreen(self):
        """
        Dessine l'arriere-plan
        """
        super(LevelMenu, self).clearScreen()
        image(self.assets['BACKGROUND_IMAGE'], 0, 0, self.WIDTH, self.HEIGHT)
        
    def onStart(self, assets):
        """
        Appele lorsque l'ecran est cree
        """
        self.assets = assets
    
    def onMouseClicked(self):
        for button in self.all_buttons:
            if button.hovered:
                if button.id == 0: #Retourne au menu
                    self.prevMenu.newScreen = None
                    self.newScreen = self.prevMenu
                if button.id == 1: #Change de page
                    #Recree les boutons
                    self.all_buttons = [Button(0, 10, 10, 200, 60, "Back")]
                    
                    if self.actualPage == 0: #Page des niveaux standards
                        self.actualPage = 1
                        self.all_buttons.append(Button(1, 10, self.HEIGHT - 60 - 10, 200, 60, "<-- Levels"))
                        for i in range(len(levels.all_levels_build)):
                            self.all_buttons.append(Button(i + 2, self.startW + (i % self.maxB) * (self.buttonSize + self.sizeBetween), self.startH + (i // self.maxB) * (self.buttonSize + self.sizeBetween), self.buttonSize, self.buttonSize, str(i + 1)))
                    
                    elif self.actualPage == 1: #Page des niveaux custom
                        self.actualPage = 0
                        self.all_buttons.append(Button(1, self.WIDTH - 200 - 10, self.HEIGHT - 60 - 10, 200, 60, "Custom -->"))
                        for i in range(len(levels.all_levels)):
                            self.all_buttons.append(Button(i + 2, self.startW + (i % self.maxB) * (self.buttonSize + self.sizeBetween), self.startH + (i // self.maxB) * (self.buttonSize + self.sizeBetween), self.buttonSize, self.buttonSize, str(i + 1)))
                
                #Si clic sur un niveau
                if self.actualPage == 0: #Page des niveaux standards
                    for i in range(len(levels.all_levels)):
                        if button.id == i + 2:
                            self.newScreen = Game(self.WIDTH, self.HEIGHT, self.FPS, levels.all_levels[i], self)
                
                if self.actualPage == 1: #Page des niveaux custom
                    for i in range(len(levels.all_levels_build)):
                        if button.id == i + 2:
                            self.newScreen = Game(self.WIDTH, self.HEIGHT, self.FPS, levels.all_levels_build[i], self)

class TutoMenu(Menu):
    """
    Menu pour les regles
    """
    def __init__(self, WIDTH, HEIGHT, FPS):
        super(TutoMenu, self).__init__(WIDTH, HEIGHT, FPS, (150, 150, 150), None)
        
        self.all_buttons.append(Button(0, (self.WIDTH - 200)/2, self.HEIGHT - 60 - 10, 200, 60, "OK"))
        
    def clearScreen(self):
        """
        Dessine l'arriere-plan
        """
        super(TutoMenu, self).clearScreen()
        image(self.assets['BACKGROUND_IMAGE'], 0, 0, self.WIDTH, self.HEIGHT)
    
    def onMouseClicked(self):
        for button in self.all_buttons:
            if button.hovered:
                if button.id == 0: #Va au menu principal
                    self.newScreen = MainMenu(self.WIDTH, self.HEIGHT, self.FPS, 0)
    def drawScreen(self):
        """
        Dessine les regles
        """
        textAlign(CENTER)
        textSize(32)
        text("Comment jouer", self.WIDTH / 2, 150)
        
        heightStart = 250
        text("Appuie sur Q/D ou gauche/droite pour se deplacer", self.WIDTH / 2, heightStart)
        text("Appuie sur Z ou haut pour sauter", self.WIDTH / 2, heightStart + 50)
        text("Appuie sur SHIFT pour dash", self.WIDTH / 2, heightStart + 100)
        text("Appuie sur E ou clique gauche pour attacker", self.WIDTH / 2, heightStart + 150)
        text("En Map Builder, appuie sur a/e pour changer de piece\net utilise la molette pour changer l'orientation", self.WIDTH / 2, heightStart + 200)
        
        super(TutoMenu, self).drawScreen()


class WinMenu(Menu):
    """
    Menu pour les regles
    """
    def __init__(self, WIDTH, HEIGHT, FPS, prevMenu):
        super(WinMenu, self).__init__(WIDTH, HEIGHT, FPS, (150, 150, 150), prevMenu)
        
        self.all_buttons.append(Button(0, (self.WIDTH - 200)/2, self.HEIGHT - 60 - 10, 200, 60, "OK"))
        
    def clearScreen(self):
        """
        Dessine l'arriere-plan
        """
        super(WinMenu, self).clearScreen()
        image(self.assets['BACKGROUND_IMAGE'], 0, 0, self.WIDTH, self.HEIGHT)
    
    def onMouseClicked(self):
        for button in self.all_buttons:
            if button.hovered:
                if button.id == 0: #Va au menu principal
                    self.prevMenu.actualLevel = 0
                    self.newScreen = self.prevMenu #Retourne sur l'ecran precedent
    
    def drawScreen(self):
        """
        Dessine les regles
        """
        textAlign(CENTER)
        textSize(32)
        heightStart = self.HEIGHT/2 - 200
        text("Bien joue !", self.WIDTH / 2, heightStart)
        
        heightStart = heightStart + 35
        image(self.assets['LOGO'], self.WIDTH/2 - 85, heightStart, 170, 170)
        heightStart = heightStart + 200
        text("Tu as fini tous les niveaux !", self.WIDTH / 2, heightStart)
        text("N'hesite pas a aller en Map Builder\npour creer de nouveaux niveaux !", self.WIDTH / 2, heightStart + 50)
        
        super(WinMenu, self).drawScreen()
