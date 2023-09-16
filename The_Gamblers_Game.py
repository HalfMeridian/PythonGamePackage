import time
import random
import sys

#Declare Global Variables
global money
money = 100
global playername
playername = "null"
#Used to store blackjack cards.
global numberdeck
numberdeck = []

global suitdeck
suitdeck = []

#These are different true/false answers that can be legitimate.
positive_answer = ["Y", "YES", "YEAH", "YUP", "OK", "SURE", "FINE", "I GUESS"]
negative_answer = ["N", "NO", "NAH", "NOPE"]


#Dialogue tools
inDialogue = True
answer = "null"

"""
Things I might need to change/edit:
Balancing
Add timing to the game
Skill based games, timing game, maybe?
"""
def game_choice_menu():
    global money
    #This is the original game selection. First, checks for money, then asks for player choice on games.
    available_games = [ "[1]: Leave", "Luck-Based Games:", "[2]: Dice Game", "[3]: Slot Machine", "[4]: Card Table", "[5]: Blackjack"]

    #Money Check
    if(money > 0):
        print("You find that you still have", money, "dollars left.")
        print("You decide to do something. Your options are to:")
        for x in available_games:
            print(x)
        print("What would you like to do?")
        answer = input()
        inDialogue = True
        while inDialogue:
            if(answer == "1"):
                #Decision to leave the casino.
                print("You decide to leave the casino.")
                print("You walk out with", money, "dollars.")
                sys.exit()
                inDialogue = False
                return
            if(answer == "2"):
                print("You decide to play a dice game.")
                inDialogue = False
                diceGame()
            if(answer == "3"):
                print("You walk over to the slot machine and sit down.")
                inDialogue = False
                slotMachine()
            if(answer == "4"):
                print("You move to the card table.")
                inDialogue = False
                cardGame()
            if(answer == "5"):
                BlackJack()
            else:
                print("You feel racked with indecision. What would you like to do?")
                answer = input()


    #No money, so ends game
    else:
        print("You find that you have no money. You finally leave the casino behind.")
        if(money == 0):
            print("You ended up with no debt, but no money.")
        else:
            print("You ended up", money*-1, "dollars in debt.")
        sys.exit()
        return

def diceGame():
    global money
    if(money <= 0):
        return
    else:
        print("You find that you still have", money, "dollars left.")
        print("Would you like to hear the rules?")
        inDialogue = True
        answer = input()
        while inDialogue:
            if answer.upper() in positive_answer:
                print("There is a number that is between 1 and 6. If the dice are in your favor, you win some money.")
                inDialogue = False
            elif answer.upper() in negative_answer:
                inDialogue = False
            else:
                print("It was a good thing that incoherent mumbling wasn't understood by anyone else.")
                print("Would you like to hear the rules?")
                answer = input()
        print("How many dice would you like to roll?")
        diceCount = input()
        inDialogue = True
        while inDialogue:
            #Check that Dicecount is an int
            try:
                diceCount = int(diceCount)
            except:
                pass
            if not type(diceCount) == int:
                print("That was definitely not the right thing to say.")
                print("How many dice would you like to roll?")
                diceCount = input()
            elif diceCount < 0:
                print("You can't wager a negative number of dice. So how many is it going to be?")
                diceCount = input()
            else:
                inDialogue = False
        print("How much money do you wager on each dice?")
        wager = input()
        inDialogue = True
        while inDialogue:
            #Check that wager is an int
            try:
                wager = int(wager)
                if(wager < 0):
                    print("You can't wager negative money, though that would be a good way to win.")
                    print("How much would you care to wager?")
                    wager = input()
                elif diceCount * wager > money:
                    print("You can't wager that amount of money, because you realise that you don't have it.")
                    print("How much would you like to wager?")
                    wager = input()
                else:
                    inDialogue = False
            except:
                print("That did not make much sense. Betting is obviously restricted to whole dollars, under penalty of a likely death. (Or so you say to yourself.)")
                print("How much money would you like to wager per dice?")
                wager = input()


        print("What number from 1-6 do you guess?")
        guess = input()
        inDialogue = True
        while inDialogue:
            #Check that guess is an int
            try:
                guess = int(guess)
            except:
                pass
            if not (guess >= 1) and (guess <= 6):
                print("That's not even a number on the dice.")
                guess = input()
            elif not type(diceCount) == int:
                print("The cigar smoke must be getting to you. That's not a number on the dice.")
                print("What number on the dice do you think it will be?")
                guess = input()
            else:
                inDialogue = False
        #Calculations for winning
        if (diceCount > 1):
            winChance = 1
        else:
            winChance = 0

        #If you wager zero dice or zero dollars
        if(wager*diceCount == 0):
            print("You find you have no stake in this game, and you eyes wander.")
        else:
            for x in range(diceCount):
                i = random.randint(1,6)
                print("Dice number", x+1, "rolled a", str(i) + ".")
                time.sleep(1)
                if i == guess:
                    winChance = winChance + 1
                else:
                    winChance = winChance - 1
            if winChance >= 1:
                print("You won", wager * diceCount, "dollars!")
                money = money + (wager*diceCount*4)
            else:
                print("You lost", (wager * diceCount), "dollars.")
                money = money - (wager*diceCount)
        print("Do you want to leave the dice game?")
        inDialogue = True
        answer = input()
        while inDialogue:
            if answer.upper() in positive_answer:
                print("You choose to leave the dice table.")
                inDialogue = False
                game_choice_menu()
            elif answer.upper() in negative_answer:
                print("You choose to stay at this table.")
                diceGame()
                inDialogue = False
            else:
                print("Your ramblings, thank goodness, were heard by no one.")
                print("Would you like to stay here?")
                answer = input()

def slotMachine():
    global money
    tokencost = 5
    #Balance Var will make the rolls more or less worthwhile. The ideal balance is 80% return, but it can be a little more.
    balance = 2

    #Check for money
    if(money <= 0):
        return
    else:
        #Ask for token count
        print("You find you still have", money, "dollars.")
        print("Tokens are", tokencost, "dollars each.")
        print("How many tokens would you like?")
        slotTokens = input()
        inDialogue = True
        while inDialogue:
            try:
                slotTokens = int(slotTokens)
                if slotTokens*tokencost > money:
                    print("When you actually look into your pockets, you find that you don't have enough money.")
                    print("How many would you like?")
                    slotTokens = input()
                elif(slotTokens < 0):
                    print("The machine definitely can't take a negative number of dollars.")
                    print("How many would you like?")
                    slotTokens = input()
                else:
                    money = money - (tokencost * slotTokens)
                    inDialogue = False

            except:
                print("The machine doesn't seem to take amounts that aren't numbers.")
                print("How many tokens would you like?")
                slotTokens = input()
        #correcting a bug
        slotTokens = slotTokens + 1
        if(slotTokens == 0):
            print("You don't even get any slot tokens.")
        else:
            while slotTokens > 1:
                rollObjects = ["Dollar", "Cherry", "Lime", "Seven", "Skull"]
                #This is for skull balancing
                if(random.randint(0,1) == 1):
                    rollObjects = ["Dollar", "Cherry", "Lime", "Seven"]
                slotTokens = slotTokens - 1

                #Begin the show of rolls
                print("You have", slotTokens, "tokens left.")

                roll1 = random.choice(rollObjects)
                time.sleep(1)
                print("The first roll was a", roll1)

                roll2 = random.choice(rollObjects)
                time.sleep(1)
                print("The second roll was a", roll2)

                roll3 = random.choice(rollObjects)
                time.sleep(1)
                print("The third roll was a", roll3)
                time.sleep(2)

                #Calculations for winnings
                #Skull means immediate end
                if(roll1 == "Skull" and roll2 == "Skull" and roll3 == "Skull"):
                    print("You got three skulls. Here's a free token.")
                    slotTokens = slotTokens + 1
                elif(roll1 == "Skull" or roll2 == "Skull" or roll3 == "Skull"):
                    print("You got a Skull. You lost.")
                else:
                    #All three are the same
                    if(roll1 == roll2 == roll3):
                        if(roll1 == "Seven"):
                            winnings = 30 + balance
                            print("You win BIG! You won", winnings, "dollars!")
                            money = money + winnings
                        if(roll1 == "Lime"):
                            winnings = 18 + balance
                            print("You won", winnings, "dollars!")
                            money = money + winnings
                        if(roll1 == "Cherry"):
                            winnings = 21 + balance
                            print("You won", winnings, "dollars!")
                            money = money + winnings
                        if(roll1 == "Dollar"):
                            winnings = 23 + balance
                            print("You won", winnings, "dollars!")
                            money = money + winnings
                    else:
                        #Two are the same
                        if(roll1 == roll2):
                            if(roll1 == "Dollar"):
                                winnings = 5 + balance
                            if(roll1 == "Lime"):
                                winnings = 3 + balance
                            if(roll1 == "Cherry"):
                                winnings = 4 + balance
                            if(roll1 == "Seven"):
                                winnings = 7 + balance
                            print("You won", winnings, "dollars!")
                            money = money + winnings
                        elif(roll2 == roll3):
                            if(roll1 == "Dollar"):
                                winnings = 5 + balance
                            if(roll1 == "Lime"):
                                winnings = 3 + balance
                            if(roll1 == "Cherry"):
                                winnings = 5 + balance
                            if(roll1 == "Seven"):
                                winnings = 7 + balance
                            #Less reward bonus for second order
                            winnings = winnings - 1 + balance
                            print("You won", winnings, "dollars!")
                            money = money + winnings
                        elif(roll3 == roll1):
                            if(roll1 == "Dollar"):
                                winnings = 5 + balance
                            if(roll1 == "Lime"):
                                winnings = 3 + balance
                            if(roll1 == "Cherry"):
                                winnings = 5 + balance
                            if(roll1 == "Seven"):
                                winnings = 7 + balance
                            #Even less reward bonus for third order.
                            winnings = winnings - 2 + balance
                            print("You won", winnings, "dollars!")
                            money = money + winnings
                        else:
                            print("You didn't win. Better luck next time.")
                print(" ")
                print(" ")
            print("That's all the tokens you have.")
        print("Would you like to leave the slot machine?")
        answer = input()
        inDialogue = True
        while inDialogue:
            if answer.upper() in positive_answer:
                inDialogue = False
                game_choice_menu()
            if answer.upper() in negative_answer:
                print("You choose to stay put.")
                slotMachine()
            else:
                print("That rationalizing made absolutely no sense. What would you like to do?")
                answer = input()

def cardGame():
    global money
    global suitdeck
    if money <= 0:
        game_choice_menu()
    else:
        print("You move over to the card table with", money, "dollars in your pocket.")
        print("Would you like to hear the rules to the card game?")
        answer = input()
        inDialogue = True
        while inDialogue:
            if answer.upper() in positive_answer:
                print("You will guess a suit the card will be. If you are right, you will triple your wager.")
                print("Otherwise, you divide your wager by 2 of the money you wagered. Then you can guess again, until you want to quit.")
                inDialogue = False
            elif answer.upper() in negative_answer:
                inDialogue = False
            else:
                print("That completely incoherent string of words that came out of your mouth was ridiculous.")
                print("Would you like to hear the rules to the card game?")
                answer = input()
        print("Let's begin. How much would you like to wager?")
        wager = input()
        inDialogue = True
        while inDialogue:
            try:
                wager = int(wager)
                if wager < 0:
                    print("You can't wager a negative number of dollars. How much would you like to wager?")
                    wager = input()
                elif wager > money:
                    print("You don't have enough money to wager that. What would you like to wager?")
                    wager = input()
                else:
                    money = money - wager
                    inDialogue = False
            except:
                print("That didn't make any sense. Do you want to try that again?")
                print("How much would you like to wager?")
                wager = input()
        card_options = ["Diamonds", "Hearts", "Spades", "Clubs"]
        while(wager > 0):
            inDialogue = True
            if len(suitdeck) < 5:
                print("The deck was shuffled")
                suitdeck = ["Clubs", "Hearts", "Spades", "Diamonds"] * 13
                random.shuffle(suitdeck)
            while inDialogue:
                time.sleep(1)
                print("What suit do you think the card will be? It can either be diamonds, hearts, clubs, or spades. You can also quit.")
                player_choice = input()
                if wager <= 0:
                    print("You lost your wager.")
                    inDialogue = False
                    break
                elif(player_choice.upper() == "QUIT"):
                    print("You choose to stop playing with your current wager of", str(wager) + ".")
                    money = money + wager
                    inDialogue = False
                    break
                elif player_choice.upper() in (card.upper() for card in card_options):
                    correct_choice = (suitdeck.pop())
                    print("The suit of the card turned out to be a", correct_choice + ".")
                    if player_choice.upper() == correct_choice.upper():
                        wager = int(wager * 3)
                        print("You got it correct, and your wager increased. It is now", str(wager) + ".")
                    else:
                        wager = int(wager / 2)
                        print("That was not the correct suit. You wager is now", str(wager) + ".")
                else:
                    print("That's not one of the options for the suits.")
                    print("It can be a diamonds, hearts, clubs, or a spades. You can also choose to quit.")
                    player_choice = input()
            print("Would you like to leave the table?")
            answer = input()
            inDialogue = True
            while inDialogue:
                if answer.upper() in positive_answer:
                    inDialogue = False
                    game_choice_menu()
                if answer.upper() in negative_answer:
                    print("You choose to stay at the table.")
                    cardGame()
                else:
                    print("Your incoherent ramblings made no sense. What would you like to do?")
                    answer = input()

def BlackJack():
    global money
    global numberdeck
    if money < 0:
        return
    else:
        print("You decide to play blackjack with", money, "dollars in your pocket.")
        print("Would you like to hear the rules to the game?")
        answer = input()
        inDialogue = True
        while inDialogue:
            if answer.upper() in positive_answer:
                print("You will place a bet, and the dealer will match it. You will be given two cards, and you will see one of the dealer's cards.")
                print("You can either stay or hit, and you are aiming to get twenty one. But be careful, because if you get over, you immediately lose.")
                inDialogue = False
            elif answer.upper() in negative_answer:
                inDialogue = False
            else:
                print("The question goes unanswered. Do you want to hear the rules?")
                answer = input()
        print("What do you bet?")
        bet = input()
        inDialogue = True
        while inDialogue:
            try:
                bet = int(bet)
                if bet > money:
                    print("You don't have enough money for that bet. What would you like to bet?")
                    bet = input()
                elif bet < 0:
                    print("You can't bet a negative number of dollars. What would you like to bet?")
                    bet = input()
                else:
                    money = money - bet
                    inDialogue = False
            except:
                print("That's not something that you can bet. Good thing nobody heard that. What would you like to bet?")
                bet = input()
        #Make sure bet is not zero.
        if bet > 0:
            #Deck Shuffle
            if len(numberdeck) < 8:
                print("The deck was shuffled.")
                numberdeck = [2,3,4,5,6,7,8,9,10,10,10,10,11]*4
                random.shuffle(numberdeck)
            playercards = []
            dealercards = []
            #Get cards for the player
            playercards = [numberdeck.pop(), numberdeck.pop()]
            print("You drew a", str(playercards[0]), "and a", str(playercards[1]) + ".")
            time.sleep(1)
            dealercards = [numberdeck.pop(), numberdeck.pop()]
            playertotal = sum(playercards)
            dealertotal = sum(dealercards)
            print("The dealer has a", str(dealercards[0]), "and another card.")
            time.sleep(1)
            gameComplete = False
            inDialogue = True
            while inDialogue:
                time.sleep(2)
                if dealertotal > 21:
                    print("The dealer went over 21. You win!")
                    print("You won", bet*2, "dollars.")
                    money = money + bet * 2
                    inDialogue = False
                    gameComplete = True
                elif playertotal > 21:
                    print("You went over 21. You lose.")
                    print("You lost", bet, "dollars.")
                    inDialogue = False
                    gameComplete = True
                elif playertotal == 21:
                    print("You win with a blackjack!")
                    print("You won", bet * 3, "dollars!")
                    money = money + bet * 3
                    inDialogue = False
                    gameComplete = True
                else:
                    print("You can either stay, or you can hit.")
                    answer = input()
                    if answer.upper() == "HIT":
                        print("You choose to hit.")
                        playercards.append(numberdeck.pop())
                        playertotal = sum(playercards)
                        time.sleep(1)
                        print("You now have", str(playertotal) + ".")
                    elif answer.upper() == "STAY":
                        print("You choose to stay.")
                        inDialogue = False
            time.sleep(1)
            if gameComplete == False:
                print("The dealer has", dealercards[0], "and a", str(dealercards[1]) + ".")
                print("This makes the dealer's total", str(dealertotal) + ".")
            while gameComplete == False:
                if dealertotal < 17:
                     dealercards.append(numberdeck.pop())
                     dealertotal = sum(dealercards)
                     time.sleep(1)
                     print("The dealer's total is now", str(dealertotal) + ".")
                elif(dealertotal == 21):
                    print("The dealer won with 21.")
                    gameComplete = True
                else:
                    print("The dealer stays.")
                    time.sleep(1)
                    print("Your total was", str(playertotal), "and the dealer's was", str(dealertotal) + ".")
                    if ((playertotal > dealertotal) and (playertotal < 22)) or dealertotal > 21:
                        print("You won", bet*3, "dollars!")
                        gameComplete = True
                        money = money + bet * 3
                    else:
                        print("The dealer won.")
                        gameComplete = True

        else:
            print("You find your intrest is not on the game.")
        print("Would you like to stay at this table?")
        answer = input()
        inDialogue = True
        while inDialogue:
            if answer.upper() in negative_answer:
                inDialogue = False
                game_choice_menu()
            if answer.upper() in positive_answer:
                print("You choose to stay at the table.")
                BlackJack()
            else:
                print("That's not really possible. Would you like to leave?")
                answer = input()



#Begin the game and ask for playername
print("""
 ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄  ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄
█       █  █ █  █       █  █       █      █  █▄█  █  ▄    █   █   █       █   ▄  █ █  ██       █  █       █      █  █▄█  █       █
█▄     ▄█  █▄█  █    ▄▄▄█  █   ▄▄▄▄█  ▄   █       █ █▄█   █   █   █    ▄▄▄█  █ █ █ █▄▄██  ▄▄▄▄▄█  █   ▄▄▄▄█  ▄   █       █    ▄▄▄█
  █   █ █       █   █▄▄▄   █  █  ▄▄█ █▄█  █       █       █   █   █   █▄▄▄█   █▄▄█▄    █ █▄▄▄▄▄   █  █  ▄▄█ █▄█  █       █   █▄▄▄
  █   █ █   ▄   █    ▄▄▄█  █  █ █  █      █       █  ▄   ██   █▄▄▄█    ▄▄▄█    ▄▄  █   █▄▄▄▄▄  █  █  █ █  █      █       █    ▄▄▄█
  █   █ █  █ █  █   █▄▄▄   █  █▄▄█ █  ▄   █ ██▄██ █ █▄█   █       █   █▄▄▄█   █  █ █    ▄▄▄▄▄█ █  █  █▄▄█ █  ▄   █ ██▄██ █   █▄▄▄
  █▄▄▄█ █▄▄█ █▄▄█▄▄▄▄▄▄▄█  █▄▄▄▄▄▄▄█▄█ █▄▄█▄█   █▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄█  █▄█   █▄▄▄▄▄▄▄█  █▄▄▄▄▄▄▄█▄█ █▄▄█▄█   █▄█▄▄▄▄▄▄▄█   V2.1
  A Half Meridian Game
""")
time.sleep(3)

print("Walking into the casino, you feel the smell of cigar smoke and whiskey wash over you.")
print("Looking into your wallet, you find a small amount of bills,",money,"dollars to be exact.")
print("You also see your ID. What name do you find on it?")
playername = input()
while inDialogue:
    print("It says the name", playername + ".")
    print("Did you read that correctly?")
    answer = input()
    if(answer.upper() in positive_answer):
        inDialogue = False
    elif(answer.upper() in negative_answer):
        print("You must have read that wrong. It actually says,")
        playername = input()
    else:
        print("That's doesn't make sense. Must be some sort of incoherent thought, brought on by too little sleep.")
game_choice_menu()
