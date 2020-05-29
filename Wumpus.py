# Wumpus.py
# Conversaion of WUMPUS.PAS from Apple Pascal Games

from random import randint

# Wumpus constants
MAX_ROOMS = 20
MAX_BATS = 2
MAX_PITS = 2
NUMBER_OF_ARROWS = 7
PROMPT = ">"
TUNNELS_PER_ROOM = 3
MOVE = "M"
QUIT = "Q"
SHOOT = "S"
HELP = "?"

def do_instructions():
    print("\n")
    print("Your mission, should you desire to accept it, is to hunt for the")
    print("Wumpus in his cave. To succeed, you must shoot it with one of your")
    print(NUMBER_OF_ARROWS,"arrows. If you shoot into a room which is not directly connected to")
    print("yours, the arrow will bounce to one of the rooms that does connect.")
    print("The bats in the cave may pick you up and place you in a different")
    print("room. If you enter a room which has a pit, you will fall into it.")
    print("If the wumpus finds you or you run out of arrows, you lose.")

def ask_instructions():
    answer = input("Do you want instructions? ")
    while (answer.upper() != "Y" and answer.upper() != "N"):
        print("Please answer yes or no")
        answer = input("Would you like instructions? ")
    
    if (answer.upper() == "Y"):
        do_instructions()
    
# add_tiunnel
# make a tunnel connection between two rooms

def add_tunnel(orig, dest):
    global cave
    cave[orig].append(dest)
    cave[dest].append(orig)

# make_maze
# makes a reasonably random maze. for each room tries to make 3 new tunnels.
# if a tunnel already exists in that direction, another digging that way is
# not made.

def make_maze():
    for current_room in range(2,MAX_ROOMS+1):
        add_tunnel(current_room, current_room-1)
    for current_room in range(3,MAX_ROOMS+1):
        new_tunnel = randint(1,current_room-1)
        if (new_tunnel not in cave[current_room]):
            add_tunnel(current_room, new_tunnel)

# describe
# give a description of the current room ( player ). tell player if the
# wumpus, bats or a pit is nearby.

def describe():
    print("\n")
    print("You are in room", player)
    print("There are tunnels leadinng to rooms", end=" ")
    for i in range(1,MAX_ROOMS+1):
        if i in cave[player]:
            print(i, end=" ")
    print("\n")
    if (player in cave[wumpus]) or (len(set(cave[player]).intersection(set(cave[wumpus]))) != 0):
        print("I smell a Wumpus")
    if (len(set(cave[player]).intersection(set(bats))) != 0):
        print("I hear bats")
    if (len(set(cave[player]).intersection(set(pits))) != 0):
        print("I feel a draft")

# command
# returns the single character that signifies what is to be done

def command():
    describe()
    ch = ""
    while (ch.upper() not in commandset):
        ch = input(str(PROMPT)+" ")
        if (ch.upper() not in commandset):
            print("Type ? for instructions.")
    return ch.upper()

# checkwump
# move the wumpus and see if it went to the same room as the player,
# if so he's dead.

def checkwump():
    global wumpus, killed
    new_wump_room = randint(1,MAX_ROOMS)
    if (new_wump_room in cave[wumpus]):
        wumpus = new_wump_room
    if (wumpus == player):
        print("Look Out!! The Wumpus got you")
        print("Better luck next time.")
        killed = True

# checkbats
# if the player is in a room with bats they will pick him up and move him to
# another room (which will not have bats in it).

def checkbats():
    global player
    if (player in bats):
        while (player in bats+pits or player == wumpus):
            player = randint(1,MAX_ROOMS)
        print("A superbat picked you up and carried you off")

# checkpits
# determines if the player fell into a pit

def checkpits():
    global killed
    if not killed and (player in pits):
        print("Don't do that!! Too late, you fell into a pit.")
        print("You should be more careful")
        killed = True

# randroom
# returns a random room number in the range limited by the set argument.

def randroom(limitedto):
    apossibility = 0
    while (apossibility not in limitedto):
        apossibility = randint(1,MAX_ROOMS)
    return apossibility

# doshoot
# player tries to shoot the wumpus by listing the rooms that he wants to
# shoot through. if the rooms do not match the list, the arrow bounces
# randomly to a connecting tunnel.

def doshoot():
    global killed, wumpuskilled, arrowsleft
    lastroom = player
    nextroom = input("Where ")
    while (nextroom and not killed and not wumpuskilled):
        nextroom = int(nextroom)
        if (wumpus == nextroom and nextroom in cave[lastroom]):
            wumpuskilled = True
        elif (player == nextroom):
            killed = True
        elif (nextroom not in cave[lastroom]):
            nextroom = randroom(cave[lastroom])
        lastroom = nextroom
        nextroom = input("Where (or ENTER to fire) ")
    arrowsleft -= 1
    if killed:
        print("You klutz! You just shot yourself.")
    elif wumpuskilled:
        print("'Congratulations! You slew the fearsome Wumpus.")
    elif (arrowsleft == 0):
        print("You ran out of arrows.")

# domove
# player's move, must be to an adjacent room

def domove():
    global player
    dest = input("To ")
    dest = int(dest) if dest else None
    if (dest not in list(range(1,MAX_ROOMS+1))):
        print("There is no room #", dest)
    elif (dest not in cave[player]):
        print("I see no tunnel to room #", dest)
    else:
        player = dest
    checkbats()
    checkwump()
    checkpits()

# doquit
# asks if the player really wants to quit

def doquit():
    global quitting
    print("\n")
    answer = input("Do you really want to quit now? ")
    quitting = answer in ["Y", "y"]

# doaturn
# does a turn by getting the users input and executing the selected function

def doaturn(action):
    {
        MOVE:   domove,
        SHOOT:  doshoot,
        QUIT:   doquit,
        HELP:   do_instructions,
    }.get(action)()

# gameover
# returns true if the game is over

def gameover():
    gameover = quitting or killed or wumpuskilled or (arrowsleft == 0)
    return gameover

# initialize
# generates a random maze and the positions of the player, wumpus,and bats.
# make sure that the player doesn't start with the wumpus.

def initialize():
    global cave, bats, pits, wumpus, player, quitting, killed, wumpuskilled, arrowsleft, commandset
    cave = [[] for i in range(MAX_ROOMS + 1)]
    bats = []
    pits = []
    make_maze()
    wumpus = randint(1,MAX_ROOMS)
    for i in range(1,MAX_BATS+1):
        bats = bats + [randint(1,MAX_ROOMS)]
    for i in range(1,MAX_PITS+1):
        pits = pits + [randint(1,MAX_ROOMS)]
    while True:
        player = randint(1,MAX_ROOMS)
        if (player != wumpus) and (player not in pits) and (player not in bats):
            break
    quitting = False
    killed = False
    wumpuskilled = False
    arrowsleft = NUMBER_OF_ARROWS
    commandset = [MOVE, SHOOT, QUIT, HELP]

print("Welcome to Wumpus!!")
ask_instructions()
initialize()
while (not gameover()):
    doaturn(command())