import sys, pygame

class space:
    def __init__(self, typeOfSpace, spaceName, gridX, gridY, spaceSize, spaceColour, initDat):
        '''requires type, name, grid pos, size and colour'''
        self.spaceType = typeOfSpace    #allows different types of space to be rendered 
        self.name = spaceName
        self.positionX = (gridX * spaceSize)+20
        self.positionY = (gridY * spaceSize)+5
        self.size = spaceSize
        self.colour = spaceColour
        self.owner = None
        self.upgrades = 0
        self.isMorgaged = False
        self.transport = False
        #print(initialDataEntry)
        self.value = None
        self.playerCoords = [[self.positionX+5, self.positionY+5],[self.positionX+(self.size/2), self.positionY+5],[self.positionX+5, self.positionY+(self.size/2)],[self.positionX+(self.size/2), self.positionY+(self.size/2)]]
        if self.spaceType == "PROPERTY":
            self.value = int(initDat[5])
            self.rent = int(initDat[6])
            self.rent1House = int(initDat[7])
            self.rent2House = int(initDat[8])
            self.rent3House = int(initDat[9])
            self.rent4House = int(initDat[10])
            self.rentHotel = int(initDat[11])
            self.upgradeCost = int(initDat[12])
            self.morgage = int(initDat[13])
            self.playerCoords = [[self.positionX+5, self.positionY+5],[self.positionX+(self.size/2), self.positionY+5],[self.positionX+5, self.positionY+(self.size/2)],[self.positionX+(self.size/2), self.positionY+(self.size/2)]]
            self.upgradeImage = [pygame.image.load("1house.png"),
                                 pygame.image.load("2houses.png"),
                                 pygame.image.load("3houses.png"),
                                 pygame.image.load("4houses.png"),
                                 pygame.image.load("hotel.png")]
        elif self.spaceType == "TRAIN":
            self.spaceImage = pygame.image.load("train.png")
            self.value = int(initDat[5])
            self.rent = int(initDat[6])
            self.rent1 = int(initDat[7])
            self.rent2 = int(initDat[8])
            self.rent3 = int(initDat[9])
            self.morgage = int(initDat[10])
            self.transport = True
        elif self.spaceType == "TRAM":
            self.spaceImage = pygame.image.load("tram.png")
            self.value = int(initDat[5])
            self.rent = int(initDat[6])
            self.rent1 = int(initDat[7])
            self.rent2 = int(initDat[8])
            self.rent3 = int(initDat[9])
            self.morgage = int(initDat[10])
            self.transport = True
        elif self.spaceType == "BUS":
            self.spaceImage = pygame.image.load("bus.png")
            self.value = int(initDat[5])
            self.rent = int(initDat[6])
            self.rent1 = int(initDat[7])
            self.rent2 = int(initDat[8])
            self.rent3 = int(initDat[9])
            self.morgage = int(initDat[10])
            self.transport = True
        elif self.spaceType == "JAIL":
            self.spaceImage = pygame.image.load("jail.png")
            self.playerCoords = [[self.positionX+(self.size/2), self.positionY],[self.positionX, self.positionY],[self.positionX, self.positionY+(self.size/3)],[self.positionX, self.positionY+((self.size*2)/3)]]
            self.playerCoordsJail = [[self.positionX+(self.size/2), self.positionY+(self.size/2)],[self.positionX+(self.size/2)+15, self.positionY+(self.size/2)],[self.positionX+(self.size/2)+15, self.positionY+(self.size/2)],[self.positionX+(self.size/2)+15, self.positionY+(self.size/2)+15]]
        elif self.spaceType == "GO_TO_JAIL":
            self.spaceImage = pygame.image.load("go_to_jail.png")            
        elif self.spaceType == "CHANCE":
            self.spaceImage = pygame.image.load("chance.png")
        elif self.spaceType == "FREE_PARKING":
            self.spaceImage = pygame.image.load("free_parking.png")
        elif self.spaceType == "UTILITY":
            self.value = int(initDat[5])
            self.morgage = int(initDat[8])
            if "Telecom" in self.name:
                self.spaceImage = pygame.image.load("telecom.png")
                
            elif "Electric" in self.name:
                self.spaceImage = pygame.image.load("power.png")
        elif self.spaceType == "TAX":
            self.value = int(initDat[5])
        try:
            self.fontType = pygame.font.match_font('Comic Neue Bold', bold = True, italic = False)
        except:
            self.fontType = pygame.font.get_default_font()
        self.mainFont = pygame.font.Font(self.fontType, 12)
        self.bigFont = pygame.font.Font(self.fontType, 20)    


    def render(self, surface, colourLookup):    #allows single call for all space types to render
        if self.spaceType == "PROPERTY":
            self.renderProperty(surface, colourLookup)
        elif self.spaceType == "GO":
            self.renderGo(surface, colourLookup)
        elif self.spaceType == "TAX":
            self.renderTax(surface, colourLookup)
        else:
            self.renderImageSpace(surface, colourLookup)

    def renderTax(self, surface, colourLookup):
        pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [self.positionX,self.positionY,self.size,self.size], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)
        self.drawText(surface, self.name, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+5), (self.positionY+5), (self.size-10), (self.size*(3/4))), self.bigFont)
        self.drawText(surface, ("Pay £"+str(self.value)), colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+5), (self.positionY+(5*self.size/6)), (self.size-10), (self.size/4)), self.mainFont)

    def renderImageSpace(self, surface, colourLookup):
        surface.blit(self.spaceImage, (self.positionX, self.positionY))
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)
        if self.transport == True:
            self.drawText(surface, self.name, colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+5), (self.positionY+5), (self.size-10), (self.size/4)), self.mainFont)
            self.drawText(surface, ("£"+str(self.value)), colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+5), (self.positionY+(3*self.size/4)), (self.size-10), (self.size/4)), self.mainFont)
        if self.spaceType == "UTILITY":
            self.drawText(surface, self.name, colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+5), (self.positionY+((2/3)*self.size)), (self.size-10), (self.size/4)), self.mainFont)
            self.drawText(surface, ("£"+str(self.value)), colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+5), (self.positionY+(5*self.size/6)), (self.size-10), (self.size/4)), self.mainFont)
            
    def renderGo(self, surface, colourLookup):  #renders the go square
        posTopRight = self.positionX+self.size
        arrowIndent = 5
        fontSize = 25
        fontSizeSmall = 12
        pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [self.positionX,self.positionY,self.size,self.size], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)
        pygame.draw.polygon(surface, colourLookup["RED"], [((posTopRight-(((self.size/6)+((self.size/10)*2))/2)), (self.positionY+(self.size/9))),       #tip
                                                           ((posTopRight-(self.size/10)), (self.positionY+(3*(self.size/9)))),  #rhtip
                                                           ((posTopRight-((self.size/10)+arrowIndent)), (self.positionY+(3*(self.size/9)))), #rhindend
                                                           ((posTopRight-((self.size/10)+arrowIndent)), (self.positionY+(8*(self.size/9)))), #rhbase
                                                           ((posTopRight-((self.size/6)+(self.size/10)-arrowIndent)), (self.positionY+(8*(self.size/9)))),  #lhbase
                                                           ((posTopRight-((self.size/6)+(self.size/10)-arrowIndent)), (self.positionY+(3*(self.size/9)))),  #lhindent
                                                           ((posTopRight-((self.size/6)+(self.size/10))), (self.positionY+(3*(self.size/9))))], 0)  #lhtip

        pygame.draw.polygon(surface, colourLookup["BLACK"], [((posTopRight-(((self.size/6)+((self.size/10)*2))/2)), (self.positionY+(self.size/9))),       #tip
                                                           ((posTopRight-(self.size/10)), (self.positionY+(3*(self.size/9)))),  #rhtip
                                                           ((posTopRight-((self.size/10)+arrowIndent)), (self.positionY+(3*(self.size/9)))), #rhindend
                                                           ((posTopRight-((self.size/10)+arrowIndent)), (self.positionY+(8*(self.size/9)))), #rhbase
                                                           ((posTopRight-((self.size/6)+(self.size/10)-arrowIndent)), (self.positionY+(8*(self.size/9)))),  #lhbase
                                                           ((posTopRight-((self.size/6)+(self.size/10)-arrowIndent)), (self.positionY+(3*(self.size/9)))),  #lhindent
                                                           ((posTopRight-((self.size/6)+(self.size/10))), (self.positionY+(3*(self.size/9))))], 2)  #lhtip4
        
            
        goFont = pygame.font.Font(self.fontType, fontSize)
        surface.blit(self.mainFont.render("Collect", True, (0,0,0)), (self.positionX+(self.size/8),self.positionY+(self.size/6)))
        surface.blit(self.mainFont.render("£200 as", True, (0,0,0)), (self.positionX+(self.size/8),self.positionY+(self.size/6)+self.mainFont.get_linesize()))
        surface.blit(self.mainFont.render("you pass", True, (0,0,0)), (self.positionX+(self.size/8),self.positionY+(self.size/6)+(2*self.mainFont.get_linesize())))
        surface.blit(goFont.render("GO", True, (255,0,0)), (self.positionX+(self.size/8),self.positionY+((self.size*2)/3)))

    def renderProperty(self, surface, colourLookup):    #renders a property square
        pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [self.positionX,self.positionY,self.size,self.size], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)
        pygame.draw.rect(surface, self.colour, [self.positionX,self.positionY,self.size,(self.size/4)], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,(self.size/4)], 4)
        self.drawText(surface, self.name, colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+10), (self.positionY+(self.size/4)+5), (self.size-20), (self.size/2)), self.mainFont)
        self.drawText(surface, ("£"+str(self.value)), colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+10), (self.positionY+(3*self.size/4)), (self.size-20), (self.size/4)), self.mainFont)
        if self.upgrades > 0:
            surface.blit(self.upgradeImage[self.upgrades-1], (self.positionX, self.positionY))
    
    # The drawText function below is not my own work and is made available http://pygame.org/wiki/TextWrap
    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted
    def drawText(self, surface, text, color, rect, font, aa=True, bkg=None):
        y = rect.top
        lineSpacing = -2
        #print(color)
        # get the height of the font
        fontHeight = font.size("Tg")[1]
     
        while text:
            i = 1
     
            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break
     
            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
     
            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1
     
            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)
     
            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
     
            # remove the text we just blitted
            text = text[i:]
     
        return text

class dice:
    def __init__(self, diceNo):
        self.ID = diceNo
        if diceNo == 0:
            self.positionX = 1030
            self.positionY = 5
        elif diceNo == 1:
            self.positionX = 1130
            self.positionY = 5
        self.size = 90
        self.currentValue = 1
        self.image1 = pygame.image.load("./1.png")
        self.image2 = pygame.image.load("./2.png")
        self.image3 = pygame.image.load("./3.png")
        self.image4 = pygame.image.load("./4.png")
        self.image5 = pygame.image.load("./5.png")
        self.image6 = pygame.image.load("./6.png")

    def render(self, surface, colourLookup):
        if self.currentValue == 1:
            surface.blit(self.image1, (self.positionX, self.positionY))
        elif self.currentValue == 2:
            surface.blit(self.image2, (self.positionX, self.positionY))
        elif self.currentValue == 3:
            surface.blit(self.image3, (self.positionX, self.positionY))
        elif self.currentValue == 4:
            surface.blit(self.image4, (self.positionX, self.positionY))
        elif self.currentValue == 5:
            surface.blit(self.image5, (self.positionX, self.positionY))
        else:
            surface.blit(self.image6, (self.positionX, self.positionY))
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)    
        
class menuElement:
    def __init__(self, isMarked, gridX, gridY, menuSize, menuText, propertySpace = None):
        self.space = propertySpace
        self.marked = isMarked
        self.text = menuText
        self.positionX = 1030 + ((int(gridX)+(int(gridX)-1))*int(menuSize))
        self.positionY = 35 + (int(gridY)*int(menuSize))
        self.size = menuSize
        self.marker = pygame.image.load("./marker.png")
        try:
            self.fontType = pygame.font.match_font('Comic Neue Bold', bold = True, italic = False)
        except:
            self.fontType = pygame.font.get_default_font()
        self.bigFont = pygame.font.Font(self.fontType, 25)
        self.medFont = pygame.font.Font(self.fontType, 12)
        self.smallFont = pygame.font.Font(self.fontType, 8)

    def render(self, surface, colourLookup):
        if self.space == None or self.space.name != self.text:
            pygame.draw.rect(surface, colourLookup["BLACK"], [(self.positionX-self.size),self.positionY,self.size,self.size], 4)
            pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)
            pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [(self.positionX-self.size),self.positionY,self.size,self.size], 0)
            pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [self.positionX,self.positionY,self.size,self.size], 0)
            if self.marked == True:
                surface.blit(self.marker, ((self.positionX-self.size), (self.positionY)))
            returnedText = space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+10), (self.positionY+5), (self.size-20), (self.size-10)), self.bigFont)
            if returnedText != "":
                pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [self.positionX,self.positionY,self.size,self.size], 0)
                returnedText = space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+10), (self.positionY+5), (self.size-20), (self.size-10)), self.medFont)
                if returnedText != "":
                    pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [self.positionX,self.positionY,self.size,self.size], 0)
                    space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+10), (self.positionY+5), (self.size-20), (self.size-10)), self.smallFont)
        else:
            pygame.draw.rect(surface, colourLookup["BLACK"], [(self.positionX-self.size),self.positionY,self.size,self.size], 4)
            pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX,self.positionY,self.size,self.size], 4)
            pygame.draw.rect(surface, colourLookup["GREEN_BACKGROUND"], [(self.positionX-self.size),self.positionY,self.size,self.size], 0)
            pygame.draw.rect(surface, self.space.colour, [self.positionX,self.positionY,self.size,self.size], 0)
            if self.marked == True:
                surface.blit(self.marker, ((self.positionX-self.size), (self.positionY)))
            returnedText = space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+10), (self.positionY+5), (self.size-20), (self.size-10)), self.bigFont)
            if returnedText != "":
                pygame.draw.rect(surface, self.space.colour, [self.positionX,self.positionY,self.size,self.size], 0)
                returnedText = space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+10), (self.positionY+5), (self.size-20), (self.size-10)), self.medFont)
                if returnedText != "":
                    pygame.draw.rect(surface, self.space.colour, [self.positionX,self.positionY,self.size,self.size], 0)
                    space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"],  pygame.Rect((self.positionX+10), (self.positionY+5), (self.size-20), (self.size-10)), self.smallFont)

class card:
    def __init__(self, cardSpace):
        self.positionX = 1300
        self.positionY = 300
        self.width = 400
        self.height = 700
        self.data = cardSpace
        self.marked = None
        try:
            self.fontType = pygame.font.match_font('Comic Neue Bold', bold = True, italic = False)
        except:
            self.fontType = pygame.font.get_default_font()
        self.bigFont = pygame.font.Font(self.fontType, 25)
        self.medFont = pygame.font.Font(self.fontType, 12)
        self.smallFont = pygame.font.Font(self.fontType, 8)
        self.staticText = []
        if self.data.spaceType == "PROPERTY":
            self.staticText.append("Rent - Site Only......... £"+str(self.data.rent))
            self.staticText.append('  "  with 1 house.......... £'+str(self.data.rent1House))
            self.staticText.append('  "  with 2 houses....... £'+str(self.data.rent2House))
            self.staticText.append('  "  with 3 houses....... £'+str(self.data.rent3House))
            self.staticText.append('  "  with 4 houses....... £'+str(self.data.rent4House))
            self.staticText.append('  "  with a Hotel.......... £'+str(self.data.rentHotel))
        elif self.data.spaceType == "UTILITY":
            self.staticText.append("Rent - 4x a dice roll")
            self.staticText.append('  "  with second Utility owned,')
            self.staticText.append("     10x a dice roll")
        else:
            self.staticText.append("Rent - 1 Transport link .. £"+str(self.data.rent))
            self.staticText.append('  "  - 2 Transport links .. £'+str(self.data.rent1))
            self.staticText.append('  "  - 3 Transport links .. £'+str(self.data.rent2))
            self.staticText.append('  "  - 4 Transport links .. £'+str(self.data.rent3))
            
        self.staticTextLower = []    
        if self.data.spaceType == "PROPERTY":
            self.staticTextLower.append('Cost to Upgrade.... £'+str(self.data.upgradeCost))
        self.staticTextLower.append('Morgage Value........ £'+str(self.data.morgage))
            


    def render(self, surface, colourLookup):
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX, self.positionY, self.width, self.height], 4)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX+20, self.positionY+20, self.width-40, self.height/8], 4)
        pygame.draw.rect(surface, self.data.colour, [self.positionX+20, self.positionY+20, self.width-40, self.height/8], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX+20, (self.positionY+520), self.width-40, 5], 0)
        returnedText = space.drawText(self, surface, self.data.name, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+30, self.width-60, (self.height/8)-20), self.bigFont)
        if returnedText != "":
            pygame.draw.rect(surface, self.space.colour, [self.positionX,self.positionY,self.size,self.size], 0)
            returnedText = space.drawText(self, surface, self.data.name, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+30, self.width-60, (self.height/8)-20), self.medFont)
            if returnedText != "":
                pygame.draw.rect(surface, self.space.colour, [self.positionX,self.positionY,self.size,self.size], 0)
                space.drawText(self, surface, self.data.name, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+30, self.width-60, (self.height/8)-20), self.smallFont)
        j = 2
        for i in self.staticText:
            returnedText = space.drawText(self, surface, i, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+(j*70), self.width-60, (self.height/8)-20), self.bigFont)
            if returnedText != "":
                pygame.draw.rect(surface, colourLookup["WHITE_RGB"], [self.positionX,self.positionY,self.size,self.size], 0)
                returnedText = space.drawText(self, surface, i, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+(j*70), self.width-60, (self.height/8)-20), self.medFont)
                if returnedText != "":
                    pygame.draw.rect(surface, colourLookup["WHITE_RGB"], [self.positionX,self.positionY,self.size,self.size], 0)
                    space.drawText(self, surface, i, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+(j*70), self.width-60, (self.height/8)-20), self.smallFont)
            j += 1

        j = 8
        for i in self.staticTextLower:
            returnedText = space.drawText(self, surface, i, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+(j*70), self.width-60, (self.height/8)-20), self.bigFont)
            if returnedText != "":
                pygame.draw.rect(surface, colourLookup["WHITE_RGB"], [self.positionX,self.positionY,self.size,self.size], 0)
                returnedText = space.drawText(self, surface, i, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+(j*70), self.width-60, (self.height/8)-20), self.medFont)
                if returnedText != "":
                    pygame.draw.rect(surface, colourLookup["WHITE_RGB"], [self.positionX,self.positionY,self.size,self.size], 0)
                    space.drawText(self, surface, i, colourLookup["BLACK_RGB"],  pygame.Rect(self.positionX+30, self.positionY+(j*70), self.width-60, (self.height/8)-20), self.smallFont)
            j += 1
        
class chance:
    def __init__(self, chanceData):
        self.positionX = 1300
        self.positionY = 300
        self.width = 400
        self.height = 200
        self.text = chanceData[0]
        self.value = int(chanceData[1])
        if self.value <= 0:
            self.fee = True
            self.dispValue = "Pay £"+str(self.value*-1)
        else:
            self.fee = False
            self.dispValue = "Collect £"+str(self.value)
        self.marked = None

        try:
            self.fontType = pygame.font.match_font('Comic Neue Bold', bold = True, italic = False)
        except:
            self.fontType = pygame.font.get_default_font()
        self.bigFont = pygame.font.Font(self.fontType, 25)
        self.medFont = pygame.font.Font(self.fontType, 25)
        self.smallFont = pygame.font.Font(self.fontType, 8)

    def render(self, surface, colourLookup):
        pygame.draw.rect(surface, colourLookup["RED"], [self.positionX, self.positionY, self.width, self.height], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX, self.positionY, self.width, self.height], 4)
        pygame.draw.rect(surface, colourLookup["WHITE"], [self.positionX+10, self.positionY+10, self.width-20, self.height-20], 0)
        pygame.draw.rect(surface, colourLookup["BLACK"], [self.positionX+10, self.positionY+10, self.width-20, self.height-20], 4)
        space.drawText(self, surface, "CHANCE", colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+(self.width*(2/5))), (self.positionY+20), (self.width/4), (self.height/4)), self.bigFont)
        space.drawText(self, surface, self.text, colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+40), (self.positionY+(self.height/4)), (self.width-100), (self.height*(1/2))), self.medFont)
        space.drawText(self, surface, self.dispValue, colourLookup["BLACK_RGB"], pygame.Rect((self.positionX+(self.width/2)-30), (self.positionY+(self.height*(3/4))), (self.width/2), (self.height/4)), self.medFont)
        
        
        
