import random
NUM_PER_HAND = 5

class Card:
    def __init__(self, number, suit):
        if number == 11:
            self.number = 'Jack'
        elif number == 12:
            self.number = 'Queen'
        elif number == 13:
            self.number = 'King'
        elif number == 1:
            self.number = 'Ace'
        else:
            self.number = str(number)
        self.suit = suit
    
    def showCard(self):
        print self.number, "of", self.suit
        

class Deck:
    def __init__(self):
        nums = range(1,14)
        suit = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
        self.cards = []
        for num in nums:
            for s in suit:
                self.cards.append(Card(num, s))

    def showDeck(self):
        for card in self.cards:
            card.showCard()

    def shuffleDeck(self):
        random.shuffle(self.cards)
        
    def isEmpty(self):
        if len(self.cards) > 0:
            return False
        else:
            return True

        
class Player():
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.score = 0
    
    def addCard(self, card):
        self.hand.append(card)
    
    def removeCard(self, card):
        self.hand.remove(card)
    
    def showHand(self):
        self.hand = [x for x in self.hand if x is not None]
        for card in self.hand:
            if card is None:
                continue
            card.showCard()

    def ask(self):
        potential = []
        for card in self.hand:
            potential.append(card.number)

        pot = set(potential)
        choice = random.choice(list(pot))
        return choice
    
    def returnCard(self, cardNum):
        returnList = []
        for card in self.hand:
            if cardNum == card.number:
                returnList.append(card)
        
        return returnList
    
    def fourOfAKind(self):
        dct = {}
        num =  0
        for card in self.hand:
            if card.number not in dct.keys():
                dct[card.number] = [card]
            else:
                dct[card.number].append(card)
        
        for key in dct:
            if len(dct[key]) == 4:
                self.score += 1
                num = key
                for c in dct[key]:
                    self.hand.remove(c)
        return num
    
    def returnNums(self):
        nums = []
        for card in self.hand:
            nums.append(card.number)
        return nums
        
class Game():
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffleDeck()
        self.player = Player('Player')
        self.computer = Player('Computer')
    
    def setup(self):
        # Deal cards
        for i in range(0,NUM_PER_HAND):
            self.player.addCard(self.deck.cards[i])
            self.deck.cards.remove(self.deck.cards[i])
        for i in range(NUM_PER_HAND, 2*NUM_PER_HAND):
            self.computer.addCard(self.deck.cards[i])
            self.deck.cards.remove(self.deck.cards[i])

    def play(self):
        closed_cards = []
        
        while len(self.player.hand) > 0 or len(self.computer.hand) > 0:
            
            pscore = str(self.player.score)
            cscore = str(self.computer.score)
            print "Current score: PLAYER -- {0} |  COMPUTER -- {1}".format(pscore, cscore)
            print closed_cards
            
            # Make sure computer has cards:
            if len(self.player.hand) == 0 and not self.deck.isEmpty():
                minNum = min(len(self.deck.cards), 5)
                for i in range(0, minNum):
                    card = self.deck.cards[0]
                    self.player.addCard(card)
                    self.deck.cards.remove(card)
            
            # Player's turn
            print "Your cards now: "
            print self.player.showHand()
            playerNum = raw_input('Pick a card: ')
            returnList = self.computer.returnCard(playerNum)
            
            if len(returnList) == 0:
                print "Go fish, {}!".format(self.player.name)
                if not self.deck.isEmpty():
                    card = self.deck.cards[0]
                    self.player.addCard(card)
                    self.deck.cards.remove(card)
            else:
                print "Shucks, here you go"
                for card in returnList:
                    self.player.addCard(card)
                    self.computer.removeCard(card)
            
            num = self.player.fourOfAKind()
            if num != 0:
                closed_cards.append(num)
                print "You closed out {}!".format(num)
            
            if self.computer.score + self.player.score == 13:
                break


            # Computer's turn
            # Make sure computer has cards:
            if len(self.computer.hand) == 0 and not self.deck.isEmpty():
                minNum = min(len(self.deck.cards), 5)
                for i in range(0, minNum):
                    card = self.deck.cards[0]
                    self.computer.addCard(card)
                    self.deck.cards.remove(card)
                    
            num = self.computer.ask()
            print "Do you have any cards with {}?".format(num)
            returnList = self.player.returnCard(num)
            
            if len(returnList) == 0:
                print "Go fish, {}!".format(self.computer.name)
                if not self.deck.isEmpty():
                    card = self.deck.cards[0]
                    self.computer.addCard(card)
                    self.deck.cards.remove(card)
            else:
                print "Thanks for the cards, sucker!"
                for card in returnList:
                    self.computer.addCard(card)
                    self.player.removeCard(card)
        
            num = self.computer.fourOfAKind()
            if num != 0:
                closed_cards.append(num)
                print "Computer closed out {}!".format(num)


        print "FINAL SCORE: PLAYER -- {0} |  COMPUTER -- {1}".format(str(self.player.score), str(self.computer.score))
        if self.player.score > self.computer.score:
            print "YOU GO PLAYER! GOOD JOB MATE"
        else:
            print "Sorry! Try again next time."
            
    
def main():
    g = Game()
    g.setup()
    g.play()

if __name__ == '__main__':

        