from checkout import Checkout
from client import Client
import random
import time


#Graphical CONST
SPACE_BETWEEN_CHECKOUTS = 6
CHECKOUT_OFFSET = SPACE_BETWEEN_CHECKOUTS/2.0

#Checkout timer
TIME_BEFORE_OPENING = 30
TIME_BEFORE_CLOSE = 30

#Client entrance
MIN_SECOND_BETWEEN_CLIENTS = 1
MAX_SECOND_BETWEEN_CLIENTS = 60

#Client 
MAX_CLIENT_PER_CHECKOUT = 5
MAX_CLIENT_SPEED = 100
MIN_CLIENT_SPEED = 80
MAX_CLIENT = 200
#Time in store
MIN_TSTORE = 3
MAX_TSTORE = 30
#Relation between store time and checkout time
CHECKOUT_STORE_RELATION = 1

class Store:

    def __init__(self,width=800,height=600,nbCheckouts=10,startClients=20):
        self._size = width,height
        self._clients = []
        self._checkouts = []
        self._lastT = time.time()
        if MAX_SECOND_BETWEEN_CLIENTS <= MIN_SECOND_BETWEEN_CLIENTS:
            self._timeBeforeClient = MIN_SECOND_BETWEEN_CLIENTS
        else:
            self._timeBeforeClient = random.randrange(MIN_SECOND_BETWEEN_CLIENTS,MAX_SECOND_BETWEEN_CLIENTS)

        self._timeBeforeOpening = -1
        self._timeBeforeClosing = -1
        
        for i in range(nbCheckouts):
            self._addCheckout(i,nbCheckouts)
        for j in range(startClients):
            self._addClient()

        self._idLastOpened = -1
        self._openCheck()

    #add a client to store
    def _addClient(self):
        if(len(self._clients) < MAX_CLIENT):
            posX = self._size[0]
            posY = 0
            radius = 20
            tstore = random.randrange(MIN_TSTORE,MAX_TSTORE)
            tcheckout = tstore/CHECKOUT_STORE_RELATION
            destX = random.randint(radius,self._size[0]-radius)
            destY = random.randint(radius,self._size[1]-50-(radius*2)*5)
            speed = ((tstore-MIN_TSTORE)/(MAX_TSTORE-MIN_TSTORE) * (MAX_CLIENT_SPEED-MIN_CLIENT_SPEED) + MIN_CLIENT_SPEED)
            self._clients.append(Client(posX,posY,radius,tstore,tcheckout,destX,destY,speed))

    #add a checkout to store
    def _addCheckout(self,idCheckout,totalCheckout):

        width = (self._size[0]-totalCheckout*SPACE_BETWEEN_CHECKOUTS)/(totalCheckout)
        x = width * idCheckout + idCheckout * SPACE_BETWEEN_CHECKOUTS + CHECKOUT_OFFSET
        y = self._size[1] - 50
        height = 50
        maxClients = MAX_CLIENT_PER_CHECKOUT

        self._checkouts.append(Checkout(x,y,width,height,maxClients))
    
    def _advertiseNeededCheck(self):
        if(self._timeBeforeClosing > 0):
            self._timeBeforeClosing = 0
        elif(self._timeBeforeOpening <= 0):
            self._timeBeforeOpening = TIME_BEFORE_OPENING
    def _advertiseClosing(self):
        if(self._timeBeforeOpening > 0):
            self._timeBeforeOpening = 0
        elif(self._timeBeforeClosing <= 0):
            self._timeBeforeClosing = TIME_BEFORE_CLOSE
            
    
    #Open a checkout
    def _openCheck(self):
        if(self._idLastOpened+1 < len(self._checkouts)):
            self._idLastOpened += 1
            self._lastFreeCheckout = self._checkouts[self._idLastOpened]
            self._lastFreeCheckout.open()

    #Close last checkout
    def _closeCheck(self):
        if(self._idLastOpened-1 >= 0):
            self._checkouts[self._idLastOpened].close()
            self._idLastOpened -= 1
            self._lastFreeCheckout = self._checkouts[self._idLastOpened]

    #move client and open checkout if needed
    def makingMove(self):
        elapsedTime =  time.time() - self._lastT
        self._lastT  = time.time()



        self._timeBeforeClient -= elapsedTime

        
        
        #add client
        if(self._timeBeforeClient <= 0):
            self._addClient()

            if MAX_SECOND_BETWEEN_CLIENTS <= MIN_SECOND_BETWEEN_CLIENTS:
                self._timeBeforeClient = MIN_SECOND_BETWEEN_CLIENTS
            else:
                self._timeBeforeClient = random.randrange(MIN_SECOND_BETWEEN_CLIENTS,MAX_SECOND_BETWEEN_CLIENTS)


        nbWaitingForCheckout = 0

        #clients process
        for client in self._clients:
            #move client
            client.moving(self._lastFreeCheckout)
            #redirect to last free checkout
            if(client.waitingForCheckout is not None and not client.isInQueue):
                nbWaitingForCheckout += 1
                client.goTo(self._lastFreeCheckout)
            #make client go forward in queue
            if(client.isInQueue):
                client.goTo(client.isInQueue)

            needOpening = True
            #Detect the need of opening a new checkout or redirect to a free
            if(self._lastFreeCheckout.isFull()):
                for i in range(self._idLastOpened+1):
                    if(not self._checkouts[i].isFull()):
                        self._lastFreeCheckout = self._checkouts[i]
                        needOpening = False
                        break
                if(needOpening and nbWaitingForCheckout > 0):
                    self._advertiseNeededCheck()

        #clients is checking out
        inQueue = 0
        for check in self._checkouts:
            client = check.checkouting()
            if(client is not None):
                if(client in self._clients):
                    self._clients.remove(client)
            inQueue += check.nbClient()

        #close unneeded checkout
        if(inQueue + nbWaitingForCheckout < (self._idLastOpened-1) * MAX_CLIENT_PER_CHECKOUT):
            self._advertiseClosing()


        #open or close checkout
        if(self._timeBeforeOpening > 0):
            self._timeBeforeOpening -= elapsedTime
            if(not needOpening or nbWaitingForCheckout <= 0):
                self._timeBeforeOpening = 0
            elif(self._timeBeforeOpening <= 0):
                self._openCheck()

        if(self._timeBeforeClosing > 0):
            self._timeBeforeClosing -= elapsedTime
            if(inQueue + nbWaitingForCheckout > self._idLastOpened * MAX_CLIENT_PER_CHECKOUT):
                self._timeBeforeClosing = 0
            elif(self._timeBeforeClosing <= 0):
                self._closeCheck()
        

    #draw all
    def draw(self,window,font):
        if(self._timeBeforeOpening > 0):
            textOpen = font.render("%.2f" % self._timeBeforeOpening,True,(0,255,0))
        else:
            textOpen = font.render("",True,(0,0,0))
        if(self._timeBeforeClosing > 0):
            textClose = font.render("%.2f" % self._timeBeforeClosing,True,(255,0,0))
        else:
            textClose = font.render("",True,(0,0,0))
        
        textOpenRect = textOpen.get_rect()
        textCloseRect = textClose.get_rect()


        textOpenRect.move(2,2)
        textCloseRect.move(2,2)


        #draw
        for check in self._checkouts:
            check.draw(window)
        for client in self._clients:
            client.draw(window)
        window.blit(textOpen,textOpenRect)
        window.blit(textClose,textCloseRect)
        
    