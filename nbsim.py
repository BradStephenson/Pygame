import pygame
import math
from pygame.locals import *

pygame.init()

WINDOWWIDTH, WINDOWHEIGHT = (1500, 1000)
#screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
imbuf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSClock = pygame.time.Clock()
G = .0000001

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
        self.buttondown = False
        (self.xdown, self.ydown) = (0, 0)
        self.massDown = 1
        
        self.things = []
        
        self.things.append(Thing((600, 40), (12.7, 0.0)))
        self.things.append(Thing((600, 60), (11.7, 0.0)))
        self.things.append(Thing((850, 550), (1.0, 3.0), 20000))
        self.things.append(Thing((750, 500), (-.4, -1.3), 50000))

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.buttondown:
                if event.type == pygame.MOUSEBUTTONUP:
                    (x, y) = pygame.mouse.get_pos()
                    vec = addv((self.xdown, self.ydown), (-x, -y))
                    self.things.append(Thing((self.xdown, self.ydown), scalev(vec, .1), self.massDown))
                    self.buttondown = False
            if not self.buttondown:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (self.xdown, self.ydown) = pygame.mouse.get_pos()
                    self.buttondown = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    self.massDown = self.massDown/2
                if event.key == K_UP:
                    self.massDown = self.massDown*2
                    

        

        
        FPSClock.tick(60)
        imbuf.fill((0, 0, 0))
        for t in self.things:
            t.gravitate(G, self.things)
        for t in self.things:
            t.move()
        for t in self.things:
            t.draw(imbuf)
        if self.buttondown:
            pygame.draw.circle(imbuf, (155, 155, 155), (self.xdown, self.ydown), int(self.massDown ** (1.0/3.5)))
            pygame.draw.line(imbuf, (155,155,155), pygame.mouse.get_pos(), (self.xdown, self.ydown), 1)
            





            
        pygame.display.update()
        #print("running")
        return True

class Thing:
    def __init__(self, (locx, locy), (velx, vely), mass=1):
        (self.locx, self.locy) = (float(locx), float(locy))
        (self.velx, self.vely) = (float(velx), float(vely))
        self.mass = mass
        self.radius = self.mass ** (1.0/3.5)
        self.collided = False
        
#    def __init__(self, (locx, locy), (velx, vely)):
#        (self.locx, self.locy) = (float(locx), float(locy))
#        (self.velx, self.vely) = (float(velx), float(vely))
#        self.mass = 1

    def gravitate(self, G, things):
        for t in things:
            if t == self:
                continue
            mag = math.sqrt(distance(self.getLoc(), t.getLoc())) * G * t.getMass()
            uv = unitv(self.getLoc(), t.getLoc())
            uv = scalev(uv, mag)
            (self.velx, self.vely) = addv((self.velx, self.vely), uv)
            
        
            

    def move(self):
        self.locx += self.velx
        self.locy += self.vely

    def collide(self, otherThing):
        pass


    def draw(self, imbuf):
        pygame.draw.circle(imbuf, (255, 255, 255), self.getdisplayLoc(), int(self.radius))
        #print("trying to draw at")

    def getLoc(self):
        return (self.locx, self.locy)

    def getdisplayLoc(self):
        return (int(self.locx), int(self.locy))

    def getMass(self):
        return self.mass

mLoop()
pygame.quit()
