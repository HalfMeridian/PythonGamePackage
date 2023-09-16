import time
import sys
import art
import random
#declare global variables
#Order is [iron, copper, zinc, tin, lead, nickel, chromium, steel, brass, bronze, soul]
global metals
global HP
global enemyHealth #Calling a variable from engageCombat FN
global maxEnemyHealth
#Default: Warm. Order is [warm, temperate, cool, cold, frigid, frozen]
global temp
global coins
global weapons
global blueprints
#Order is [healing, warming, damage, coal, soul, wood]
global inventory
metals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
inventory = [0, 0, 0, 0, 0, 0]
coins = 0
temp = "temperate"
HP = 80
blueprints = []
weapons = []
global inCombat

class useWeapons: #Declare weapons Class
    def __init__(self, name, damage, defense, luck):
        self.name = name
        self.damage = damage
        self.defense = defense
        self.luck = luck
class enemy:
    def __init__(self, name, damage, defense, luck, health):
        self.name = name
        self.damage = damage
        self.defense = defense
        self.luck = luck
        self.health = health
def DEVTOOL():
    print("Devtool engaged. Performing selected task.")
    global weapons
    global inventory
    global metals
    global blueprints
    weapons.append(useWeapons("Basic Axe", 2, 1, 1))
    engageCombat() #This one is for me.

def checkHP():
    healthDashes = 20
    maxHealth = 100
    dashConvert = int(maxHealth/healthDashes)            # Get the number to divide by to convert health to dashes (being 10)
    currentDashes = int(HP/dashConvert)              # Convert health to dash count: 80/10 => 8 dashes
    remainingHealth = healthDashes - currentDashes       # Get the health remaining to fill as space => 12 spaces

    healthDisplay = '-' * currentDashes                  # Convert 8 to 8 dashes as a string:   "--------"
    remainingDisplay = ' ' * remainingHealth             # Convert 12 to 12 spaces as a string: "            "
    percent = str(int((HP/maxHealth)*100)) + "%"     # Get the percent as a whole number:   40%

    print("|" + healthDisplay + remainingDisplay + "|")  # Print out textbased healthbar
    print("         " + percent) #Used to Check HP #Used to check HP of player
def checkHPCombat(): #This is used to check HP while in combat.
    maxHealth = 100
    global inCombat
    global HP
    percent = str(int((HP/maxHealth)*100)) + "%"     # Get the percent as a whole number:   40%
    print("         " + percent) #Used to Check HP #Used to check HP of player
    if(HP < 0):
        print("You were knocked unconcious in battle. Your enemy stole your coins.")
        print("You wake up back in the forge, ready for another adventure.")
        HP = 50
        coins = 0
        inCombat = "false"
        mapD3Interior()
def checkHPEnemy():
    global coins
    global enemyHealth #Calling a variable from engageCombat FN
    global maxEnemyHealth
    global inCombat
    if(enemyHealth > 0):
        percent = str(int((enemyHealth/maxEnemyHealth)*100)) + "%"     # Get the percent as a whole number:   40%
        print("         " + percent) #Used to Check HP
    if(enemyHealth <= 0):
        loot = random.randint(1,2) #Rolls for Metals, or Inventory Resources.
        if(loot == 1): #Gives Metals
            metalLoot = random.randint(0,6)
            if(metalLoot == 0):
                metals[0] = metals[0] +1
                print("You gained 1 iron.")
            if(metalLoot == 1):
                metals[1] = metals[1] +1
                print("You gained 1 copper.")
            if(metalLoot == 2):
                metals[2] = metals[2] +1
                print("You gained 1 zinc.")
            if(metalLoot == 3):
                metals[3] = metals[3] +1
                print("You gained 1 tin.")
            if(metalLoot == 4):
                metals[4] = metals[4] +1
                print("You gained 1 lead.")
            if(metalLoot == 5):
                metals[5] = metals[5] +1
                print("You gained 1 nickel.")
            if(metalLoot == 6):
                metals[6] = metals[6] +1
                print("You gained 1 chromium.")
        if(loot == 2): #Gives INV resources, excluding soul.
            invLoot = random.randint(1,2)
            if(invLoot==1):
                inventory[3] = inventory[3] +1
                print("You gained 1 coal.")
            if(invLoot==2):
                inventory[5] = inventory[5] +1
                print("You gained 1 wood.")
        coins = coins +10
        time.sleep(1)
        print("You won the fight. Your health is")
        checkHP()
        inCombat = "false"
def checkTemp():
    print("You feel " + temp + ".") #Used to Check TEMP
def engageCombat(): #Start Combat
    global HP
    global enemyHealth #To send the variable to checkHPEnemy FN
    type = random.randint(1,1)
    if(type == 1):
        enemyName = "Rogue Brazen"
        enemyDMG = random.randint(10,20)
        enemyDEF = random.randint(10,20)
        enemyLUCK = random.randint(1,3)
        enemyHEALTH = enemyDEF #Creates a Rogue Brazen
    yourEnemy = enemy(enemyName, enemyDMG, enemyDEF, enemyLUCK, enemyHEALTH)
    print("You encounter a " + yourEnemy.name)
    print("It's stats are: DMG-" + str(yourEnemy.damage) + " DEF-" + str(yourEnemy.defense) + " LUCK-" + str(yourEnemy.luck))
    print("What would you like to do?")
    print("Options: ATTACK, BLOCK")
    enemyHealth = yourEnemy.defense-yourEnemy.luck
    global maxEnemyHealth
    maxEnemyHealth = int(yourEnemy.defense)
    tempMultiplier = 0
    if(temp == "warm"):
        tempMultiplier = .5
    if(temp == "temperate"):
        tempMultiplier = 1
    if(temp == "cool"):
        tempMultiplier = 1.5
    if(temp == "cold"):
        tempMultiplier = 2
    if(temp == "frigid"):
        tempMultiplier = 3
    choice = input()
    ans = "incorrect"
    global inCombat
    global coins
    global HP
    inCombat = "true"
    while(inCombat == "true"):
        #return enemyHealth
        #return HP
        if(choice.upper() == "REROLL"): #For testing purposes.
            engageCombat()
        if(choice.upper() == "BLOCK"):
            playerLuck = random.randint(1,weapons[0].luck)#Sets the luck of the player, min 1, no max.
            damageDealtPlayer = round((yourEnemy.damage*yourEnemy.luck - weapons[0].defense*5)/tempMultiplier)
            damageDealtEnemy = round(((yourEnemy.defense - weapons[0].damage/5*playerLuck)/2)/tempMultiplier)
            enemyHealth = enemyHealth - damageDealtEnemy
            HP = HP - damageDealtPlayer
            print("Your HP:")
            checkHPCombat()
            print("Enemy's HP:")
            checkHPEnemy()
            print("Options: ATTACK, BLOCK")
            choice = input()
        if(choice.upper() == "ATTACK"):
            playerLuck = random.randint(1,weapons[0].luck)#Sets the luck of the player, min 1, no max.
            damageDealtEnemy = round(((yourEnemy.defense*3 - weapons[0].damage*playerLuck*2)/3)/tempMultiplier)
            damageDealtPlayer = round(((yourEnemy.damage*3*yourEnemy.luck - weapons[0].defense)/2)*tempMultiplier)
            enemyHealth = enemyHealth - damageDealtEnemy
            HP = HP - damageDealtPlayer
            print("Your HP:")
            checkHPCombat()
            print("Enemy's HP:")
            checkHPEnemy()
            print("Options: ATTACK, BLOCK")
            choice = input()
        else:
            print("That's not one of the options. Either ATTACK or BLOCK.")
            choice = input()
def Menu():
    art.Menu()
def startUp():
    print("You open your eyes. Everything around you is snowy and bitter cold. You have been exiled from Wainwright,")
    print("your home. Everyone around you has turned their back on you, and you have been put to the test.")
    print("It's time to survive.")
    print("Options: GET UP, THINK")
    #This is where all the (global)variables are set for the first time.
    global metals
    metals = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    global inventory
    inventory = [0, 0, 0, 0, 0, 1]
    global coins
    coins = 0
    global HP
    HP = 80
    global temp
    temp = "cool"
    global blueprints
    blueprints = []
    blueprints.append("Basic Axe")
    choice = input()
    time.sleep(1)
    ans = "incorrect"
    while(ans == "incorrect"):
         if(choice.upper() == "GET UP"):
            print("You decide to get up. Your eyes adjust and you see a town in the distance.")
            ans = "correct"
            mapD3Encounter()  #start moving on the map
         elif(choice.upper() == "THINK"):
            print("Your memory seems to be coming back. You remember how you used to have a family back in Wainwright. You")
            print("remember your life as a smith, running your own forge. But your town had a special rule:")
            print("If you can't produce what the town needs, you are removed. That rule cost you all your livelihood, and")
            print("is the reason you are here now.")
            print("Options: GET UP, THINK")
            choice = input()
         elif(choice.upper() == "DEVTOOL"): #This is the devtool, which is for me.
            DEVTOOL()
         elif(choice.upper() == "CHECK HEALTH"):
            checkHP()
            choice = input()
         elif(choice.upper() == "CHECK TEMP"):
            checkTemp()
            choice = input()
         else:
            print("That's not something you can do.")
            print("options: GET UP, THINK")
            choice = input() #When game starts up, first scene
def mapD3Encounter(): #Upon encountering mapD3 for the first time
    print("You see a distant shack on the horizon. You wonder what it's doing there.")
    print("Options: LOOK AROUND, GO TOWARDS SHACK")
    choice = input()
    time.sleep(1)
    ans = "incorrect"
    while(ans == "incorrect"):
        if(choice.upper() == "LOOK AROUND"):
            print("Around you, you see trees and snow. There is a shack on the horizon, which looks important, or at")
            print("least your best chance of survival.")
            print("Options: GO TOWARDS SHACK")
            choice = input()
        elif(choice.upper() == "GO TOWARDS SHACK"):
            print("You walk towards the shack. Upon arriving there, you enter.")
            ans = "correct"
            mapD3InteriorFirst() #Go inside mapD3 interior.
        elif(choice.upper() == "CHECK HEALTH"):
           checkHP()
           choice = input()
        elif(choice.upper() == "CHECK TEMP"):
           checkTemp()
           choice = input()
        else:
            print("That's not something you can do.")
            print("Options: LOOK AROUND, GO TOWARDS SHACK")
            choice = input()
def mapD3InteriorFirst(): #Interior of mapD3Interior, for the first time
    print("As you enter, you notice that this is a forge. Old memories flood over you and fill you with a desire for the way")
    print("things used to be.")
    print("Options: LOOK AROUND")
    choice = input()
    time.sleep(1)
    ans = "incorrect"
    while(ans == "incorrect"):
        if(choice.upper() == "LOOK AROUND"):
            print("You look around and discover all the machinery still works. You begin to wonder whether this would")
            print("be a good place to settle down. You could work here and probably make weapons to survive.")
            ans = "correct"
            mapD3Interior()
        elif(choice.upper() == "CHECK HEALTH"):
           checkHP()
           choice = input()
        elif(choice.upper() == "CHECK TEMP"):
           checkTemp()
           choice = input()
        else:
            print("That's not something you can do.")
            print("Options: LOOK AROUND")
            choice = input()
def mapD3Exterior():
    global inCombat
    inCombat = "true"
    while(inCombat == "true"):
        engageCombat()
    print("That's the end of the game for now.")
def mapD3Interior():
    print("You are now inside the Forge. What would you like to do?")
    print("Options: START FORGE, SLEEP, LOOK AROUND, EXIT")
    choice = input()
    time.sleep(1)
    ans = "incorrect"
    while(ans == "incorrect"):
        if(choice.upper() == "START FORGE"):
            #art.forgeArt() #Forge Artwork
            beginForge()
            ans = "correct"
        elif(choice.upper() == "SLEEP"):
            print("You chose to sleep. Your HP has been refilled and temperature is temperate.")
            global HP
            HP = 100
            global temp
            temp = "temperate"
            print("Options: START FORGE, SLEEP, LOOK AROUND, EXIT")
            choice = input()
        elif(choice.upper() == "LOOK AROUND"):
            print("As you look around, you notice a note. It says:")
            print("More resources in Keechketan.")
            print("You also find a map.")
            print("Options:START FORGE, SLEEP, LOOK AROUND, EXIT")
            choice = input()
        elif(choice.upper() == "EXIT"):
            try: #About the jankyiest soloution to this problem.
                if(weapons[0] != "placeholder"): #This makes sure that you have some weapons
                    print("You venture out into the cold. ")
                    ans = "correct"
                    mapD3Exterior()
            except:
                    print("I don't think it would be a good idea to exit without a weapon.")
                    print("Options: START FORGE, SLEEP, LOOK AROUND, EXIT")
                    choice = input()
        elif(choice.upper() == "CHECK HEALTH"):
           checkHP()
           choice = input()
        elif(choice.upper() == "CHECK TEMP"):
           checkTemp()
           choice = input()
        else:
            print("That's not something you can do.")
            print("Options: START FORGE, SLEEP, LOOK AROUND, EXIT")
            choice = input()
def beginForge():
    global inventory
    global weapons
    global metals
    global blueprints
    print("You start the forge. You can make alloys and weapons with the metals you collected.")
    print("Options: MAKE ALLOYS, MAKE WEAPONS, CHECK METALS, CHECK INVENTORY, EXIT")
    ans = "incorrect"
    choice = input()
    time.sleep(1)
    def checkInventory():
        print("You Have:")
        print("Coal: " + str(inventory[3]))
        print("Soul Powder: " + str(inventory[4]))
        print("Wood: " + str(inventory[5]))
    def makeAlloys():
        print("The alloys you can make are steel, brass, bronze, and soul")
        print("Which one would you like to make?")
        print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
        global metals
        global inventory
        choice2 = input()
        ans2 = "incorrect"
        while(ans2 == "incorrect"):
            if(choice2.upper() == "EXIT"):
                choice2 = "correct"
                beginForge()
            elif(choice2.upper() == "STEEL"):
                if(metals[0] >= 1 and inventory[3] >= 1):
                    print("You make steel.")
                    metals[7] = metals[7] + 1 #Adds new alloy
                    metals[0] = metals[0] - 1 #Takes old Metal
                    inventory[3] = inventory[3] - 1 #Uses old resource
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
                else:
                    print("You don't have enough resources to craft this.")
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
            elif(choice2.upper() == "BRASS"):
                if(metals[1] >= 1 and metals[2] >= 1):
                    print("You make brass.")
                    metals[8] = metals[8] + 1 #Adds new alloy
                    metals[1] = metals[1] - 1 #Takes old Metal
                    metals[2] = metals[2] - 1 #Uses old metal
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
                else:
                    print("You don't have enough resources to craft this.")
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
            elif(choice2.upper() == "BRONZE"):
                if(metals[3] >= 1 and inventory[1] >= 1):
                    print("You make bronze.")
                    metals[9] = metals[9] + 1 #Adds new alloy
                    metals[3] = metals[3] - 1 #Takes old Metal
                    metals[1] = metals[1] - 1 #Uses old resource
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
                else:
                    print("You don't have enough resources to craft this.")
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
            elif(choice2.upper() == "SOUL"):
                if(metals[4] >= 1 and inventory[4] >= 1):
                    print("You make soul steel.")
                    metals[9] = metals[9] + 1 #Adds new alloy
                    metals[4] = metals[4] - 1 #Takes old Metal
                    inventory[4] = inventory[4] - 1 #Uses old resource
                    choice2 = input()
                    print("What now?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                else:
                    print("You don't have enough resources to craft this.")
                    print("Which one would you like to make?")
                    print("Options: STEEL, BRASS, BRONZE, SOUL, EXIT")
                    choice2 = input()
            else:
                print("That's not something you can make.")
                print("Options: STEEL, BRASS, BRONZE, STAINLESS, BELL, SOUL, EXIT")
                choice2 = input() #Alloy Production
    def craftWeapons():
        global blueprints
        global weapons
        blueprintBasicAxe = 0
        print("Type a blueprint that you have to craft it, or you can exit. The numbers represent DMG, DEF, LUCK.")
        print("You can make:")
        if "Basic Axe" in blueprints:
            print("Basic Axe -- One Wood, Two Iron -- 2,1,1")
            blueprintBasicAxe = 1 #Check for Basic Axe BP
        else:
            print("You have no blueprints.")
            makeWeapons()
        choice4 = input()
        ans4 = "incorrect"
        while(ans4 == "incorrect"):
            if(choice4.upper() == "EXIT"):
                makeWeapons()
            if(choice4.upper() == "BASIC AXE" and blueprintBasicAxe == 1): #Craft Basic Axe
                if(metals[0] >= 2 and inventory[5] >= 1):
                    print("You make a basic axe.")
                    weapons = []
                    time.sleep(1)
                    weapons.append(useWeapons("Basic Axe", 2, 1, 1)) #Adds new weapon
                    metals[0] = metals[0] - 2 #Takes old Metal
                    inventory[5] = inventory[5] - 1 #Uses old resource
                    ans4 = "correct"
                else:
                        print("You don't have enough resources to craft this.")
                        ans4 = "correct"
            else:
                print("That's not something you can craft.")
                choice4 = input()
        print("What now?")
        makeWeapons()
    def makeWeapons():
        global blueprints
        global metals
        global weapons
        print("You can craft new weapons with the correct blueprints.")
        print("Options: CHECK BLUEPRINTS, CRAFT WEAPONS, EXIT")
        ans3 = "incorrect"
        choice3 = input()
        while(ans3 == "incorrect"):
            if(choice3.upper() == "CHECK BLUEPRINTS"):
                try: #About the jankyiest soloution to this problem.
                    if(blueprints[0] != "placeholder"): #This makes sure that you have some
                        print("You have blueprints for:")
                        for x in blueprints:
                            print(x)
                        print("What now?")
                        print("Options: CHECK BLUEPRINTS, CRAFT WEAPONS, EXIT")
                        choice3 = input()
                except:
                    print("You have no blueprints.")
                    print("What now?")
                    print("Options: CHECK BLUEPRINTS, CRAFT WEAPONS, EXIT")
                    choice3 = input()
            elif(choice3.upper() == "EXIT"):
                choice3 = "correct"
                beginForge()
            elif(choice3.upper() == "CRAFT WEAPONS"):
                craftWeapons()
            else:
                print("That's not something you can do.")
                print("Options: CHECK BLUEPRINTS, CRAFT WEAPONS, EXIT")
    def checkMetals():
        print("You have")
        print("Iron: " + str(metals[0]))
        print("Copper: " + str(metals[1]))
        print("Zinc: " +str(metals[2]))
        print("Tin: " + str(metals[3]))
        print("Lead: " + str(metals[4]))
        print("Nickel: " + str(metals[5]))
        print("Chromium: " + str(metals[6]))
        print("Steel: " + str(metals[7]))
        print("Brass: " + str(metals[8]))
        print("Bronze: " + str(metals[9]))
        print("Soul: " + str(metals[10]))

    while(ans == "incorrect"):
        if(choice.upper() == "MAKE ALLOYS"):
            makeAlloys()
            choice = "correct"
        elif(choice.upper() == "MAKE WEAPONS"):
            makeWeapons()
        elif(choice.upper() == "CHECK METALS"):
            checkMetals()
            print("Options: MAKE ALLOYS, MAKE WEAPONS, CHECK METALS, CHECK INVENTORY, EXIT")
            choice = input()
        elif(choice.upper() == "EXIT"):
            print("You stop forging.")
            mapD3Interior()
        elif(choice.upper() == "CHECK HEALTH"):
           checkHP()
           choice = input()
        elif(choice.upper() == "CHECK TEMP"):
           checkTemp()
           choice = input()
        elif(choice.upper() == "CHECK INVENTORY"):
           checkInventory()
           choice = input()
        else:
            print("That's not something you can do.")
            print("Options: MAKE ALLOYS, MAKE WEAPONS, CHECK METALS, CHECK INVENTORY, EXIT")
            choice = input()



while(1 == 1):#Makes a loop you can break out from. This would end the game.
    Menu()
    startUp()#Begin the story
    break
