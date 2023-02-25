from copy import deepcopy
from heapq import heappush, heappop
import time

class Vertex :
    def __init__(self, number, includes_devotee) :
        self.number = number
        self.includes_devotee = includes_devotee
        self.includes_recipe = False

dir_address = 'testcases (easy)/'
file_name = 'input3.txt'

input_file = open(dir_address+file_name, 'r')
input_lines = input_file.readlines()
input_file.close()

first_line = input_lines[0].split(' ')
n, m = map(int, first_line)

adj_vertexes = [[] for i in range(n + 1)]

required_recipes = {}
recipes = []

for i in range(1, m + 1) :
    u, v = map(int, input_lines[i].split(' '))
    adj_vertexes[u].append(v)
    adj_vertexes[v].append(u)

vertexes = [Vertex(i, False) for i in range(n + 1)]

h = int(input_lines[m + 1])
line = input_lines[m + 2].split(' ')
impassable_vertexes = []

for i in range(h) :
    impassable_vertexes.append(int(line[i]))

s = int(input_lines[m + 3])

for i in range(m + 4, m + 4 + s) :
    line = input_lines[i].split(' ')
    p = int(line[0])
    q = int(line[1])

    vertexes[p].includes_devotee = True
    recipe = []
    for i in range(q) :
        recipe.append(int(line[i + 2]))
    required_recipes[p] = recipe

    for i in range(q) :
        if recipe[i] not in recipes :
            recipes.append(recipe[i])
        if vertexes[recipe[i]].includes_recipe != True :
            vertexes[recipe[i]].includes_recipe = True

recipes_count = len(recipes)

seyed_loc = int(input_lines[m + 4 + s])

visited_states = []

q = []

def del_recipe(recipe, required_recipes) :
    for each in list(required_recipes.values()) :
        if recipe in each :
            each.remove(recipe)

def calc_path_time(path) :
    t0 = len(path) - 1
    for v in impassable_vertexes :
        n = path.count(v)
        if n > 1 :
            t0 += ((n * (n + 1)) // 2) - n
    return t0

def check_recipe(v, seen_recipes, required_recipes) :
    if vertexes[v].includes_recipe :
        if v not in seen_recipes :
            seen_recipes.append(v)
            del_recipe(v, required_recipes)

def check_devotee(v, required_recipes, satisfied_devotees) :
    if vertexes[v].includes_devotee :
        if v in list(required_recipes.keys()) :
            if len(required_recipes[v]) == 0 :
                required_recipes.pop(v)
                if v not in satisfied_devotees :
                    satisfied_devotees.append(v)


def astar(alpha, seen_recipes, tmp_required_recipes, satisfied_devotees) :
    if len(q) == 0 :
        check_recipe(seyed_loc, seen_recipes, tmp_required_recipes)
        check_devotee(seyed_loc, tmp_required_recipes, satisfied_devotees)
        visited_states.append((seyed_loc, seen_recipes, satisfied_devotees))
        heappush(q, (alpha * (s - len(satisfied_devotees) + recipes_count - len(seen_recipes)), 
        (seyed_loc, satisfied_devotees, [seyed_loc], seen_recipes, tmp_required_recipes)))
    while q :
        displeased_devotees_count, info = heappop(q)
        curr_v, tmp_satisfied_devotees, tmp_path, tmp_seen_recipes, tmp_required_recipes = info
        for vertex in adj_vertexes[curr_v] :
            path = deepcopy(tmp_path)
            seen_recipes = deepcopy(tmp_seen_recipes)
            satisfied_devotees = deepcopy(tmp_satisfied_devotees)
            required_recipes = {key: list(val) for key, val in tmp_required_recipes.items()}
            path.append(vertex)
            if (vertexes[vertex].includes_devotee and len(list(required_recipes.keys())) == 1 
            and len(seen_recipes) == recipes_count) :
                if vertex in list(required_recipes.keys()) :
                    return path
            check_recipe(vertex, seen_recipes, required_recipes)
            check_devotee(vertex, required_recipes, satisfied_devotees)
            if (vertex, seen_recipes, satisfied_devotees) not in visited_states :
                visited_states.append((vertex, seen_recipes, satisfied_devotees))
                heappush(q, (alpha * (s - len(satisfied_devotees)  + recipes_count - len(seen_recipes))
                + calc_path_time(path), (vertex, satisfied_devotees, path, seen_recipes, required_recipes)))

tmp_required_recipes = {key: list(val) for key, val in required_recipes.items()}
alpha = 4

def print_solution() :
    s_time = time.time()
    path = astar(alpha, [], tmp_required_recipes, [])
    e_time = time.time()
    exec_time = e_time - s_time
    file_times = open('astar_times.txt', 'a')
    file_times.write(str(exec_time)+'\n')
    file_times.close()
    path_time = calc_path_time(path)
    l = len(path)
    print('path : ', end = '')
    for i in range(l) :
        if i == l - 1 :
            print(path[i])
        else :
            print(path[i], end = ' -> ')
    print(f'path time = {path_time}')
    print(f'For alpha = {alpha} A* execution time = {exec_time} seconds')
    print(f'visited states count = {len(visited_states)}')

print_solution()
