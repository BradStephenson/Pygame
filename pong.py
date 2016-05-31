import pygame
import math
from pygame.locals import *

pygame.init()

WINDOWWIDTH, WINDOWHEIGHT = (1000, 600)
RED = (255, 0, 0)
RADIUS = 5
YVEL = 3.5
MAXXVEL = 6.0
PADDLESPEED = 3
PADDLEHEIGHT = 6
PADDLEWIDTH = 70
#screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
imbuf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSClock = pygame.time.Clock()

def mLoop():
    sim = Simulation()
    pygame.display.update()
    print ("starting")
    while sim.run():
        pass
    

def distance((x1, y1), (x2, y2)):
    return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))

def unitv(x, y):
    dis = distance((x, y), (0,0))
    return (x/dis, y/dis)

def unitv((x1, y1),(x2, y2)):
    dis = distance((x1, y1),(x2, y2))
    return ((x2-x1)/dis, (y2-y1)/dis)

def scalev((x, y), scaler):
    return ((x*scaler, y*scaler))

def addv((x1, y1), (x2, y2)):
    return ((x1+x2),(y1+y2))


class Simulation:
    def __init__(self):
        self.playerPaddle = Paddle(WINDOWHEIGHT - 20)
        self.AIPaddle = Paddle(20)
        self.ball = Ball()
        self.movingLeft = False
        self.movingRight = False

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    self.movingLeft = True
                if event.key == K_RIGHT:
                    self.movingRight = True
                    
            if event.type == pygame.KEYUP:
                if event.key == K_LEFT:
                    self.movingLeft = False
                if event.key == K_RIGHT:
                    self.movingRight = False
        

        
        FPSClock.tick(60)
        imbuf.fill((0, 0, 0))
        self.ball.move()
        if self.movingLeft: 
            self.playerPaddle.moveLeft()
        if self.movingRight:
            self.playerPaddle.moveRight()

        self.AIPaddle.move(self.ball.getLocInt()[0])
        self.AIPaddle.checkBounce(self.ball)
        self.playerPaddle.checkBounce(self.ball)

        self.playerPaddle.draw(imbuf)
        self.AIPaddle.draw(imbuf)
        self.ball.draw(imbuf)

        
        pygame.display.update()
        return True

class Ball:
    def __init__(self):
        self.loc = (100.0 , 100.0)
        self.xVel = 1.2
        self.down = 1

    def draw(self, surf):
        pygame.draw.circle(surf, RED, self.getLocInt(), RADIUS)

    def getLocInt(self):
        return (int(self.loc[0]), int(self.loc[1]))

    def move(self):
        self.loc = ((self.loc[0] + self.xVel), (self.loc[1] + YVEL * self.down) )

        if self.loc[1] < 0 or self.loc[1] > WINDOWHEIGHT:
            self.loc = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            self.xVel = 1.2

        if self.loc[0] < RADIUS or self.loc[0] > (WINDOWWIDTH - RADIUS):
            self.xVel *= -1
    
    def bounce(self, factor):
        self.down = self.down * -1
        self.xVel = factor*MAXXVEL
        print factor

    


class Paddle:
    def __init__(self, yLoc):
        self.yLoc = yLoc
        self.xLoc = WINDOWWIDTH/2
            
    def checkBounce(self, ball):
        h = ball.getLocInt()
        if h[1] < RADIUS + self.yLoc + PADDLEHEIGHT and h[1] > self.yLoc - RADIUS - PADDLEHEIGHT:
            if h[0] < self.xLoc + PADDLEWIDTH/2 and h[0] > self.xLoc -PADDLEWIDTH/2:
                factor = h[0] - self.xLoc + 0.0
                factor /= PADDLEWIDTH/2
                ball.bounce(factor)

    def moveRight(self):
        if self.xLoc<WINDOWWIDTH -10:
            self.xLoc += PADDLESPEED

    def moveLeft(self):
        if self.xLoc > 10:
            self.xLoc -= PADDLESPEED

    def move(self, ballLoc):
        if ballLoc > self.xLoc + 2:
            self.moveRight()
        if ballLoc < self.xLoc - 2:
            self.moveLeft()

    def getRect(self):
        return ((self.xLoc - PADDLEWIDTH/2, self.yLoc - PADDLEHEIGHT/2), (PADDLEWIDTH, PADDLEHEIGHT))

    def draw(self, surf):
        pygame.draw.rect(surf, RED, self.getRect())

mLoop()
pygame.quit()
