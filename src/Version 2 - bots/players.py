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

    def split(self, game: Game, player2):
        #Add copy of player to players in round
        
        players = game.players_in_round
        this_index = players.index(self)

        players.insert(this_index, player2)    #game.prompt_action() otherwise give it an input of players and run it again
        
        #Match bets:
        player2.bet_val = self.bet_val
        self.bank -= player2.bet_val

        #Split hands:
        player2.hand.append(self.hand[1])
        self.hand.remove(1) #double check that one card hands work and that we reunite the two players after.
        

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
            bet_value = input("How much would you like to bet? ")

            if not bet_value.isnumeric():
                continue

            elif self.bank < bet_value:
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


    def split(self, game: Game):
        #Add copy of player to players in round
        
        player2 = Player(self.name + '2', self.bank) #must make same type as Player
        
        super().split(game, player2)
        
        


class Bot(Player):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)
    

class BasicStrategist(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)

    def bet(self, game):
        if self.bank >= game.min_bet:
            self.bet_val = game.min_bet
            self.bank -= self.bet_val
            return True

        #else:
        self.bet_val = 0
        return False


    #Overload to make same type
    def split(self, game: Game):
        #Add copy of player to players in round
        
        player2 = BasicStrategist(self.name + '2', self.bank)
        
        super().split(game, player2)
    

    def play(self, game):
        hand = self.hand
        hand_vals = hand.get_hValue()
        upCard = game.dealer.upCard.get_cValue()

        action = ''
        while hand_vals[0] < 22 and action != 's' and action != 'd':
            action = '' #reset action
            
            #Hard:
            if hand_vals[0] == hand_vals[1] or hand_vals[1] > 21:
                #Default: hit

                if hand.num_of_cards() == 2 and self.bank >= self.bet_val:
                    
                    #Split:
                    ranks = hand.cards[0].get_cValue() #1-10, 11
                    if (hand.cards[0].rank == hand.cards[1].rank and ranks != 5 and ranks != 10):
                    
                        h_cond1 = (ranks == 4 and ((upCard > 1 and upCard < 5) or (upCard == 7)))
                        h_cond2 = (ranks < 8 and ranks > 1) and (upCard > 7 and upCard < 12)
                        h_cond3 = (ranks == 6 and upCard == 7)

                        stays = (ranks == 9) and (upCard == 7 or upCard > 9)

                        #spHit
                        if h_cond1 or h_cond2 or h_cond3:
                            action = 'h'
                            card = game.shoe.distribute_card()
                            self.hit(card)

                        elif stays:
                            action = 's'
                            self.stay()

                        else:
                            action = 'sp'
                            self.split(game)

                    
                    #Double:
                    else:  
                        double_condition1 = (hand_vals[0] == 10 or hand_vals[0] == 11) and (upCard < 10 and upCard > 1)
                        double_condition2 = (hand_vals[0] == 9) and (upCard > 2 and upCard < 7)
                        double_condition3 = (hand_vals[0] == 11 and upCard == 10)

                        if double_condition1 or double_condition2 or double_condition3:
                            action = 'd'
                            card = game.shoe.distribute_card()
                            self.double(card)


                #Standard
                if action == '':

                    #Hit
                    hcond1 = (upCard >= 11 and upCard > 6) and hand_vals[0] < 17
                    hcond2 = hand_vals[0] < 13 and (upCard < 4 and upCard >6)

                    if hcond1 or hcond2:
                        action = 'h'
                        card = game.shoe.distribute_card()
                        self.hit(card)

                    #Stay:
                    else:
                        action = 's'
                        self.stay()
            
            #Soft:
            else:
                #Double or Split
                if hand.num_of_cards() == 2 and self.bank >= self.bet_val:
                    double_condition1 = (hand_vals[1] > 19 and hand_vals[1] > 12 and upCard < 7 and upCard > 4)
                    double_condition2 = (hand_vals[1] < 19 and hand_vals[1] > 16 and upCard < 5 and upCard > 2)
                    double_condition3 = (hand_vals[1] < 17 and hand_vals[1] > 14 and upCard == 4)
                    
                    if hand.cards[0].rank == hand.card[1].rank:
                        action = 'sp'
                        self.split(game)

                    elif (double_condition1 or double_condition2 or double_condition3):
                        action = 'd'
                        card = game.shoe.distribute_card()
                        self.double(card)

                if action == '':

                    #Stay:
                    if (hand_vals[1] == 18 and upCard < 9) or hand_vals[1] > 18:
                        action = 's'
                        self.stay()
                    
                    else:
                        action = 'h'
                        card = game.shoe.distribute_card()
                        self.hit(card)
                


class Rando(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)

class DImitator(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)

class CardCounter(Bot):
    def __init__(self, name: str, bank: int):
        super().__init__(name, bank)
