from deck import *
from game_bs import *

class Players:

    def __init__(self, name: str):
        self.name = name
        self.hand = Hand(0, [])
        
    def hit(self, card):
        self.hand.add_card(card)
        return self.hand

    def stay(self):
        return self.hand
    
    def display_cards(self):
        print(f"{self.name}: {str(self.hand)}")
        

class Dealer(Players):
    def __init__(self, stand_value: int):
        super().__init__('Dealer')
        self.stand_value = stand_value
        self.upCard = None

    def set_upCard(self):
        if len(self.hand.cards) > 1:
            self.upCard = self.hand.cards[1]
        
        return self.upCard
    
    def display_cards(self, played: bool):
        if played: 
            super().display_cards()
        else:
            print(f"{self.name}: [X, {str(self.upCard)}] = {str(self.upCard.get_cValue())}")

class Player(Players):
    def __init__(self, name: str, bank: int):
        super().__init__(name)
        self.bet_val = 0
        self.bank = bank

    def bet(self, game):
        while True:
            print(f"{self.name} has ${self.bank} in the bank.")
            bet_value = int(input("How much would you like to bet? "))

        
            if self.bank < bet_value:
                print("Cannot bet more than you have in bank:", self.bank)

            elif bet_value < game.min_bet and bet_value != 0:
                print("Cannot bet less than min bet", game.min_bet)
            
            elif bet_value > game.max_bet:
                print("Cannot exceed max_bet:", game.max_bet)

            else: #bet meets requirements
                break
            
        self.bank -= bet_value
        self.bet_val = bet_value

        if bet_value > 0:
            return True
        else:
            return False

    def play(self, action, shoe: Shoe):
        if action == 'H':
            card = shoe.distribute_card()
            self.hit(card)

        elif action == 'S':
            self.stay()
        
        elif action == 'D':
            card = shoe.distribute_card()
            self.double(card)

        elif action == 'P':
            self.split()
    

    def double(self, card):
        self.bank -= self.bet_val
        self.bet_val *= 2
        self.hit(card)


    def split(self, game):
        #Add copy of player to players in round
        
        player2 = Player(self.name + '2', self.bank) #must make same type as Player
        
        players = game.players_in_round
        this_index = players.index(self)

        players.insert(this_index, player2)    #game.prompt_action() otherwise give it an input of players and run it again
        
        #Match bets:
        player2.bet_val = self.bet_val
        self.bank -= player2.bet_val

        #Split hands:
        self.hand = self.hand[0]
        player2.hand = self.hand[1]


class Bot(Player):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)
    
    def bet(self):
        bet_value = 0
        self.bank -= bet_value
        self.bet_val = bet_value
        return True

class BasicStrategist(Bot):
    def __init__(self, name: str, bank: int):
        pass
        #super().__init__(name, bank)
        

    def determine_bet(self):
        #return bet
        pass
    
        


class Rando(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)

class DImitator(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)

class CardCounter(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)