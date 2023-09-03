#!/usr/bin/python
from deck import *
from players import *
from game_bs import *



#def round():


def play_game():
    #Default settings
    d_stand = 17
    initial_bank = 500

    #Setup:
    players_num = int(input("How many players will be playing? "))
    players = []
    for i in range(players_num):
         print(f"Player {i+1}'s name is: ", end='')
         name = input()
         players.append(Player(name, initial_bank))
    
#Initialize Game:
    
    dealer = Dealer(d_stand)
    game = Game(dealer, players)

    print(f"\n\nThe default settings are the following:\n\tDealer stands on {d_stand}\n\
        Players start with ${initial_bank}\n\tThere are 6 decks in a shoe\n\tMin bet: 5 and Max bet : 1000.\n")
    
    print("Starting game...")
    
#Game's Loop:
    while len(players) > 0:
    
    #round setup
        playing = game.prompt_bet()

        if len(playing) == 0:
            endRound(game) #cleanup players hands and display standings
            print("Thank you for Playing!")
            break
        
        game.players_in_round = playing
        game.initial_deal()
        #game.display_hands(False)
        
    #play round:
        if game.dealer.hand.get_hValue()[1] != 21:
            game.prompt_action()
        game.play_dealer()

        #game.payout() #pay players_in_round and pay house those who are beat -bj and bust already paid

    #end round:
        endRound(game)
        print(f"Round {game.round} over.\n")
        input("Press enter for next round.\n")
    

        
    
def run_sim():

    #Setup Game
    d_stand = 17
    initial_bank = 500

    bot1 = BasicStrategist("BasicBot", initial_bank)
    players = [bot1]

    dealer = Dealer(d_stand)
    game = Game(dealer, players)

    #Game's Loop:
    while len(players) > 0:
    
    #round setup
        playing = game.prompt_bet()

        if len(playing) == 0:
            endRound(game) #cleanup players hands and display standings
            print("Thank you for Playing!")
            break
        
        game.players_in_round = playing
        game.initial_deal()
        
        
    #play round:
        if game.dealer.hand.get_hValue()[1] != 21:
            game.prompt_action()
        game.play_dealer()

    #end round:
        endRound(game)
        print(f"Round {game.round} over.\n")





def endRound(game):
    game.display_standings()
    game.clean_up()
    for player in game.gplayers:
         if player.bank < game.min_bet:
              game.gplayers.remove(player)
    

#main()
if __name__ == '__main__':
        #play_game()
        run_sim()
    
