import sys, pygame

class player:
    def __init__(self, AIPlayer, charImage, playerID):
        self.ID = playerID
        self.AI = AIPlayer
        self.bankrupt = False
        self.bank = 1500
        self.posIndex = 0
        self.inJail = False
        self.charSprite = pygame.image.load(charImage)
        self.property = []
        self.double = False
        self.doubleCount = 0

    def output(self):
        print(self.ID)
        print(self.bank)
        print(self.posIndex)
        print(self.property)
        print(self.double)
        print(self.doubleCount)
