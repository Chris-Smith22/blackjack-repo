from random import *
import tkinter as tk

def main():
    window = tk.Tk()

    greeting = tk.Label(text="Starting game...")
    score = 0
    num_qs = 0

    while True:
        num_qs += 1
        pair = getPair()
        ans = getAns(pair)

        print("\n ", pair, "\n")
        user_in = input("H, S, Dh, Rh, or q? \t")

        if ans.upper() == user_in.upper():
            score += 1
            print("Correct! Score:", str(score)+ '/'+ str(num_qs))

        elif user_in.lower() == 'q':
            break

        else:
            print("False. Score:", str(score)+ '/'+ str(num_qs))
    
    print("Game over. Score:", str(score) + '/' + str(num_qs - 1) + '\n\n')



def getPair():
    p = randint(4,21) #returns num between 4 and 21
    d = randint(2,11)
    return (p,d)


def getAns(pair):
    #Default: hit
    ans = 'H'


    #Surrender/hit:
    if pair == (15,10):
        ans = 'Rh'

    elif pair[0] == 16 and (pair[1] > 8):
        ans = 'Rh'


    #Double/hit:
    elif (pair[0] == 9 and (pair[1] > 2 and pair[1] < 7)):
        ans = 'Dh'

    elif (pair[0] == 10 or pair[0] == 11):  
        if (pair[1] < 10):
            ans = 'Dh'
    
    elif pair == (11,10):
        ans = 'Dh'
    

    #Stays:
    elif pair[0] > 12 and pair[1] < 7:
        ans = 'S'

    elif pair[0] == 12 and (pair[1] < 7 and pair[1] > 3):
        ans = 'S'
    
    elif pair[0] > 16:
        ans = 'S'

    return ans




if __name__ == '__main__':
    main()