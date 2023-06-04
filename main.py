############################################################
##########################################################
# Coded in Python 3.5.0 -- Will not run in Py2  ####
####################################################
# Needed for the game to function. ##
#####################################
import cmd
import textwrap
import sys
import os
import time
import random
screen_width = 100

################
# Player Setup #
################
class player:
    def __init__(self):
        self.name = ''
        self.feeling = ''
        self.astrological = ''
        self.position = 'ground'
        self.won = False
        self.solves = 0
player1 = player()


#############
# Map Setup    #
#############
"""
You're basically in a cube, trying to solve each side of the cube to "break it open" and escape.
Here's a diagram!
----------------------------------------------------
        North -v      _.-+
                 _.-""     '
             +:""            '
             | \  v Top Side   '
              | \             _.-+
              |  '.       _.-"   |
    West -->  |    \  _.-"       |  <-- East
               |    +"           |
               +    | South->    |
                \   |          .+
                 \  |       .-'
                  \ |    .-'    <-- Ground/Center
                   \| .-'
                    +'
-----------------------------------------------------
You can travel to any adjcent wall, but not across.  The game will tell you there is a gap in space.
Unfolding walls will change this system.
"""

#Sets up constant variables
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = False
SIDE_UP = 'up', 'forward'
SIDE_DOWN = 'down', 'back'
SIDE_LEFT = 'left','east'
SIDE_RIGHT = 'right',;'west'

room_solved = {'up': False, 'north': False, 'ground': False, 'east': False, 'west': False, 'south': False,}

"""
How this works:
dictionary = {
    keys1: {
        keys2: Value
    }
}
"""
cube = {
    'top': {
        DESCRIPTION: "You find yourself standing normally on hill as high as the clouds, strangely.",
        INFO: "Even more strange than standing on clouds is the\nbird that begins speaking to you.\n",
        PUZZLE: "The bird intimidatingly asks:\nI see without eyes. I move without legs.\nWhat is a women? who marries an enemy tribe?'",
        SOLVED: "peaceweaver",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'east',
        SIDE_RIGHT: 'west',
    },
    'north': {
        DESCRIPTION: "You see what looks like a Troll.\n It.. walks up.",
        INFO: " Hrothgar says that at night.",
        PUZZLE: "one can see, what on the mere?",
        SOLVED: "fire",
        SIDE_UP: 'top',
        SIDE_DOWN: 'ground',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    },
    'ground': {
        DESCRIPTION: "You find yourself in a rather scary yet soul-less place.\n All you see is fog and what look like the edge of the earth.",
        INFO: "You walk closer, to notice its water\nHow odd.",
        PUZZLE: "* foot steps coming up behind you*\nYou get pushed in the lough!\nIts horrifying in the water, theres serpents and sea-dragons. Whos else might be lurking in the water?",
        SOLVED: False, #Will work after you solve all other puzzles?
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    },
    'east': {
        DESCRIPTION: "You find yourself in woods, bursting with wildlife\.",
        INFO: "A scruffy hooligan is standing next to a tree.\nHis eyes are as big as they could possibly be, almost as if he doesn't have any eyelids.",
        PUZZLE: "The rough-looking hooligan asks,\n'Verses often divided into two halves separated by a long pause.?'",
        SOLVED: "Caesura",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'ground',
        SIDE_RIGHT: 'top',
    },
    'west': {
        DESCRIPTION: 'The swamps of the land of the Spear-Danes.',
        INFO: 'Where can you find a shaggy fur giant,?.',
        PUZZLE: "Standing at 10-foot-tall & armless\n?",
        SOLVED: "Grendel's cave",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'top',
        SIDE_RIGHT: 'ground',
    },
    'south': {
        DESCRIPTION: "- I am all on my own, Wounded by iron weapons and scarred by swords. I often see the battle. I am tired of fighting.\nI do not expect to be allowed to retire from warfare Before I am completely done for. At the wall of the city, I am knocked about and bitten again and again.",
        INFO: "Hard-edged things made by the blacksmith's hammer attack me. Each time I wait for something worse.",
        PUZZLE: "I have never been able to find a doctor who could make me better Or give me medicine made from herbs instead, the sword gashes all over me grow bigger day and night.",
        SOLVED: "a shield",#Should be your astrological sign.
        SIDE_UP: 'ground',
        SIDE_DOWN: 'top',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    }
}


################
# Title Screen #
################
def title_screen_options():
    #Allows the player to select the menu options, case-insensitive.
    option = input("> ")
    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("quit"):
        sys.exit()
    elif option.lower() == ("help"):
        help_menu()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Invalid command, please try again.")
        option = input("> ")
        if option.lower() == ("play"):
            setup_game()
        elif option.lower() == ("quit"):
            sys.exit()
        elif option.lower() == ("help"):
            help_menu()

def title_screen():
    #Clears the terminal of prior code for a properly formatted title screen.
    os.system('clear')
    #Prints the pretty title.
    print('#' * 45)
    print('#      Welcome To Beowulf Last Battle #')
    print("#      Phillip Jordan Final Project!  #")
    print('#' * 45)
    print("                 .: Play :.                  ")
    print("                 .: Help :.                  ")
    print("                 .: Quit :.                  ")
    title_screen_options()


#############
# Help Menu #
#############
def help_menu():
    print("")
    print('#' * 45)
    print("Written by Phillip Jordan")
    print("Version Final (1.0.2a)")
    print("~" * 45)
    print("Type a command such as 'move' then 'left'")
    print("to nagivate the map of the cube puzzle.\n")
    print("Inputs such as 'look' or 'examine' will")
    print("let you interact with puzzles in rooms.\n")
    print("Puzzles will require various input and ")
    print("possibly answers from outside knowledge.\n")
    print("Please ensure to type in lowercase for ease.\n")
    print('#' * 45)
    print("\n")
    print('#' * 45)
    print("    Please select an option to continue.     ")
    print('#' * 45)
    print("                 .: Play :.                  ")
    print("                 .: Help :.                  ")
    print("                 .: Quit :.                  ")
    title_screen_options()


#################
# Game Handling #
#################
quitgame = 'quit'

def print_location():
    #Makes a pretty picture when printed and prints the cube floor information for the player.
    print('\n' + ('#' * (4 +len(player1.position))))
    print('# ' + player1.position.upper() + ' #')
    print('#' * (4 +len(player1.position)))
    print('\n' + (cube[player1.position][DESCRIPTION]))

def prompt():
    if player1.solves == 5:
        print("Something in the world seems to have changed. Hmm...")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("What would you like to do?")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'inspect', 'examine', 'look', 'search']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
    while action.lower() not in acceptable_actions:
        print("Unknown action command, please try again.\n")
        action = input("> ")
    if action.lower() == quitgame:
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        move(action.lower())
    elif action.lower() in ['inspect', 'examine', 'look', 'search']:
        examine()

def move(myAction):
    askString = "Where would you like to "+myAction+" to?\n> "
    destination = input(askString)
    if destination == 'up':
        move_dest = cube[player1.position][SIDE_UP] #if you are on ground, should say north
        move_player(move_dest)
    elif destination == 'left':
        move_dest = cube[player1.position][SIDE_LEFT]
        move_player(move_dest)
    elif destination == 'right':
        move_dest = cube[player1.position][SIDE_RIGHT]
        move_player(move_dest)
    elif destination == 'down':
        move_dest = cube[player1.position][SIDE_DOWN]
        move_player(move_dest)
    else:
        print("Invalid direction command, try using forward, back, left, or right.\n")
        move(myAction)

def move_player(move_dest):
    print("\nYou have moved to the " + move_dest + ".")
    player1.position = move_dest
    print_location()

def examine():
    if room_solved[player1.position] == False:
        print('\n' + (cube[player1.position][INFO]))
        print((cube[player1.position][PUZZLE]))
        puzzle_answer = input("> ")
        checkpuzzle(puzzle_answer)
    else:
        print("There is nothing new for you to see here.")

def checkpuzzle(puzzle_answer):
    if player1.position == 'ground':
        if player1.solves >= 5:
            endspeech = ("hello again thought i went gonna see you again, somehow, you manage to have escaped!")
            for character in endspeech:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(0.08)
            print("\nCONGRATULATIONS!\nyou get nothing...i lied\nthere no potion\hope you had fun playing though")
            sys.exit()
        else:
            print("Nothing seems to happen still...")
    elif player1.position == 'south':
        if puzzle_answer == (cube[player1.position][SOLVED]):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. lets go!")
            print("\nPuzzles solved: " + str(player1.solves))
        else:
            print("Wrong answer! Try again.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
            examine()
    else:
        if puzzle_answer == (cube[player1.position][SOLVED]):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. Onwards!")
            print("\nPuzzles solved: " + str(player1.solves))
        else:
            print("Wrong answer! Try again.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
            examine()

def main_game_loop():
    total_puzzles = 6
    while player1.won is False:
        #print_location()
        prompt()


################
# Execute Game #
################
def setup_game():
    #Clears the terminal for the game to start.
    os.system('clear')

    #QUESTION NAME: Obtains the player's name.
    question1 = "Hello there, what is your name?\n"
    for character in question1:
        #This will occur throughout the intro code.  It allows the string to be typed gradually - like a typerwriter effect.
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    player1.name = player_name

    #QUESTION FEELING: Obtains the player's feeling.
    question2 = "My dear friend " + player1.name + ", how are you feeling?\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    feeling = input("> ")
    player1.feeling = feeling.lower()

    #Creates the adjective vocabulary for the player's feeling.
    good_adj = ['good', 'great', 'rohit', 'happy', 'aight', 'understanding', 'great', 'alright', 'calm', 'confident', 'not bad', 'courageous', 'peaceful', 'reliable', 'joyous', 'energetic', 'at', 'ease', 'easy', 'lucky', 'k', 'comfortable', 'amazed', 'fortunate', 'optimistic', 'pleased', 'free', 'delighted', 'swag', 'encouraged', 'ok', 'overjoyed', 'impulsive', 'clever', 'interested', 'gleeful', 'free', 'surprised', 'satisfied', 'thankful', 'frisky', 'content', 'receptive', 'important', 'animated', 'quiet', 'okay', 'festive', 'spirited', 'certain', 'kind', 'ecstatic', 'thrilled', 'relaxed', 'satisfied', 'wonderful', 'serene', 'glad', 'free', 'and', 'easy', 'cheerful', 'bright', 'sunny', 'blessed', 'merry', 'reassured', 'elated', '1738', 'love', 'interested', 'positive', 'strong', 'loving']
    hmm_adj = ['idk', 'concerned', 'lakshya', 'eager', 'impulsive', 'considerate', 'affected', 'keen', 'free', 'affectionate', 'fascinated', 'earnest', 'sure', 'sensitive', 'intrigued', 'intent', 'certain', 'tender', 'absorbed', 'anxious', 'rebellious', 'devoted', 'inquisitive', 'inspired', 'unique', 'attracted', 'nosy', 'determined', 'dynamic', 'passionate', 'snoopy', 'excited', 'tenacious', 'admiration', 'engrossed', 'enthusiastic', 'hardy', 'warm', 'curious', 'bold', 'secure', 'touched', 'brave', 'sympathy', 'daring', 'close', 'challenged', 'loved', 'optimistic', 'comforted', 're', 'enforced', 'drawn', 'toward', 'confident', 'hopeful', 'difficult']
    bad_adj = ['bad', 'meh', 'sad', 'hungry', 'unpleasant', 'feelings', 'angry', 'depressed', 'confused', 'helpless', 'irritated', 'lousy', 'upset', 'incapable', 'enraged', 'disappointed', 'doubtful', 'alone', 'hostile', 'discouraged', 'uncertain', 'paralyzed', 'insulting', 'ashamed', 'indecisive', 'fatigued', 'sore', 'powerless', 'perplexed', 'useless', 'annoyed', 'diminished', 'embarrassed', 'inferior', 'upset', 'guilty', 'hesitant', 'vulnerable', 'hateful', 'dissatisfied', 'shy', 'empty', 'unpleasant', 'miserable', 'stupefied', 'forced', 'offensive', 'detestable', 'disillusioned', 'hesitant', 'bitter', 'repugnant', 'unbelieving', 'despair', 'aggressive', 'despicable', 'skeptical', 'frustrated', 'resentful', 'disgusting', 'distrustful', 'distressed', 'inflamed', 'abominable', 'misgiving', 'woeful', 'provoked', 'terrible', 'lost', 'pathetic', 'incensed', 'in', 'despair', 'unsure', 'tragic', 'infuriated', 'sulky', 'uneasy', 'cross', 'bad', 'pessimistic', 'dominated', 'worked', 'up', 'a', 'sense', 'of', 'loss', 'tense', 'boiling', 'fuming', 'indignant', 'indifferent', 'afraid', 'hurt', 'sad', 'insensitive', 'fearful', 'crushed', 'tearful', 'dull', 'terrified', 'tormented', 'sorrowful', 'nonchalant', 'suspicious', 'deprived', 'pained', 'neutral', 'anxious', 'pained', 'grief', 'reserved', 'alarmed', 'tortured', 'anguish', 'weary', 'panic', 'dejected', 'desolate', 'bored', 'nervous', 'rejected', 'desperate', 'preoccupied', 'scared', 'injured', 'pessimistic', 'cold', 'worried', 'offended', 'unhappy', 'disinterested', 'frightened', 'afflicted', 'lonely', 'lifeless', 'timid', 'aching', 'grieved', 'shaky', 'victimized', 'mournful', 'restless', 'heartbroken', 'dismayed', 'doubtful', 'agonized', 'threatened', 'appalled', 'cowardly', 'humiliated', 'quaking', 'wronged', 'menaced', 'alienated', 'wary']

    #Identifies what type of feeling the player is having and gives a related-sounding string.
    if player1.feeling in good_adj:
        feeling_string = "I am glad you feel"
    elif player1.feeling in hmm_adj:
        feeling_string = "that is interesting you feel"
    elif player1.feeling in bad_adj:
        feeling_string = "I am sorry to hear you feel"
    else:
        feeling_string = "I do not know what it is like to feel"

    #Combines all the above parts.
    question3 = "Well then, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    #QUESTION SIGN: Obtains the player's astrological sign for a later puzzle.
    question4 = "Now tell me, what is your astrological sign?\n"
    for character in question4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    #Prints the astrological sign guide for the player.  Also converts text to be case-insensitive, as with most inputs.
    print("#####################################################")
    print("# Please print the proper name to indicate your sign.")
    print("# ♈ Aries (The Ram)")
    print("# ♉ Taurus (The Bull)")
    print("# ♊ Gemini (The Twins)")
    print("# ♋ Cancer (The Crab)")
    print("# ♌ Leo (The Lion)")
    print("# ♍ Virgo (The Virgin)")
    print("# ♎ Libra (The Scales)")
    print("# ♏ Scorpio (The Scorpion)")
    print("# ♐ Sagittarius (Centaur)")
    print("# ♑ Capricorn (The Goat)")
    print("# ♒ Aquarius (The Water Bearer)")
    print("# ♓ Pisces (The Fish)")
    print("#####################################################")
    astrological = input("> ")
    acceptable_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.  Also stores it in class.

    while astrological.lower() not in acceptable_signs:
        print("That is not an acceptable sign, please try again.")
        astrological = input("> ")
    player1.astrological = astrological.lower()

    #Leads the player into the cube puzzle now!
    speech1 = "Ah, " + player1.astrological + ", how interesting. we can use astrology signs to travel back in time,  Well then.\n"
    speech2 = "It seems this is where we must part, " + player1.name + ".\n"
    speech3 = "How unfortunate.\n"
    speech4 = "Oh, you don't know where you are?  Well...\n"
    speech5 = "welcome to Greatland, there will be little puzzles throughout the adventure. Hopefully, you can escape this box and get the venom potion. So can save Beowulf.\n"
    speech6 = "Heh. Heh.. Heh...good luck\n"
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech5:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech6:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.2)
    time.sleep(1)

    os.system('clear')
    print("################################")
    print("# Here begins the adventure... #")
    print("################################\n")
    print("You find yourself in the center of a strange place.\nSeems like you are trapped in a little box.\n")
    print("Every inside face of the box seems to have a different theme.\nHow can you get out of this...\n")
    print("You notice objects standing sideways on the walls.\nDoes gravity not apply?...")
    main_game_loop()


title_screen()
#0 comments on commit c921abf

