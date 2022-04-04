from abc import abstractmethod
import pygame
import time
from random  import randrange
from pygame.locals import*
from time import sleep


class Sprite():
    def __init__(self, x1, y1, w1, h1, im):
        self.x = x1
        self.y = y1
        self.w = w1
        self.h = h1
        self.image = pygame.image.load(im)
        self.vert_velocity = 0    	
    @abstractmethod
    def update(self):
        pass 

    @abstractmethod
    def isBrick(self):
        pass

    @abstractmethod
    def isMario(self):
        pass

    @abstractmethod
    def isCoinBlock(self):
        pass


class Mario(Sprite):
    def __init__(self, x1, y1):
        super(Mario, self).__init__(x1, y1, 60, 95, "mario1.png")
        self.spaceFrame = 0
        self.vert_velocity = 0  
        self.speed = 1
        self.direction = 1
        self.marioScreenLocation = 200
        self.lastX, self.lastY = 0,0
        self.marImageNum = 0

    def update(self):

        self.vert_velocity += 4.6
        self.y += self.vert_velocity
        self.spaceFrame += 1

        if self.y >= 400:
             self.vert_velocity = 0
             self.y = 400
             self.releaseCoin = 0
             self.spaceFrame = 0
		
       

    def isMario(self):
        return True

    def isCoin(self):
        return False

    def lastDest(self):
        self.lastX = self.x
        self.lastY = self.y 

    def updateImage(self):
        self.marImageNum += 1
        if(self.marImageNum > 4):
            self.marImageNum = 0; 


class Brick(Sprite):
    def __init__(self, x1, y1, m):
        super(Brick, self).__init__(x1, y1, 75, 75, "brick.png")
        self.model = m

    def update(self):
        pass 

    def isBrick(self):
        return True
    
    def isCoinBlock(self):
        return False

    def isCoin(self):
        return False

class CoinBlock(Sprite):
    def __init__(self, x1, y1, m):
        super(CoinBlock, self).__init__(x1, y1, 75, 75, "coinblock.png")
        self.model = m
        self.maxCoin = 0

    def update(self):
        pass 

    def isBrick(self):
        return False

    def isCoinBlock(self):
        return True

    def isCoin(self):
        return False

    def releaseCoin(self):
        self.coin = Coin((self.x+self.w/2), self.y, self.model)
        self.model.sprites.append(self.coin)
        self.maxCoin += 1
  

class Coin(Sprite):
    def __init__(self, x1, y1, m):
        super(Coin, self).__init__(x1, y1, 75, 75, "coin.png")
        self.model = m
        self.hor_velocity = randrange(23) - 10
        self.vert_velocity = -15

    def update(self):
        self.vert_velocity += 1
        self.x += self.hor_velocity
        self.y += self.vert_velocity
        
        return True

    def isCoin(self):
        return True

class Model():
    def __init__(self):
        self.mario = Mario(0,0)
        self.sprites = []
        self.sprites.append(self.mario)
        self.brick1 = Brick(200,420, self)
        self.sprites.append(self.brick1)
        self.sprites.append(CoinBlock(100,200, self))
        self.sprites.append(Brick(350,300, self))
        self.sprites.append(Brick(460,330, self))
        self.sprites.append(Brick(600,360, self))
        self.sprites.append(Brick(760,200, self))

    def update(self):
        for sprite in self.sprites:
            sprite.update()
            if(sprite.isBrick() or sprite.isCoinBlock()):
                if(self.marioColliding(self.mario, sprite)):
                    self.stopMario(self.mario, sprite) 
                    

    def marioColliding(self, m, sprite):
        if m.x + m.w <= sprite.x:
            return False
        if m.x >= sprite.x + sprite.w:
            return False 
        if m.y + m.h <= sprite.y:
            return False
        if m.y >= sprite.y + sprite.w:
            return False
        return True

    def stopMario(self, mario, sprite):
        if(mario.x + mario.w >= sprite.x and mario.lastX + mario.w <= sprite.x):
            mario.x = sprite.x - mario.w
        elif(mario.x <= sprite.x + sprite.w and mario.lastX >= sprite.x + sprite.w):
            mario.x = sprite.x + sprite.w
        elif (mario.y + mario.h >= sprite.y and mario.lastY + mario.h <= sprite.y):
            mario.y = sprite.y - mario.h
            self.mario.spaceFrame = 0
            self.mario.vert_velocity = 0
            mario.releaseCoin = 0
        elif (mario.y <= sprite.y + sprite.h and mario.lastY >= (sprite.y + sprite.h)): 
             self.mario.vert_velocity = 0
             mario.y = sprite.y + sprite.h
             if (mario.releaseCoin == 0 and sprite.isCoinBlock()):
                 mario.releaseCoin += 1
                 if sprite.maxCoin < 5:
                     sprite.releaseCoin()
  
class View():
    def __init__(self, model):
        screen_size = (775,575)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.backgroundImage = pygame.image.load("background.png")
        self.brickImage = pygame.image.load("brick.png")
        self.coinImage = pygame.image.load("coin.png")
        self.coinBlockImage = pygame.image.load("coinblock.png")


        self.marioImages = []
        self.marioImages.append (pygame.image.load("mario1.png"))
        self.marioImages.append (pygame.image.load("mario2.png"))
        self.marioImages.append (pygame.image.load("mario3.png"))
        self.marioImages.append (pygame.image.load("mario4.png"))
        self.marioImages.append (pygame.image.load("mario5.png"))

        self.model = model

    def update(self):    
        self.screen.fill([0,200,100])
        for i in range(5):
            self.screen.blit(self.backgroundImage,[(i * 1800) - (self.model.mario.x - self.model.mario.marioScreenLocation)/15, 0])

        for sprite in self.model.sprites:

            if (sprite.isMario()):
                self.screen.blit(self.marioImages[self.model.mario.marImageNum], ((self.model.mario.marioScreenLocation, self.model.mario.y)))
            if (sprite.isBrick()):
                self.screen.blit(self.brickImage,((sprite.x - self.model.mario.x + self.model.mario.marioScreenLocation, sprite.y)))
                
            if (sprite.isCoinBlock()):
                if(sprite.maxCoin < 5):
                    self.screen.blit(self.coinBlockImage,((sprite.x - self.model.mario.x + self.model.mario.marioScreenLocation, sprite.y)))
                else:
                    self.screen.blit(self.brickImage, ((sprite.x - self.model.mario.x + self.model.mario.marioScreenLocation, sprite.y)))
            if (sprite.isCoin()):
                self.screen.blit(self.coinImage,((sprite.x - self.model.mario.x + self.model.mario.marioScreenLocation, sprite.y)))
         

        pygame.display.flip()

class Controller():
    def __init__(self, model):
        self.model = model
        self.keep_going = True

    def update(self):
        self.model.mario.lastDest()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
            
                
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.model.mario.x -= 4
            self.model.mario.updateImage()
        if keys[K_RIGHT]:
            self.model.mario.x += 4
            self.model.mario.updateImage()
        if keys[K_SPACE]:
            if self.model.mario.spaceFrame < 15:
                self.model.mario.vert_velocity -= 7.1

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")