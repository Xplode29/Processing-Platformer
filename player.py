from entity import Entity
from objects import Block, Goal

class Player(Entity):
    GRAVITY = 4.0
    ANIMATION_DELAY = 4.0
    
    def __init__(self, x, y, w, h):
        super(Player, self).__init__(x, y, w, h, 1)
        
        self.jumpCount = 0.0
        self.dashCount = 0.0
        self.isDashing = False
        self.dashingCooldown = 100
        self.actualDashingCooldown = 0.0
        self.all_shadows = []
        
        self.maxInvincibilityTime = 40.0
        self.maxPV = 3
        self.PV = self.maxPV
        
        self.attackDamage = 2
        self.prevDashCount = 0
        
        self.attackBox = AttackBox(self.x, self.y, self.width * 3, self.height, self)
    
    def drawObject(self, offsetX, offsetY, WIDTH, HEIGHT):
        """
        Called when the object is drawn on the screen
        """
        if self.x + self.width > offsetX and self.x < WIDTH + offsetX and self.y + self.height > offsetY and self.y < HEIGHT + offsetY:
            if not self.isDead:
                #Hitbox
                #fill(240, 230, 70, 100)
                #rect(self.x - offsetX, self.y - offsetY, self.width, self.height)
                
                if self.invincibilityTime < self.maxInvincibilityTime:
                    if int(self.invincibilityTime) % (self.maxInvincibilityTime // 2) > (self.maxInvincibilityTime // 4):
                        tint(0, 255)
                        
                if self.SPRITES == self.assets['PLAYER_RUN_SPRITES_LEFT'] or self.SPRITES == self.assets['PLAYER_RUN_SPRITES_RIGHT'] or self.SPRITES == self.assets['PLAYER_ATTACK_SPRITES_LEFT1'] or self.SPRITES == self.assets['PLAYER_ATTACK_SPRITES_RIGHT1'] or self.SPRITES == self.assets['PLAYER_ATTACK_SPRITES_LEFT2'] or self.SPRITES == self.assets['PLAYER_ATTACK_SPRITES_RIGHT2']:
                    image(self.actualSprite, (self.x - offsetX - 3*self.width/2), (self.y - offsetY - self.height/2), self.width*2 * 2, self.height*2)
                else:
                    image(self.actualSprite, (self.x - offsetX) - self.width/2, (self.y - offsetY), self.width * 2, self.height)
                
                for pv in range(self.PV):
                    image(self.assets['HEART'][0], 16 + 32*pv, 16, 32, 32)
                
                tint(255, 255)
                
                self.attackBox.drawObject(offsetX, offsetY)
    
    def loadAssets(self, assets):
        self.assets = assets
        self.SPRITES = self.assets['PLAYER_IDLE_SPRITES_RIGHT']
        self.actualSprite = self.SPRITES[int(self.animState)]
        self.attackBox.loadAssets(assets)
    
    def start(self, platforms, entities):
        """
        Called when the game starts
        """
        super(Player, self).start(platforms, entities)
        
        for _ in range(4):
            self.all_shadows.append(PlayerShadow(self.x, self.y, self.width, self.height, self.actualSprite))
    
    def update(self, player, fps):
        """
        Apply applyMovementment to the cube
        """
        super(Player, self).update(player, fps)
        
        if not self.isDead:
            if self.isDashing:
                self.dashCount += 60/fps
                self.velocity[1] = 0.0
                if self.dashCount > 20.0:
                    self.isDashing = False
                    self.actualDashingCooldown = 0.0
                elif int(self.dashCount) // 5 > self.prevDashCount: #Affiche une image remanente
                    self.prevDashCount = int(self.dashCount) // 5
                    if self.prevDashCount >= len(self.all_shadows):
                        self.prevDashCount = 0 #Reprends la premiere dans la liste de base
                    self.all_shadows[self.prevDashCount].showTo(self.x, self.y, self.actualSprite)
            else:
                if self.actualDashingCooldown < self.dashingCooldown:
                    self.actualDashingCooldown += 60/fps
        
        self.attackBox.update(fps)
    
    def update_sprite(self, fps):
        if self.isDashing:
            self.SPRITES = self.assets['PLAYER_JUMP_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_JUMP_SPRITES_LEFT']
        
        #On Ground
        elif self.isGrounded:
            if self.velocity[0] != 0:
                self.SPRITES = self.assets['PLAYER_RUN_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_RUN_SPRITES_LEFT']
            else:
                self.SPRITES = self.assets['PLAYER_IDLE_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_IDLE_SPRITES_LEFT']
        
        #In Air
        else:
            if -0.5 < self.velocity[1] and self.velocity[1] < 0.5:
                self.SPRITES = self.assets['PLAYER_APEX_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_APEX_SPRITES_LEFT']
            elif self.velocity[1] < 0:
                if self.jumpCount == 1:
                    self.SPRITES = self.assets['PLAYER_JUMP_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_JUMP_SPRITES_LEFT']
                elif self.jumpCount == 2:
                    self.SPRITES = self.assets['PLAYER_DOUBLEJUMP_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_DOUBLEJUMP_SPRITES_LEFT']
            elif 0 < self.velocity[1]:
                self.SPRITES = self.assets['PLAYER_FALL_SPRITES_RIGHT'] if self.direction == 1 else self.assets['PLAYER_FALL_SPRITES_LEFT']
        
        self.attackBox.update_sprite(fps)
        
        super(Player, self).update_sprite(fps)
    
    def dash(self):
        if self.actualDashingCooldown >= self.dashingCooldown and not self.isDashing and self.canMove:
            self.isDashing = True
            self.dashCount = 0.0
            self.animState = 0.0

    def hit_head(self):
        self.jumpCount = 2
        self.velocity[1] *= -1
        self.animState = 0.0
    
    def landed(self):
        self.timeInAir = 0.0
        self.animState = 0.0
        self.jumpCount = 0
        self.velocity[1] = 0
        self.isGrounded = True

class PlayerShadow:
    def __init__(self, x, y, w, h, sprite):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.actualSprite = sprite
        self.isEnabled = False
        self.time = 0.0
        self.maxTime = 15.0
    
    def showTo(self, x, y, sprite):
        self.x, self.y = x, y
        self.isEnabled = True
        self.actualSprite = sprite
        self.time = 0.0
    
    def update(self, fps):
        if self.time < self.maxTime:
            self.opacity = (1 - self.time/self.maxTime) * 255
            self.time += 60/fps
        else:
            self.time = 0.0
            self.isEnabled = False
    
    def drawObject(self, offsetX, offsetY, WIDTH, HEIGHT):
        """
        Called when the object is drawn on the screen
        """
        tint(0, self.opacity) # decrease the opacity
        image(self.actualSprite, (self.x - offsetX) - self.width/2, (self.y - offsetY), self.width * 2, self.height)
        tint(255, 255)

class AttackBox(object):
    ANIMATION_DELAY = 5.0
    
    def __init__(self, x, y, w, h, player):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        
        self.attackCount = 0
        self.attackCooldown = 10.0
        self.actualAttackCooldown = 0.0
        self.isAttacking = False
        
        self.player = player
        self.animState = 0.0
    
    def loadAssets(self, assets):
        self.assets = assets
        self.SPRITES = self.assets['PLAYER_ATTACK_SPRITES_RIGHT1']
        self.actualSprite = self.SPRITES[int(self.animState)]
        
        self.attackCooldown = (len(self.SPRITES) - 1) * self.ANIMATION_DELAY
    
    def update(self, fps):
        if self.player.direction == -1:
            self.x = self.player.x - self.width
            self.y = self.player.y + (self.player.height - self.height) / 2
        
        elif self.player.direction == 1:
            self.x = self.player.x + self.player.width
            self.y = self.player.y + (self.player.height - self.height) / 2
        
        #if not self.isAttacking:
        self.actualAttackCooldown += 60/fps
    
    def drawObject(self, offsetX, offsetY):
        #fill(255, 0, 0, 100)
        #rect(self.x - offsetX, self.y - offsetY, self.width, self.height)
        imgW = self.width/4
        imgH = self.height
        if self.player.direction == -1:
            image(self.actualSprite, (self.x - offsetX + self.player.width), (self.y - offsetY - imgH/2), imgW * 4, imgH * 2)
        
        elif self.player.direction == 1:
            image(self.actualSprite, (self.x - offsetX - self.player.width), (self.y - offsetY - imgH/2), imgW * 4, imgH * 2)
        pass
    
    def attack(self, all_entities):
        for entity in all_entities:
            if self.x + self.width > entity.x and self.x < entity.x + entity.width and self.y + self.height > entity.y and self.y < entity.y + entity.height:
                if isinstance(entity, Entity):
                    entity.take_damage(self.player.attackDamage, self.player)
    
    
    def update_sprite(self, fps):
        if self.attackCount == 0:
            self.SPRITES = self.assets['PLAYER_ATTACK_SPRITES_RIGHT1'] if self.player.direction == 1 else self.assets['PLAYER_ATTACK_SPRITES_LEFT1']
        else:
            self.SPRITES = self.assets['PLAYER_ATTACK_SPRITES_RIGHT2'] if self.player.direction == 1 else self.assets['PLAYER_ATTACK_SPRITES_LEFT2']
        
        actualSprite_index = int(int(self.animState) // self.ANIMATION_DELAY) % len(self.SPRITES)
        self.actualSprite = self.SPRITES[actualSprite_index]
        if self.isAttacking:
            self.animState += 60/fps
        else:
            self.animState = 0.0

        if actualSprite_index == len(self.assets['PLAYER_ATTACK_SPRITES_RIGHT1']) - 1 or actualSprite_index == len(self.assets['PLAYER_ATTACK_SPRITES_LEFT1']) - 1 or actualSprite_index == len(self.assets['PLAYER_ATTACK_SPRITES_RIGHT2']) - 1 or actualSprite_index == len(self.assets['PLAYER_ATTACK_SPRITES_LEFT2']) - 1:
            self.isAttacking = False
