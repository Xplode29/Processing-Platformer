from entity import Entity
from player import Player
from random import *

class Enemy(Entity):
    ANIMATION_DELAY = 5.0
    
    def __init__(self, x, y, w, h, direction):
        super(Enemy, self).__init__(x, y, w, h, direction)
        
        self.maxInvincibilityTime = 40.0
        self.maxPV = 4
        self.PV = self.maxPV
        self.attackDamage = 1
        
        self.hasGravity = True
    
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
                    if int(self.invincibilityTime) % 20 > 10:
                        tint(0, 255)
                        
                image(self.actualSprite, (self.x - offsetX - self.width/2), (self.y - offsetY - self.height/2), self.width*2, self.height*2)
                tint(255, 255)
    
    def loadAssets(self, assets):
        self.assets = assets
        self.SPRITES = self.assets['ENEMY_IDLE_RIGHT']
        self.actualSprite = self.SPRITES[int(self.animState)]
    
    def start(self, platforms, entities):
        """
        Called when the game starts
        """
        super(Enemy, self).start(platforms, entities)
    
    def update(self, player, fps):
        """
        Apply applyMovementment to the cube
        """
        super(Enemy, self).update(player, fps)
        
        if self.canMove:
            self.velocity[0] = self.direction * 4
    
    def update_sprite(self, fps):
        #On Ground
        if self.isGrounded:
            if self.velocity[0] != 0:
                self.SPRITES = self.assets['ENEMY_RUN_RIGHT'] if self.direction == 1 else self.assets['ENEMY_RUN_LEFT']
            else:
                self.SPRITES = self.assets['ENEMY_IDLE_RIGHT'] if self.direction == 1 else self.assets['ENEMY_IDLE_LEFT']
        
        super(Enemy, self).update_sprite(fps)
    
    def collide_left(self, leftObject):
        if self.velocity[0] < 0:
            self.velocity[0] = 0
            self.direction = 1
            self.x = leftObject.x + leftObject.width
        
        if isinstance(leftObject, Player) and self.invincibilityTime > self.maxInvincibilityTime:
            leftObject.take_damage(self.attackDamage, self)
    
    def collide_right(self, rightObject):
        if self.velocity[0] > 0:
            self.velocity[0] = 0
            self.x = rightObject.x - self.width
            self.direction = -1
        
        if isinstance(rightObject, Player) and self.invincibilityTime > self.maxInvincibilityTime:
            rightObject.take_damage(self.attackDamage, self)
    
    def collide_up(self, upperObject):
        if self.velocity[1] < 0:
            self.velocity[1] = 0
            self.y = upperObject.y + upperObject.height
        
        if isinstance(upperObject, Player) and self.invincibilityTime > self.maxInvincibilityTime:
            upperObject.take_damage(self.attackDamage, self)
    
    def collide_down(self, lowerObject):
        if self.velocity[1] > 0:
            self.landed()
            self.velocity[1] = 0
            self.y = lowerObject.y - self.height
        
        if isinstance(lowerObject, Player) and self.invincibilityTime > self.maxInvincibilityTime:
            lowerObject.take_damage(self.attackDamage, self)
            if lowerObject.isGrounded:
                lowerObject.jumpCount = 0
    
    def applyMovement(self, fps):
        super(Enemy, self).applyMovement(fps)
        
        #Test de chute
        self.x += self.width/2 * self.direction #On avance pour tester si on tombe
        lowerBlockNext = self.checkVerticalCollisions(self.velocity[1] + max(60/fps, min(60/fps, float(self.timeInAir * self.GRAVITY))))
        self.x -= self.width/2 * self.direction
        
        if not lowerBlockNext and self.isGrounded:
            #Recule et change de direction
            self.direction *= -1
            self.velocity[0] = -self.velocity[0]
            self.x += self.velocity[0] * 60/fps

class FlyEnemy(Enemy):
    ANIMATION_DELAY = 10.0
    
    def __init__(self, x, y, w, h, direction):
        super(Enemy, self).__init__(x, y, w, h, direction)
        
        self.maxInvincibilityTime = 40.0
        self.maxPV = 4
        self.PV = self.maxPV
        self.attackDamage = 1
        
        self.hasGravity = False
        self.startPoint = (x, y)
        self.maxDistance = self.width * 5
    
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
                    if int(self.invincibilityTime) % 20 > 10:
                        tint(0, 255)
                        
                image(self.actualSprite, (self.x - offsetX), (self.y - offsetY), self.width, self.height)
                tint(255, 255)
    
    def update(self, player, fps):
        """
        Apply applyMovementment to the cube
        """
        super(Enemy, self).update(player, fps)
        
        if self.x > self.startPoint[0] + self.maxDistance:
            self.direction = -1
        if self.x + self.maxDistance < self.startPoint[0]:
            self.direction = 1
        
        if self.canMove:
            self.velocity[0] = self.direction * 4
    
    def update_sprite(self, fps):
        #On Ground
        if self.isGrounded:
            if self.velocity[0] != 0:
                self.SPRITES = self.assets['FLYENEMY_RUN_RIGHT'] if self.direction == 1 else self.assets['FLYENEMY_RUN_LEFT']
            else:
                self.SPRITES = self.assets['FLYENEMY_IDLE_RIGHT'] if self.direction == 1 else self.assets['FLYENEMY_IDLE_LEFT']
        
        super(Enemy, self).update_sprite(fps)
    
    def collide_up(self, upperObject):
        if self.velocity[1] < 0:
            self.velocity[1] = 0
            self.y = upperObject.y + upperObject.height
        
        if isinstance(upperObject, Player):
            upperObject.velocity[1] = -12
            upperObject.jumpCount = 0
    
    
    def take_damage(self, amount, giver):
        if self.invincibilityTime > self.maxInvincibilityTime:
            self.invincibilityTime = 0.0
            self.PV -= amount
            if self.PV <= 0:
                self.die()
    
    def applyMovement(self, fps):
        super(Enemy, self).applyMovement(fps)

class Boss(Enemy):
    ANIMATION_DELAY = 10.0
    
    def __init__(self, x, y, w, h, direction):
        super(Enemy, self).__init__(x, y, w, h, direction)
        
        self.jumpCount = 0.0
        
        self.maxInvincibilityTime = 50.0
        self.maxPV = 10.0
        self.PV = self.maxPV
        self.attackDamage = 1
        
        self.hasGravity = True
        self.startPoint = (x, y)
        self.maxDistance = self.width * 5
        
        self.facingDirection = 0
        
        self.maxThrowCooldown = 40.0
        self.throwCooldown = 0
        
        self.all_proj = []
    
    def loadAssets(self, assets):
        self.assets = assets
        self.SPRITES = self.assets['BOSS_RUN_RIGHT']
        self.actualSprite = self.SPRITES[int(self.animState)]
    
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
                    if int(self.invincibilityTime) % 20 > 10:
                        tint(0, 255)
                        
                image(self.actualSprite, (self.x - offsetX - self.width/2), (self.y - offsetY - self.height), self.width*2, self.height*2)
                
                #HP bar
                fill(0, 0, 0)
                rect(self.x - offsetX - 5, self.y - 20 - offsetY, (self.width + 10), 10)
                
                fill(0, 255, 0)
                rect(self.x - offsetX - 5, self.y - 20 - offsetY, (self.PV / self.maxPV) * (self.width + 10), 10)
                
                tint(255, 255)
        
        for proj in self.all_proj:
            if proj.x + proj.width > offsetX and proj.x < WIDTH + offsetX:
                proj.drawObject(offsetX, offsetY, WIDTH, HEIGHT)
    
    def jump(self):
        if self.canMove:
            if self.jumpCount < 2:
                self.velocity[1] = -self.GRAVITY * 6
                self.jumpCount += 1
                self.timeInAir = 0.0
                self.animState = 0.0
    
    def update(self, player, fps):
        """
        Apply applyMovementment to the cube
        """
        super(Enemy, self).update(player, fps)
        
        if not self.isDead and self.canMove:
            if self.x > self.startPoint[0] + self.maxDistance:
                self.direction = -1
            if self.x + self.maxDistance < self.startPoint[0]:
                self.direction = 1
            
            self.velocity[0] = self.direction * 5
            
            self.facingDirection = -1 if player.x + player.width < self.x else 1
            
            canJump = self.isGrounded
            
            #Choose an action
            action = randint(0, 10)
            
            if action == 0: #Jump
                if canJump:
                    self.jump()
            
            if action == 1: #Attack
                if self.maxThrowCooldown < self.throwCooldown:
                    self.throw()
            
            self.throwCooldown += 60/fps
            
        for proj in self.all_proj:
            proj.update(player, fps)
    
    def update_sprite(self, fps):
        #On Ground
        if self.isGrounded:
            if self.velocity[0] != 0:
                self.SPRITES = self.assets['BOSS_RUN_RIGHT'] if self.facingDirection == 1 else self.assets['BOSS_RUN_LEFT']
            else:
                self.SPRITES = self.assets['BOSS_IDLE_RIGHT'] if self.facingDirection == 1 else self.assets['BOSS_IDLE_LEFT']
        
        super(Enemy, self).update_sprite(fps)
    
    def applyMovement(self, fps):
        super(Enemy, self).applyMovement(fps)
        
        #Test de chute
        self.x += self.width*2 * self.direction #On avance pour tester si on tombe
        lowerBlockNext = self.checkVerticalCollisions(self.velocity[1] + max(60/fps, min(60/fps, float(self.timeInAir * self.GRAVITY))))
        self.x -= self.width*2 * self.direction
        
        if not lowerBlockNext and self.isGrounded:
            #Recule et change de direction
            self.direction *= -1
            self.velocity[0] = -self.velocity[0]
            self.x += self.velocity[0] * 60/fps
    
    def throw(self):
        #Lance un projectile
        self.throwCooldown = 0
        newProj = Projectile(self.x, self.y + self.height/4, self.width, self.height/2, self.facingDirection, 10, self)
        newProj.loadAssets(self.assets)
        newProj.start(self.all_platforms, self.all_entities)
        self.all_proj.append(newProj)
        

class Projectile(Enemy):
    def __init__(self, x, y, w, h, direction, speed, thrower):
        super(Enemy, self).__init__(x, y, w, h, direction)
        self.attackDamage = 1
        
        self.hasGravity = False
        
        self.startPoint = (x, y)
        self.maxDistance = 64 * 20
        self.speed = speed
        
        self.thrower = thrower
    
    def drawObject(self, offsetX, offsetY, WIDTH, HEIGHT):
        """
        Called when the object is drawn on the screen
        """
        if self.x + self.width > offsetX and self.x < WIDTH + offsetX and self.y + self.height > offsetY and self.y < HEIGHT + offsetY:
            if not self.isDead:
                #Hitbox
                #fill(240, 230, 70, 100)
                #rect(self.x - offsetX, self.y - offsetY, self.width, self.height)
                
                image(self.actualSprite, (self.x - offsetX - self.width/4), (self.y - offsetY - 3 * self.height/2), 3*self.width/2, self.height*4)
                tint(255, 255)
    
    def update(self, player, fps):
        """
        Apply applyMovementment to the cube
        """
        super(Enemy, self).update(player, fps)
        
        if not self.isDead:
            if self.x > self.startPoint[0] + self.maxDistance:
                self.isDead = True
            if self.x + self.maxDistance < self.startPoint[0]:
                self.isDead = True
            
            self.velocity[0] = self.direction * self.speed
            
            for obj in self.all_objects:
                if obj != self.thrower:
                    if self.x + self.width > obj.x and self.x < obj.x + obj.width and self.y + self.height > obj.y and self.y < obj.y + obj.height:
                        if isinstance(obj, Player):
                            if not obj.isDashing:
                                obj.take_damage(self.attackDamage, self)
                                self.isDead = True
                        else:
                            self.isDead = True
    
    def loadAssets(self, assets):
        self.assets = assets
        self.SPRITES = self.assets['PROJECTILE_IDLE_RIGHT']
        self.actualSprite = self.SPRITES[int(self.animState)]
    
    def take_damage(self, amount, giver):
        pass #Cant be damaged
    
    def applyMovement(self, fps):
        self.y = self.y + self.velocity[1] * 60/fps
        self.x = self.x + self.velocity[0] * 60/fps
    
    def update_sprite(self, fps):
        self.SPRITES = self.assets['PROJECTILE_IDLE_RIGHT'] if self.direction == -1 else self.assets['PROJECTILE_IDLE_LEFT']
        
        super(Enemy, self).update_sprite(fps)
