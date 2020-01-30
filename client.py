import random
import pygame
import math
import time

class Client:
    def __init__(self,x,y,radius,tstore,tcheckout,destX=0,destY=0,speed = 10):
        self.tstore = tstore
        self._totalTStore = self.tstore
        self.tcheckout = tcheckout
        self._totalTCheckout = self.tcheckout
        self._radius = radius
        self._destX = destX
        self._destY = destY
        self._x = x
        self._y = y
        self.waitingForCheckout = None
        self.isInQueue = None
        self.arrivedToDest = False
        self._speed = speed
        
        self._time = time.time()


    def moving(self,lastOpenCheck):
        dtime = time.time()-self._time
        self._time = time.time()

        if(self.waitingForCheckout is None):
            self.tstore -= dtime
            if(self.tstore <= 0):
                self.goTo(lastOpenCheck)

        diffX = self._destX - self._x
        diffY = self._destY - self._y

        if(math.hypot(diffX,diffY) < self._speed):
            self.arrivedToDest = True
            if(self.waitingForCheckout is not None and not self.waitingForCheckout.isFull() and self.waitingForCheckout.isOpen):
                self.waitingForCheckout.queue(self)
        else:
            angle = math.atan2(diffY,diffX)
            self._x += self._speed  * math.cos(angle)
            self._y += self._speed  * math.sin(angle)

    def goTo(self,checkout):
        if(self.isInQueue is None):
            self.waitingForCheckout = checkout
            self._destX = checkout.positionX()
            self._destY = checkout.positionY() - checkout.nbClient() * (self._radius * 2)
        else:
            id = self.isInQueue.getPlaceInList(self)
            self._destX = self.isInQueue.positionX()
            self._destY = self.isInQueue.positionY() - id * (self._radius * 2)
        
        diffX = self._destX - self._x
        diffY = self._destY - self._y
        self.arrivedToDest = (math.hypot(diffX,diffY) < self._speed)

    def draw(self,window):
        r = 0
        color = (self.waitingForCheckout is not None)*64+ (self.isInQueue is not None) * 64 + ((self._totalTCheckout-self.tcheckout)/self._totalTCheckout)*128
        if(self.tstore > 0):
            r += ((self._totalTStore-self.tstore)/self._totalTStore)*255
            if(r+color > 255):
                r = 255-color
        
        if(color > 255):
            color = 255
        pygame.draw.circle(window, (color+r,color,color), (int(self._x),int(self._y)), self._radius)
        
