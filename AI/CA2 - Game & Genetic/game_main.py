import turtle
import math
import random
from time import sleep
from sys import argv
from copy import deepcopy
import time

class Sim:
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False
    win_score = 100
    lose_score = -100
    equal_score = 0

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        

        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)

    def enemy(self):
        return random.choice(self.available_moves)

                
    def _evaluate(self, available_choices, player_turn, red_choices, blue_choices):
        score = 0
        if player_turn == 'red' :
            for choice in available_choices :
                #tmp_choices = deepcopy(blue_choices)
                tmp_choices = deepcopy(red_choices)
                tmp_choices.append(choice)
                #result = self.gameover(red_choices, tmp_choices)
                result = self.gameover(tmp_choices, blue_choices)
                if  result == 'red' : score += 5
                elif result == 'blue' : score -= 5
        if player_turn == 'blue' :
            for choice in available_choices :
                #tmp_choices = deepcopy(red_choices)
                tmp_choices = deepcopy(blue_choices)
                tmp_choices.append(choice)
                #result = self.gameover(tmp_choices, blue_choices)
                result = self.gameover(red_choices, tmp_choices)
                if  result == 'red' : score += 5
                elif result == 'blue' : score -= 5
        return score

    def minimax(self, depth, player_turn, curr_choice, red_choices, blue_choices, available_choices, best_choices, alpha, beta):
        result = self.gameover(red_choices, blue_choices)
        if result == 'red' :
            return math.inf
        elif result == 'blue' :
            return -math.inf

        if depth <= 0 :
            return self._evaluate(available_choices, player_turn, red_choices, blue_choices)

        if player_turn == 'red' :
            best_choice, max_value = curr_choice, -math.inf
            for i in range(len(available_choices)) :
                tmp_available_choices = deepcopy(available_choices)
                tmp_red_choices = deepcopy(red_choices)
                curr_choice = tmp_available_choices.pop(i)
                tmp_red_choices.append(curr_choice)
                tmp_max = self.minimax(depth - 1, 'blue', curr_choice, tmp_red_choices,
                blue_choices, tmp_available_choices, best_choices, alpha, beta)
                if tmp_max > max_value :
                    best_choice, max_value = curr_choice, tmp_max
                    alpha = max(alpha, max_value)
                    if self.prune and alpha >= beta : break
            best_choices.clear()
            best_choices.append(best_choice)
            return max_value
        elif player_turn == 'blue' :
            min_value = math.inf
            for i in range(len(available_choices)) :
                tmp_available_choices = deepcopy(available_choices)
                tmp_blue_choices = deepcopy(blue_choices)
                curr_choice = tmp_available_choices.pop(i)
                tmp_blue_choices.append(curr_choice)
                tmp_min = self.minimax(depth - 1, 'red', curr_choice, red_choices,
                tmp_blue_choices, tmp_available_choices, best_choices, alpha, beta)
                if tmp_min < min_value :
                    min_value = tmp_min
                    beta = min(beta, min_value)
                    if self.prune and beta <= alpha :
                        break
            return min_value
        

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                best_choices = []
                self.minimax(self.minimax_depth, self.turn, self.available_moves[0],
                self.red, self.blue, self.available_moves, best_choices, -math.inf, math.inf)
                selection = best_choices[0]
                if selection[1] < selection[0] :
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)

            if self.turn == 'red' :
                self.turn = 'blue'
            else :
                self.turn = 'red'
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3 and len(b) < 3 :
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":

    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    results = {"red": 0, "blue": 0}
    s_time = time.time()
    for i in range(1):
        print(i)
        results[game.play()] += 1
    e_time = time.time()
        
    print(results)
    print(f'execution time = {e_time - s_time} seconds')
