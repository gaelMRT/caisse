import pygame
import time


class Checkout:
    def __init__(self,x,y,width,height,maxClient):
        self.isOpen = False
        self._maxClients = maxClient
        self._clients = list()
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._lastTime = time.time()
    
    def queue(self,client):
        if(client not in self._clients):
            client.isInQueue = self
            self._clients.append(client)
            
    def isFull(self):
        return len(self._clients) >= self._maxClients
    def isEmpty(self):
        return len(self._clients) == 0

    #Get the id of a client in list
    def getPlaceInList(self,client):
        for cl in range(self.nbClient()):
            if(id(self._clients[cl]) == id(client)):
                return(cl)
        return -1

    def positionX(self):
        return self._x + self._width/2

    def positionY(self):
        return self._y

    def nbClient(self):
        return len(self._clients)

    def getClientList(self):
        return self._clients

    def dequeue(self):
        return self._clients.pop(0)

    #Make the first client checkout
    def checkouting(self):
        dt = time.time() - self._lastTime
        self._lastTime = time.time()
        
        if(len(self._clients) > 0):
            self._clients[0].tcheckout -= dt
            if(self._clients[0].tcheckout <= 0):
                return self.dequeue()
        return None

    def open(self):
        self.isOpen = True 
    def close(self):
        self.isOpen = False
 
    def draw(self,window):
        color = 0,0,0
        if(self.isOpen):
            color = 0,255,0
        else:
            color = 255,0,0
        rect = self._x,self._y,self._width,self._height
        pygame.draw.rect(window,color , rect)