from players import *
from deck import *

class Game:

    def __init__(self, players, dealer, num_of_decks, min_bet, max_bet):

        self.players = players
        self.dealer = dealer
        self.house_standing = 0

        self.shoe = Shoe(num_of_decks)
        self.min_bet = min_bet
        self.max_bet = max_bet
        
        self.round = 0
        self.players_in_round = []
    

    def prompt_bet(self):
        #Prompts each player to bet. Returns players in this round.
        playing = []
        for player in self.players:
            
            #skip players who cant bet
            if player.bank < self.min_bet:
                continue

            bet = player.bet(self)
            if bet:
                playing.append(player)

        return playing
        

    def initial_deal(self):
        #Deal 2 cards to each player, 1 at a time, if player bets:

        for i in range(2):
            for player in self.players_in_round:
                card = self.shoe.distribute_card()
                player.hand.add_card(card)
                    
            card_d = self.shoe.distribute_card()
            self.dealer.hand.add_card(card_d)

        self.dealer.set_upCard()
        self.round +=1


    def display_hands(self, played: bool):
        for player in self.players_in_round:
            player.display_cards()
        self.dealer.display_cards(played)

    def set_players_in_round(self, players_in_round):
        self.players_in_round = players_in_round
        return


    def prompt_action(self, players):
        #prompt each given player to act

        for player in players:
            hand = player.hand

            #Check Bot
            if isinstance(player, player.Bot):
                player.play(self)
            
            #Player
            else:
                
                action = ''
                while (hand.get_hValue()[0] < 21) and (action.upper() != 'D') \
                    and (hand.get_hValue()[1] != 21) and (action.upper() != 'S'):
                    
                    player.display_cards()
                    self.dealer.display_cards(False)
                    print("")
                    
                    if hand.num_of_cards == 2 : 
                        #Add Split:
                        if hand.cards[0] == hand.cards[1]:
                            action = input("Hit (H), Stand (S), Double (D), or Split(P)? ")

                        #Initial options
                        elif player.bank >= player.bet_val:
                            action = input("Hit (H), Stand (S), or Double (D)? ")

                        else:
                            action = input("Hit (H) or Stand (S)? ")
                    
                    else:
                        action = input("Hit (H) or Stand (S)? ")
                    
                    player.play(action.upper(), self.shoe)
            
            #Result of actions:
            player.display_cards()

                #Natural Blackjack
            if hand.get_hValue()[1] == 21 and hand.get_hValue()[0] != 21:
                print("Blackjack!")
                self.payout(player)

                #Bust
            elif hand.get_hValue()[0] >= 22:
                print("Busted.")
                self.house_standing += player.bet_val
                player.bet_val = 0
    


    def play_dealer(self):
        print("\n")
        d_hand = self.dealer.hand

        self.dealer.display_cards(True)

        #Check Dealer 21
        if d_hand.get_hValue()[1] == 21:
            print("Dealer has blackjack!")
            for player in self.players_in_round:
                self.house_standing += player.bet_val
                player.bet_val = 0
            return
        

        #Hit:
        while d_hand.get_hValue()[0] < 17:

            #Stand on soft 17
            if d_hand.get_hValue()[1] > 16 and d_hand.get_hValue()[1] < 22:
                break

            card = self.shoe.distribute_card()
            self.dealer.hit(card)
            print("Hit!")
            self.dealer.display_cards(True)


        #Dealer busts
        if d_hand.get_hValue()[0] > 21:
            for player in self.players_in_round:
                if player.bet_val > 0:
                    self.payout(player)

        #Compare hands:
        for player in self.players_in_round:
            if player.bet_val > 0:
                hand2 = player.hand.get_hValue()[1] 

                #Max of h1 and h2(A=11)
                if hand2 <= 21:
                    p_hand = hand2

                else: #case where hand2(A=11) > 21 but hand1 < 21
                    p_hand = player.hand.get_hValue()[0]


                #Player beats Dealer
                if p_hand > d_hand.get_hValue()[0]:
                    self.payout(player)
                
                #Push
                elif p_hand == d_hand.get_hValue()[0]:
                    print(f"Push. You receive your bet back: {player.bet_val}")
                    player.bank += player.bet_val
                    player.bet_val = 0

                #Dealer beats player
                else:
                    self.house_standing += player.bet_val
                    player.bet_val = 0


    def display_standings(self):
        print("\nThe standings are:")
        for player in self.players:
            print(f"\t{player.name} stands at ${player.bank}")
        print(f"\n\tThe House stands at ${self.house_standing}.")



    def payout(self, player):
        pay = 0
        if len(player.hand.cards) == 2 and player.hand.get_hValue()[1] == 21:
            print("Blackjack pays 3:2")
            pay = player.bet_val * 3/2     #3/2 + initial bet
        
        else:
            pay = player.bet_val       #even + initial bet
        
        #Split player:
        if player.name.endswith('2'):
            for person in self.players_in_round:
                if person.name == player.name.strip('2'):
                    #Person is player
                    temp = player
                    player = person
                    self.players_in_round.remove(temp)

                    



        player.bank += player.bet_val + pay
        player.bet_val = 0
        print(f"You won ${pay}")
        print(f"Your balance now stands at ${player.bank}")
        self.house_standing -= pay
        #print(f"The House now stands at {self.house_standing}")


    def clean_up(self):
        for player in self.players:
            player.hand.cards = []
            player.bet_val = 0
        self.dealer.hand.cards = []
        
