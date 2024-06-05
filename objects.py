class Block(object):
    def __init__(self, x, y, w, h, img):
        self.x, self.y = x, y
        self.width, self.height = w, h
        
        self.color = color
        self.img = img
    
    def start(self):
        pass
    
    def drawObject(self, offsetX, offsetY, WIDTH, HEIGHT):
        """
        Called when the object is drawn on the screen
        """
        if self.x + self.width > offsetX and self.x < WIDTH + offsetX and self.y + self.height > offsetY and self.y < HEIGHT + offsetY:
            #fill(self.color[0], self.color[1], self.color[2])
            #rect(self.x - offsetX, self.y - offsetY, self.width, self.height)
            image(self.img, self.x - offsetX, self.y - offsetY, self.width, self.height)
    
    def update(self, fps):
        pass

class Goal(Block):
    def __init__(self, x, y, w, h, img):
        super(Goal, self).__init__(x, y, w, h, img)
    
    def start(self):
        pass
    
    def drawObject(self, offsetX, offsetY, WIDTH, HEIGHT):
        """
        Called when the object is drawn on the screen
        """
        if self.x + self.width > offsetX and self.x < WIDTH + offsetX and self.y + self.height > offsetY and self.y < HEIGHT + offsetY:
            image(self.img, self.x - offsetX - self.width/2, self.y - offsetY - self.height, self.width * 2, self.height * 2)
