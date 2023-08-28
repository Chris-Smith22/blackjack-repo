from random import *

SUITS = ['S', 'C', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.validity()
        self.value = self.get_cValue()
     
    
    def __str__(self):
        return str(self.suit) + str(self.rank)
    
    def get_cValue(self):
        value = 11 #card is an Ace or invalid card
        try:
            value = int(self.rank)

        except ValueError:
            if self.rank == 'J' or self.rank == 'Q' or self.rank == 'K':
                value = 10

        finally:
            return value

    def validity(self):
        if (self.suit not in SUITS) or (self.rank not in RANKS):
            print("Invalid card. Check rank and/or suit.")
            raise InvalidCard


    def __eq__(self, other_card) -> bool:
        return self.rank == other_card.rank
        
        


class InvalidCard(Exception):
    pass


class Hand:
    
    #Create hand (most likely to 0 cards, before adding)
    def __init__(self, num_of_cards, cards: list):
        self.num_of_cards = num_of_cards
        self.cards = cards
        self.split = False


    #Add card to hand
    def add_card(self, card):
        self.cards.append(card)
        self.num_of_cards += 1

    def remove_card(self, index):
        self.cards.remove(index)
        self.num_of_cards -= 1

    #Get value of hand:
    def get_hValue(self) -> tuple:
        total1 = 0
        total2 = 0
        for card in self.cards:
            if card.value == 11: #card is an ace
                total1 += 1
                total2 += 11
            else:
                total1 += card.value
                total2 += card.value
        
        return (total1, total2)
    
    def __str__(self):
        
        #Hand:
        cards_str = '['
        for card in self.cards:
            cards_str += str(card)
            if card != self.cards[len(self.cards) -1]:
                cards_str += ', '
            else:
                cards_str += ']'

        #Hand Value:
        val_str = ''
        totals = self.get_hValue()

            #No ace in hand, or ace = 1 because total2>21:
        if totals[1] == totals[0] or totals[1] > 21:
            val_str += str(totals[0])

        else: 
            val_str += str(totals[1]) + '/' + str(totals[0])
        
        

        return (cards_str + ' = ' + val_str)
    
    def has_ace(self):
        return '/' in self.__str__()
        
     
class Deck:

    def __init__(self):
        self.cards = self.generate_deck()
        self.num_of_cards = 52
    

    def generate_deck(self):
        cards = []

        #iterate through suit and rank
        for s in range(0,4):
            for r in range(0,13):
                card = Card(SUITS[s], RANKS[r])
                cards.append(card)
        
        shuffle(cards)
        return cards
    
    

class Shoe:

    def __init__(self, num_of_decks):
        self.num_of_decks = num_of_decks
        self.decks = self.generate_shoe()
        
    
    def generate_shoe(self):
        shoe = []
        for i in range(self.num_of_decks):
            deck = Deck()
            shoe.append(deck)

        shuffle(shoe)
        return shoe
    

    def distribute_card(self):
        #Returns first card in shoe, if exists

        #Check num of decks != 0:
        if (self.num_of_decks == 0):
            print("Empty shoe.")
            return
        
        #Check length of deck:
        for deck in self.decks:
            if len(deck.cards) == 0:
                self.decks.remove(deck)
                self.num_of_decks -= 1

        #New Card:
        card = self.decks[0].cards.pop(0)
        self.decks[0].num_of_cards -= 1
        
        return card



def display_deck():
    '''
    for suit in SUITS:
        for rank in RANKS:
            card = Card(suit, rank)
            print(card, card.value)
            '''
    
    deck = Deck()
    for card in deck.cards:
        print(card)

#display_deck()

def display_shoe():
    shoe = Shoe(1)

    for deck in shoe.decks:
        for card in deck:
            print(card)

#display_shoe()

'''
def display_hand():
    deck = Deck()
    hand = Hand(2, [deck.cards[0], deck.cards[1]])
    print(hand)
    hand.add_card(deck.cards[2])
    print(hand)

#display_hand()
'''