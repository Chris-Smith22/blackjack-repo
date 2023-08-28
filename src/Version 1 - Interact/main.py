#!/usr/bin/python
from deck import *
from players import *
from game_bs import *



#def round():


def play():
    print("Starting game...")
    #num_of_players = input("How many players would you like to play with? ")
    #players
    #num_of_decks = input()
    #note dealer does not stand on soft 17

    #Setup dealer, players, game
    dealer = Dealer(stand_value = 17)
    player1 = Player('Chris', 500)
    game = Game(1, [player1], dealer, 6, 25, 1000)


    #Prompt bet, initial deal:
    while player1.bank >= 25:
        bets_present = False
        players_in_round = game.prompt_bet()
        
        for player in players_in_round:
            if player.bet_val > 0:
                bets_present = True

        if not bets_present:
             endRound(game)
             print("Thank you for playing!")
             break
             
        game.set_players_in_round(players_in_round)
        game.initial_deal()

        #Play:
        if game.dealer.hand.get_hValue()[1] != 21:
            game.prompt_action(game.players_in_round)
        else:
             game.display_hands(True)
        
        
        game.play_dealer()
        
        print(f"Round {game.round} over.\n")
        input("Press enter for next round.\n")
        endRound(game)
        

    

        
    
def runSim():
     pass

def endRound(game):
    game.display_standings()
    game.clean_up()
    

#main()
if __name__ == '__main__':
        play()
    
