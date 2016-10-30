import os
import sys, pygame
import csv
import space
import random
import time
import player
from tkinter import *
from tkinter import filedialog

class doubleBreak(Exception):
    pass #only way to break out of nested loops...

#this class is based on a framework from my A Level project,
#the original source for which cannot be found and correctly
#attributed. However neither this class nor the case in my
#A level project are verbatim copies of a source and still
#consitute my own work. 
class Window(Frame):    
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.initWindow()

    def initWindow(self):
        self.master.title("Generic Property Game-Opoly")
        self.master.geometry("1920x1020+0+0")
        mainLogo = PhotoImage(file = "./gifLogo.gif")#.grid(row=0, column=0, columnspan=5, sticky=N)
        logoLabel = Label(image=mainLogo)
        logoLabel.image = mainLogo
        logoLabel.grid(row=1, column=1, columnspan=4, sticky=N, padx=555, pady=64)

        hatLogo = PhotoImage(file = "./hat.gif")
        carLogo = PhotoImage(file = "./car.gif")
        bootLogo = PhotoImage(file = "./boot.gif")
        barrowLogo = PhotoImage(file = "./barrow.gif")
        
        #Player 1
        p1Label = Label(self.master, text="Player 1").grid(row=3, column=2, sticky=N)
        p1SpriteLabel = Label(image=hatLogo)
        p1SpriteLabel.image = hatLogo
        p1SpriteLabel.grid(row=4, column=2, sticky=N) 
        self.p1State = StringVar(self.master)
        self.p1State.set("Not Used")
        p1StateMenu = OptionMenu(self.master, self.p1State, "Not Used", "Player", "AI")
        p1StateMenu.grid(row=5, column=2, sticky=N)

        #Player 2
        p2Label = Label(self.master, text="Player 2").grid(row=3, column=3, sticky=N)
        p2SpriteLabel = Label(image=carLogo)
        p2SpriteLabel.image = carLogo
        p2SpriteLabel.grid(row=4, column=3, sticky=N) 
        self.p2State = StringVar(self.master)
        self.p2State.set("Not Used")
        p2StateMenu = OptionMenu(self.master, self.p2State, "Not Used", "Player", "AI")
        p2StateMenu.grid(row=5, column=3, sticky=N)

        #Player 3
        p3Label = Label(self.master, text="Player 3").grid(row=7, column=2, sticky=N)
        p3SpriteLabel = Label(image=bootLogo)
        p3SpriteLabel.image = bootLogo
        p3SpriteLabel.grid(row=8, column=2, sticky=N) 
        self.p3State = StringVar(self.master)
        self.p3State.set("Not Used")
        p3StateMenu = OptionMenu(self.master, self.p3State, "Not Used", "Player", "AI")
        p3StateMenu.grid(row=9, column=2, sticky=N)

        #Player 4
        p4Label = Label(self.master, text="Player 4").grid(row=7, column=3, sticky=N)
        p4SpriteLabel = Label(image=barrowLogo)
        p4SpriteLabel.image = barrowLogo
        p4SpriteLabel.grid(row=8, column=3, sticky=N) 
        self.p4State = StringVar(self.master)
        self.p4State.set("Not Used")
        p4StateMenu = OptionMenu(self.master, self.p4State, "Not Used", "Player", "AI")
        p4StateMenu.grid(row=9, column=3, sticky=N)

        menuProceed = Button(self.master, text="Confirm Choices and proceed to Select Map")
        menuProceed.bind("<Button-1>", self.proceedButton)
        menuProceed.grid(row=10, column=2, columnspan=2, sticky=N)

        ruleLabel = Label(self.master, text="To control the cursor in game, use the arrow keys. Hit enter to select the item").grid(row=12, column=2, columnspan = 2, sticky=N)
        
    def proceedButton(self, master):
        if self.p1State.get() == "Not Used" and self.p2State.get() == "Not Used" and self.p3State.get() == "Not Used" and self.p4State.get() == "Not Used":
            pass
        else:
            self.master.playerSettings = [[self.p1State.get(), "./hat.png"], [self.p2State.get(), "./car.png"], [self.p3State.get(), "./boot.png"], [self.p4State.get(), "./barrow.png"]]
            while self.master.filename == None:
                self.master.filename = filedialog.askopenfilename(initialdir = "./boards/",
                                                           title = "Choose the game location",
                                                           filetypes = (("Board Files","*.csv"),("All Files","*.*")))
                if self.master.filename[-4:] == ".csv":
                    pass
                else:
                    print("File error, Please pick a different one")
                    root.filename = None
            self.master.destroy()
            

def rollDice(surface, colourLookup, player, array):
    global currentPlayer
    for i in range(random.randint(5,10)):
        for die in diceArray:
            die.currentValue = random.randint(1,6)
            die.render(surface, colourLookup)
        pygame.display.flip()
        time.sleep(0.2)
    if diceArray[0].currentValue == diceArray[1].currentValue:
        if player.inJail == True:
            player.inJail== False
            array = endTurn()
            return array
        else:
            player.double = True
            player.doubleCount += 1
            if player.doubleCount >= 3:
                player.inJail = True
                player.posIndex = 10
                array = endTurn()
                return array
    else:
        player.double = False
        player.doubleCount = 0
        if player.inJail == True:
            print("Oh NO!")
            array = endTurn()
            return array
    nextMove = 0
    for die in diceArray:
        nextMove += die.currentValue
    if (player.posIndex+nextMove) >= 40:
        nextMove -= (40-player.posIndex)
        player.posIndex = nextMove
        player.bank += 200
    else:
        player.posIndex += nextMove
    return array

def renderCurrentPlayer(surface, colourLookup, playerNo, balance):
    rect = pygame.Rect(1230, 25, 600, 90)
    rect2 = pygame.Rect(1230, 115, 600, 90)
    rect3 = pygame.Rect(1230, 190, 600, 90)
    try:
        fontType = pygame.font.match_font('Comic Neue Bold', bold = True, italic = False)
    except:
        fontType = pygame.font.get_default_font()
    mainFont = pygame.font.Font(fontType, 65)
    balanceFont = pygame.font.Font(fontType, 40)
    outFont = pygame.font.Font(fontType, 25)
    space.space.drawText(None, surface, ("Ready Player "+str(playerNo)+"?"), colourLookup["BLACK_RGB"], rect, mainFont)
    space.space.drawText(None, surface, ("Your balance is: £"+str(balance)), colourLookup["BLACK_RGB"], rect2, balanceFont)
    if len(bankruptPlayers) > 0:
        if len(bankruptPlayers) > 1:
            text = "Players "
            i = 1
            while i in range(1, len(bankruptPlayers)-1):
                text = text +" & "+ str(bankruptPlayers[i])
            text = text + "are bankrupt"
        else:
            text = "Player "+str(bankruptPlayers[0])+" is bankrupt"
        space.space.drawText(None, surface, text, colourLookup["BLACK_RGB"], rect3, outFont)

def menuMove(array, direction):
    j = 0
    k = 0
    for column in array:
        j = 0
        for i in column:
            if i.marked == None:
                pass
            elif i.marked == True:
                if direction == "UP" and j != 0:
                    i.marked = False
                    array[k][j-1].marked = True
                    break
                elif direction == "DOWN" and j < (len(array[k])-1):
                    i.marked = False
                    array[k][j+1].marked = True
                    break
                elif direction == "LEFT" and k != 0:
                    i.marked = False
                    print(k)
                    print(j)
                    print(array)
                    array[k-1][j].marked = True
                    break
                elif direction == "RIGHT" and k != 3:
                    try:
                        if array[k+1][j].marked == None:
                            i.marked = True
                        else:
                            array[k+1][j].marked = True
                            i.marked = False
                    except:
                        try:
                            i.marked = False
                            array[k+1][len(array[k+1])-1].marked = True
                        except:
                            i.marked = True
                            break
            j += 1
        k += 1

def menuProcess(surface, colourLookup, array, player, board):
    #print("menuProcess ENTER")
    global currentPlayer
    try:
        for column in array:
            for i in column:
                if i.marked == True:
                    if i.text == "Roll Dice":
                        rollDice(surface, colourLookup, player, array)
                        newSpace = boardArray[player.posIndex]
                        if newSpace.spaceType == "PROPERTY" or newSpace.spaceType == "TRAIN" or newSpace.spaceType == "TRAM" or newSpace.spaceType == "BUS"or newSpace.spaceType == "UTILITY":
                            if newSpace.owner == None:
                                array = [[space.menuElement(True, 1, 1, 90, "Buy Space"), space.menuElement(False, 1, 2, 90, "End Turn")],[],[],[]]
                            elif newSpace.owner == player.ID:
                                array = [[space.menuElement(True, 1,1,90, "End Turn")],[],[],[]]
                            elif newSpace.owner != None and newSpace.owner != player.ID:
                                array = [[space.menuElement(True, 1,1,90, "Pay Rent")],[],[],[]]
                            array = cardGraphic(newSpace, array)
                        elif newSpace.spaceType == "TAX":
                            array = [[space.menuElement(True, 1,1, 90, "Pay Tax")],[],[],[]]
                        elif newSpace.spaceType == "GO_TO_JAIL":
                            sendToJail(player)
                            array = endCondition(player)
                            raise doubleBreak
                        elif newSpace.spaceType == "CHANCE":
                            array = chanceGraphic()
                    elif i.text == "Buy Space":
                        buySpace(player)
                        array = endCondition(player)
                        raise doubleBreak
                    elif i.text == "Pay Tax":
                        taxPayment(player)
                        array = endCondition(player)
                        raise doubleBreak
                    elif i.text == "Manage Properties":
                        array = generatePropertyArray(player, board)
                    elif i.text == "Pay Charge" or i.text == "Collect funds":
                        chancePayCollect(player)
                        array = endCondition(player)
                        raise doubleBreak
                    elif i.text == "Pay Fine":
                        jailPayment(player)
                        array = endCondition(player)
                        raise doubleBreak
                    elif i.text == "Back":
                        if player.inJail == True:
                            array = resetMenu(True)
                        else:
                            array = resetMenu()
                    elif i.text == "Upgrade":
                        propertyModify(player, board, "Upgrade", i.space) 
                    elif i.text == "Downgrade":
                        propertyModify(player, board, "Downgrade", i.space)
                    elif i.text == "Morgage":
                        propertyModify(player, board, "Morgage", i.space)
                    elif i.text == "End Turn":
                        array = endCondition(player)
                        raise doubleBreak
                    elif i.space != None:
                        array = generateSpaceMenuArray(i.space)
                        array = cardGraphic(i.space, array)
    except doubleBreak: 
        pass
    #print("menuProcess ESCAPE")
    return array

def endCondition(player):
    if player.double == False or (player.double == True and player.posIndex == 10):
        array = endTurn()
        return array
    else:
        array = resetMenu()
        return array

def taxPayment(player):
    global boardArray
    charge = boardArray[player.posIndex].value
    if affordCheck(player, charge):
        player.bank -= charge
    else:
        player.bankrupt = True 
    
    
def chanceGraphic():
    global chanceArray, chancePointer
    chanceCard = chanceArray[chancePointer]
    array = [[],[],[],[]]
    if chanceCard.fee == True:
        array[0].append(space.menuElement(True, 1,1, 90, "Pay Charge"))
    else:
        array[0].append(space.menuElement(True, 1,1, 90, "Collect funds"))
    array[1].append(chanceCard)
    return array

def chancePayCollect(player):
    global chanceArray, chancePointer
    chanceValue = chanceArray[chancePointer].value
    if chanceArray[chancePointer].value < 0:
        if affordCheck(player, chanceValue):
            player.bank += chanceValue
        else:
            player.bankrupt = True
    else:
        player.bank += chanceValue
    chancePointer += 1
    if chancePointer == len(chanceArray):
        chancePointer = 0
    
def affordCheck(player, fee):
    canAfford = False
    if fee < 0:
        fee = fee * -1
    if player.bank >= fee:
        canAfford = True
    return canAfford


def sendToJail(player):
    player.inJail = True
    player.posIndex = 10
    
def buySpace(player):
    global boardArray, playerArray, currentPlayer
    space = boardArray[player.posIndex]
    if space.value != None:
        if affordCheck(player, space.value) and space.owner == None:
            space.owner = player.ID
            player.bank -= space.value
    else:
        print("This space cannot be bought... Why was it even an option?")

def endTurn():
    global playerArray, currentPlayer, playerArray
    currentPlayer += 1
    if currentPlayer == len(playerArray):
        currentPlayer = 0
    if playerArray[currentPlayer].bankrupt == True:
        currentPlayer += 1
        if currentPlayer == len(playerArray):
            currentPlayer = 0
    if playerArray[currentPlayer].inJail:
        array = resetMenu(True)
    else:
        array = resetMenu()
    return array
    
def resetMenu(inJail = False):
    if inJail == False:
        menuArray = [[space.menuElement(True, 1, 1, 90, "Manage Properties"),
                      space.menuElement(False, 1, 2, 90, "Roll Dice")],[],[],[]]
    else:
        menuArray = [[space.menuElement(True, 1, 1, 90, "Pay Fine"),
                      space.menuElement(False, 1, 2, 90, "Roll Dice")],[],[],[]]
    return menuArray

def cardGraphic(propertySpace, array):
    array[1].append(space.card(propertySpace))
    return array

def propertyModify(player, board, modType, placeObject):
    if modType == "Upgrade":
        if placeObject.upgrades < 5 and player.bank >= placeObject.upgradeCost and placeObject.isMorgaged == False:
            placeObject.upgrades += 1
            player.bank -= placeObject.upgradeCost
        else:
            print("can't afford upgrade")
    elif modType == "Downgrade":
        if placeObject.upgrades > 0:
            placeObject.upgrades -= 1
            player.bank += placeObject.upgradeCost
        else:
            print("No upgrades to remove")
    elif modType == "Morgage":
        if placeObject.isMorgaged == False and placeObject.upgrades == 0:
            placeObject.isMorgaged = True
            player.bank += placeObject.morgage
        elif placeObject.isMorgaged == True and player.bank >= placeObject.morgage:
            player.bank -= placeObject.morgage
            placeObject.isMorgaged = False

def generateSpaceMenuArray(propertySpace):
    array = [[],[],[],[]]    
    array[0].append(space.menuElement(True, 1,1, 90, "Back"))
    allOwned = True
    for i in boardArray:
        if i.colour == propertySpace.colour and (i.owner != propertySpace.owner or i.isMorgaged == True):
            allOwned = False
            break
    if allOwned == True:
        array[0].append(space.menuElement(False, 1,2, 90, "Upgrade", propertySpace))
        array[0].append(space.menuElement(False, 1,3, 90, "Downgrade", propertySpace))
        array[0].append(space.menuElement(False, 1,4, 90, "Morgage", propertySpace))
    else:
        array[0].append(space.menuElement(False, 1,2, 90, "You need a full, not morgaged set to upgrade them"))
        array[0].append(space.menuElement(False, 1,3, 90, "Morgage", propertySpace))
    return array

def generatePropertyArray(player, board):
    array = [[],[],[],[]]    
    array[0].append(space.menuElement(True, 1,1, 90, "Back"))
    addedSpaces = 0
    for i in board:
        if i.owner == player.ID:
            column = 0
            added = False
            while added == False:
                if len(array[column]) < 9:
                    array[column].append(space.menuElement(False, (column+1), (addedSpaces+2), 90, i.name, i))
                    added = True
                else:
                    column += 1
                    addedSpaces = 0
            addedSpaces += 1
    return array

def winChecker():
    currentPlayers = 0
    for i in playerArray:
        if i.bankrupt == False:
            currentPlayers += 1
    if currentPlayers == 1:
        return True
    else:
        return False

def jailPayment(player):
    global freeParking
    if affordCheck(player, 50):
        player.bank -= 50
        player.inJail = False
        freeParking += 50
    else:
        player.bankrupt = True

def AITurn(surface, colourLookup, player, board):
    if player.inJail == True:
        jailPayment(player)
        array = endCondition(player)
    else:
        array = [[space.menuElement(True, 1,1,90, "Roll Dice")]]
        array = menuProcess(surface, colourLookup, array, player, board)
        try:
            for j in array:
                for i in j:
                    print(i)
                    if i.text == "Buy Space":
                        array = [[space.menuElement(True, 1,1,90, "Buy Space")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
                    elif i.text == "Pay Fine":
                        array = [[space.menuElement(True, 1,1,90, "Pay Fine")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
                    elif i.text == "Pay Rent":
                        array = [[space.menuElement(True, 1,1,90, "Pay Rent")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
                    elif i.text == "Pay Tax":
                        array = [[space.menuElement(True, 1,1,90, "Pay Tax")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
                    elif i.text == "Pay Charge":
                        array = [[space.menuElement(True, 1,1,90, "Pay Charge")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
                    elif i.text == "Collect Funds":
                        array = [[space.menuElement(True, 1,1,90, "Collect Funds")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
                    elif i.text == "End Turn":
                        array = [[space.menuElement(True, 1,1,90, "End Turn")]]
                        array = menuProcess(surface, colourLookup, array, player, board)
                        raise doubleBreak
        except doubleBreak: 
            pass
    player.output()
    return array



#----Main---Program----------Main---Program----------Main---Program----------Main---Program----------Main---Program----------Main---Program----------Main---Program------

#Colour codes dictionary
colourDict = {'BLACK': 0x000000,
              'BLACK_RGB': (0,0,0),
              'GREY': 0xCCCCB2,
              'WHITE': 0xFFFFFF,
              'WHITE_RGB': (255,255,255),
              'RED': 0xFF0000,
              'BROWN': 0x803f00,
              'BLUE': 0x00FFFF,
              'PINK': 0xFF66A3,
              'ORANGE': 0xFF6600,
              'YELLOW': 0xFFFF00,
              'GREEN': 0x009900,
              'NAVY': 0x0000CC,
              'GREEN_BACKGROUND': 0xCBF3CB}

#opens a file dialog via tk
root = Tk()
root.iconbitmap(r'./hatLogo.ico')
app = Window(root)
root.filename = None
root.mainloop()

playerArray = []
playerCount = 0

for i in root.playerSettings:
    if i[0] == 'Player':
        playerArray.append(player.player(False, i[1], playerCount))
    elif i[0] == "AI":
        playerArray.append(player.player(True, i[1], playerCount))
    else:
        pass
    playerCount += 1
    
winX = 0
winY = 25
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winX,winY)

pygame.init()
size = width, height = 1920, 1020
screen = pygame.display.set_mode(size)
icon = pygame.image.load("./hatLogo.ico")
pygame.display.set_icon(icon)
pygame.display.set_caption("Generic Property Game-opoly")

#input()
#reads in content from csv
boardArray = []
with open(root.filename, newline='') as boardFile:
    boardReader = csv.reader(boardFile, delimiter=',')
    for i in boardReader:
        #print(i)
        boardArray.append(space.space(i[0], i[1], int(i[3]), int(i[4]), 90, colourDict[i[2]], i))
        #print(boardArray)

chanceArray = []
with open("CHANCE.csv", newline='') as chanceFile:
    chanceReader = csv.reader(chanceFile, delimiter=",")
    for i in chanceReader:
        chanceArray.append(space.chance(i))
        #print(chanceArray)

random.shuffle(chanceArray)

background = pygame.image.load("background2.png")

diceArray = [space.dice(0),space.dice(1)]
mainMenuArray = resetMenu()

freeParking = 0
currentPlayer = 0
chancePointer = 0
bankruptPlayers = []
menuArray = []
for i in mainMenuArray:
    menuArray.append(i[:])


#~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~~~~~Game~Loop~~~~~~~~~
while not winChecker():
    for event in pygame.event.get():    #event handling
        #print(event)
        if event.type == pygame.QUIT:   #quit
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menuMove(menuArray, "UP")
            if event.key == pygame.K_DOWN:
                menuMove(menuArray, "DOWN")
            if event.key == pygame.K_LEFT:
                menuMove(menuArray, "LEFT")
            if event.key == pygame.K_RIGHT:
                menuMove(menuArray, "RIGHT")
            if event.key == pygame.K_RETURN:
                menuArray = menuProcess(screen, colourDict, menuArray, playerArray[currentPlayer], boardArray)

    if playerArray[currentPlayer].AI == True:
        menuArray = AITurn(screen, colourDict, playerArray[currentPlayer], boardArray)
        #menuArray = endTurn()

    screen.fill(colourDict["WHITE"])
    screen.blit(background, (110, 95))
    #all the render calls
    for i in boardArray:
        i.render(screen, colourDict)
    for i in playerArray:
        if i.bankrupt == False:
            screen.blit(i.charSprite, boardArray[i.posIndex].playerCoords[i.ID])
    for die in diceArray:
        die.render(screen, colourDict)
    for i in menuArray:
        for j in i:
            try:
                j.render(screen, colourDict)
            except:
                pass
    renderCurrentPlayer(screen, colourDict, (currentPlayer+1), playerArray[currentPlayer].bank)
    #rollDice(screen, colourDict)
    pygame.display.flip()

for player in playerArray:
    if player.bankrupt == False:
        winner = player
        break
    else:
        pass
try:
    fontType = pygame.font.match_font('Comic Neue Bold', bold = True, italic = False)
except:
    fontType = pygame.font.get_default_font()
bigFont = pygame.font.Font(fontType, 200)
smallFont = pygame.font.Font(fontType, 20)

text = "Player "+str(player.ID+1)+" Wins!"
subtext = "Press any key to quit"
textRect = pygame.Rect(300, 400, 1500, 600)
subtextRect = pygame.Rect(800, 800, 400, 150)

while True:
    for event in pygame.event.get():    #event handling
        #print(event)
        if event.type == pygame.QUIT:   #quit
            pygame.quit()
            
        elif event.type == pygame.KEYDOWN:
            pygame.quit()

    screen.fill(colourDict["WHITE"])
    space.space.drawText(None, screen, text, colourDict["BLACK_RGB"], textRect, bigFont)
    space.space.drawText(None, screen, subtext, colourDict["BLACK_RGB"], subtextRect, smallFont)
    pygame.display.flip()

