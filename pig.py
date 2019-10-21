import argparse
import random
import time
random.seed(0)

parse = argparse.ArgumentParser()
parse.add_argument('--numPlayersHuman', nargs='?', default = '0')
parse.add_argument('--numPlayersComputer', nargs='?', default = '0')
parse.add_argument('--timed', const= True, nargs='?')
args = parse.parse_args()

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

class computerPlayer(player):

    def strategy(self):
        if self.turn_total >= 25 or self.overall_score + self.turn_total >= 100:
            print(f'{self.name} decides to play it safe and hold')
            return 'h'
        else:
            print(f'{self.name} decides to live a little and roll!')
            return 'r'
    
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
                decision = self.strategy()
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
        
class die:
    def __init__(self,sides = 6):
        self.sides = sides

    def roll(self):
        return random.randrange(1,self.sides)

class game:
    def __init__(self,numPlayersHuman,numPlayersComputer):
        self.numPlayersHuman = numPlayersHuman
        self.numPlayersComputer = numPlayersComputer
        self.numPlayers = self.numPlayersHuman + self.numPlayersComputer

    def run(self):
        self.playercheck()
        self.introduction()
        self.initialization()
        self.game()

    def playercheck(self):
        if self.numPlayers < 2:
            print('You can\'t play Pig with only a single player just yet. Would you like to continue with 2 players?\n')
            response = input('Yes or No:  \n').lower()
            if response == 'yes' or response == 'y':
                self.numPlayersHuman = 2
            else:
                raise SystemExit

    def introduction(self):
        print('\nWelcome to the game of Pig, would you like to play?\n')
        consent = input('Yes or No:  \n').lower()
        if consent != 'yes' and consent != 'y':
            print('\nThat\'s alright, anytime you want to play just say yes.')
            raise SystemExit

    def initialization(self):
        global dice
        global winner
        global newgame
        dice = die()
        winner = False
        newgame = False
        print('\nExcellent! Let\'s begin! First let me know your names.')
        player_names_human = [input(f'\nPlayer {x} please enter your name:  \n') for x in range(1,self.numPlayersHuman+1)]
        player_names_computer = [f'AI#{x}' for x in range(1,self.numPlayersComputer+1)]
        for y in player_names_human:
            y = player(y)
        for y in player_names_computer:
            y = computerPlayer(y)

    def game(self):
        global winner
        global newgame
        while winner == False:
            for z in player._registry:
                if winner == False and newgame == False:
                    z.turn()
                else:
                    newgame = False
                    break

class timedGameProxy(game):
    def game(self):
        global winner
        global newgame
        time_start = time.time()
        while winner == False:
            for z in player._registry:
                if time.time() - time_start > 60:
                    self.timeout()
                elif winner == False and newgame == False:
                    z.turn()
                else:
                    newgame = False
                    break

    def timeout(self):
        global winner
        scores = {z.overall_score:z.name for z in player._registry}
        winner = True
        highest_score = max(scores.keys())
        print(f'Time\'s up! The winner is {scores[highest_score]} with a score of {highest_score}!' )
        raise SystemExit


if args.timed:
    pig = timedGameProxy(int(args.numPlayersHuman),numPlayersComputer = int(args.numPlayersComputer))
else:
    pig = game(int(args.numPlayersHuman),numPlayersComputer = int(args.numPlayersComputer))

if __name__ == '__main__':
    pig.run()