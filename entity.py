from objects import *

class Entity(object):
    GRAVITY = 4.0
    ANIMATION_DELAY = 5.0
    
    def __init__(self, x, y, w, h, direction):
        self.x, self.y = x, y
        self.width, self.height = w, h
        
        self.direction = direction
        self.velocity = [0, 0]
        
        self.animState = 0.0
        self.timeInAir = 0.0
        self.isGrounded = False
        
        self.invincibilityTime = 0.0
        self.maxInvincibilityTime = 40.0
        self.canMove = False
        
        self.maxPV = 10.0
        self.PV = self.maxPV
        self.isDead = False
        self.attackDamage = 1
        
        self.hasGravity = True
    
    def drawObject(self, offsetX, offsetY, WIDTH, HEIGHT):
        """
        Called when the object is drawn on the screen
        """
        if self.x + self.width > offsetX and self.x < WIDTH + offsetX and self.y + self.height > offsetY and self.y < HEIGHT + offsetY:
            if not self.isDead:
                #Hitbox
                fill(240, 230, 70, 100)
                rect(self.x - offsetX, self.y - offsetY, self.width, self.height)
                
                #Sprite
                image(self.actualSprite, (self.x - offsetX) - self.width/2, (self.y - offsetY), self.width * 2, self.height)
    
    def loadAssets(self, assets):
        self.assets = assets
        self.SPRITES = self.assets['ENEMY_IDLE_RIGHT']
        self.actualSprite = self.SPRITES[int(self.animState)]
    
    def start(self, platforms, entities):
        """
        Called when the game starts
        """
        self.all_platforms = platforms
        self.all_entities = entities
        self.all_objects = platforms + entities
    
    def update(self, player, fps):
        """
        Apply applyMovementment to the cube
        """
        if not self.isDead:
            self.invincibilityTime += 60/fps
            
            self.canMove = self.invincibilityTime >= self.maxInvincibilityTime
            
            if not self.canMove:
                if self.velocity[0] >= 1:
                    self.velocity[0] -= 1
                elif self.velocity[0] <= -1:
                    self.velocity[0] += 1
            
            self.applyMovement(fps)
            
            self.update_sprite(fps)

    def hit_head(self):
        self.velocity[1] *= -1
    
    def landed(self):
        self.timeInAir = 0.0
        self.jumpCount = 0
        self.velocity[1] = 0
        self.isGrounded = True
        self.canJump = True
    
    def jump(self):
        if self.canMove:
            if self.jumpCount < 2:
                self.velocity[1] = -self.GRAVITY * 4
                self.jumpCount += 1
                self.timeInAir = 0.0
                self.animState = 0.0
    
    def update_sprite(self, fps):
        actualSprite_index = int(self.animState // self.ANIMATION_DELAY) % len(self.SPRITES)
        self.actualSprite = self.SPRITES[actualSprite_index]
        self.animState += 60/fps
    
    def take_damage(self, amount, giver):
        if self.invincibilityTime > self.maxInvincibilityTime:
            if self.x - giver.x > 0: self.velocity = [12, -10]
            elif self.x - giver.x < 0: self.velocity = [-12, -10]
            else: self.velocity = [0, -10]
            
            self.invincibilityTime = 0.0
            
            self.PV -= amount
            if self.PV <= 0:
                self.die()
    
    def die(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.velocity = [0, 0]
        self.isDead = True
        self.canMove = False
    
    def collide_left(self, leftObject):
        if self.velocity[0] < 0:
            self.velocity[0] = 0
            self.x = leftObject.x + leftObject.width
    
    def collide_right(self, rightObject):
        if self.velocity[0] > 0:
            self.velocity[0] = 0
            self.x = rightObject.x - self.width
    
    def collide_up(self, upperObject):
        if self.velocity[1] < 0:
            self.hit_head()
            self.velocity[1] = 0
            self.y = upperObject.y + upperObject.height
    
    def collide_down(self, lowerObject):
        if self.velocity[1] > 0:
            self.landed()
            self.velocity[1] = 0
            self.y = lowerObject.y - self.height
    
    def applyMovement(self, fps):
        lowerBlock = self.checkVerticalCollisions(self.velocity[1] * 60/fps + max(60/fps, min(60/fps, float(self.timeInAir * self.GRAVITY))))
        if lowerBlock == None and self.hasGravity:
            self.velocity[1] += max(60/fps, min(60/fps, float(self.timeInAir * self.GRAVITY)))
            self.timeInAir += 60/fps
            self.isGrounded = False
        else:
            self.isGrounded = True
            self.jumpCount = 0
        
        upperObject = self.checkVerticalCollisions(-1 if abs(self.velocity[1] * 60/fps) < 1 else -abs(self.velocity[1] * 60/fps))
        lowerObject = self.checkVerticalCollisions(1 if abs(self.velocity[1] * 60/fps) < 1 else abs(self.velocity[1] * 60/fps))
        
        if upperObject: self.collide_up(upperObject)
        if lowerObject: self.collide_down(lowerObject)
        
        self.y = self.y + self.velocity[1] * 60/fps
        
        leftObject = self.checkHorizontalCollisions(1 if abs(self.velocity[0] * 60/fps) < 1 else -abs(self.velocity[0] * 60/fps))
        rightObject = self.checkHorizontalCollisions(1 if abs(self.velocity[0] * 60/fps) < 1 else abs(self.velocity[0] * 60/fps))
        
        if leftObject: self.collide_left(leftObject)
        if rightObject: self.collide_right(rightObject)
        
        self.x = self.x + self.velocity[0] * 60/fps
        
        self.all_collided_objects = [leftObject, rightObject, upperObject, lowerObject]
        
    def checkVerticalCollisions(self, dy):
        collided_object = None
        
        for obj in self.all_objects:
            if obj != self:
                if dy > 0:
                    if self.x + self.width > obj.x and self.x < obj.x + obj.width and self.y + self.height + dy > obj.y and self.y < obj.y + obj.height:
                        if collided_object == None or (collided_object != None and collided_object.y > obj.y):
                            collided_object = obj
                    
                elif dy < 0:
                    if self.x + self.width > obj.x and self.x < obj.x + obj.width and self.y + self.height > obj.y and self.y + dy < obj.y + obj.height:
                        if collided_object == None or (collided_object != None and collided_object.y < obj.y):
                            collided_object = obj
        
        return collided_object
    
    def checkHorizontalCollisions(self, dx):
        collided_object = None
        
        for obj in self.all_objects:
            if obj != self:
                if dx > 0:
                    if self.x + self.width + dx > obj.x and self.x < obj.x + obj.width and self.y + self.height > obj.y and self.y < obj.y + obj.height:
                        if collided_object == None or (collided_object != None and collided_object.x > obj.x):
                            collided_object = obj
                        
                elif dx < 0:
                    if self.x + self.width > obj.x and self.x + dx < obj.x + obj.width and self.y + self.height > obj.y and self.y < obj.y + obj.height:
                        if collided_object == None or (collided_object != None and collided_object.x < obj.x):
                            collided_object = obj
        
        return collided_object
