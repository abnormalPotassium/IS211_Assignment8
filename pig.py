import argparse
import random
random.seed(0)

parse = argparse.ArgumentParser()
parse.add_argument('--numPlayers', nargs='?', default = '2')
args = parse.parse_args()
numPlayers = int(args.numPlayers)

if numPlayers < 2:
    print('You can\'t play Pig with only a single player just yet. Would you like to continue with 2 players?\n')
    response = input('Yes or No:  \n').lower()
    if response == 'yes' or response == 'y':
        numPlayers = 2
    else:
        raise SystemExit

class player:
    _registry = []

    def __init__(self, name):
        self._registry.append(self)
        self.name = name
        self.overall_score = 0
        self.turn_total = 0
        self.step_count = 0
        self.previous_roll = 0

    def turn(self):
        self.step_count += 1
        while self.step_count > 0:
            if self.step_count == 1:
                print(f'\nIt\'s your turn {self.name}! Your total score is {self.overall_score} and it\'s the first step of your turn. What would you like your next action to be?\n')
                self.step_count += 1
            elif self.overall_score + self.turn_total >= 100:
                print(f'\n{self.name} you last rolled {self.previous_roll}, your turn total is {self.turn_total} and your total score is {self.overall_score}. You have enough points to win if you hold!\n')
                self.step_count += 1        
            else:
                print(f'\n{self.name} you last rolled {self.previous_roll}, your turn total is {self.turn_total} and your total score is {self.overall_score}. What would you like your next action to be?\n')
                self.step_count += 1
            while True:
                decision = input('Roll with \'r\' or Hold with \'h\':  \n').lower()
                if decision == 'r' or decision == 'r':
                    self.previous_roll = dice.roll()
                    if self.previous_roll == 1:
                        print(f'\nUh oh, you rolled a one {self.name}. There go all {self.turn_total} points down the the drain! This ends your turn.\n')
                        self.reset_turn_total()
                        break
                    else:
                        self.turn_total += self.previous_roll
                        print(f'\nNice! You rolled a {self.previous_roll} bringing you up to {self.turn_total} points!')
                        break
                elif decision == 'h' or decision == 'hold':
                    self.gain_score()
                    break
                elif decision == 'e' or decision == 'exit':
                    raise SystemExit
                else:
                    print(f'\nThat\'s not a valid input {self.name}. Input \'r\' to roll, \'h\' to hold, or \'e\' to exit.\n')


    def gain_score(self):
        print(f'\nYou decided to hold {self.name}. Cashing in your {self.turn_total} turn points and bringing you to {self.overall_score + self.turn_total} overall score! This ends your turn.\n')
        self.overall_score += self.turn_total
        if self.overall_score >= 100:
            print(f'We have a winner! {self.name} is taking home the gold with {self.overall_score} points.\n')
            print('Would you like to play again?\n')
            willingness = input('Yes or No:  \n').lower()
            if willingness == 'yes' or willingness == 'y':
                global newgame
                newgame = True
            else:
                global winner
                winner = True
            self.reset_score()
        else:  
            self.reset_turn_total()

    def reset_turn_total(self):
        self.turn_total = 0
        self.step_count = 0
        self.previous_roll = 0

    def reset_score(self):
        for x in self._registry:
            x.reset_turn_total()
            x.overall_score = 0

class die:
    def __init__(self,sides = 6):
        self.sides = sides

    def roll(self):
        return random.randrange(1,self.sides)

print('\nWelcome to the game of Pig, would you like to play?\n')
consent = input('Yes or No:  \n').lower()

if consent == 'yes' or consent == 'y':
    dice = die()
    winner = False
    newgame = False
    print('\nExcellent! Let\'s begin! First let me know your names.')
    player_names = [input(f'\nPlayer {x} please enter your name:  \n') for x in range(1,numPlayers+1)]
    for y in player_names:
        y = player(y)
    while winner == False:
        for z in player._registry:
            if winner == False and newgame == False:
                z.turn()
            else:
                newgame = False
                break

else:
    print('\nThat\'s alright, anytime you want to play just say yes.')
    raise SystemExit