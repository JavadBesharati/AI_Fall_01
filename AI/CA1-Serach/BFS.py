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

q = []

def BFS() :
    global required_recipes
    q.append((seyed_loc, 1, [], [], [], required_recipes))
    while q :
        curr_v, spent_time, tmp_satisfied_devotees, tmp_path, tmp_seen_recipes, tmp_required_recipes = q.pop(0)
        if (curr_v, tmp_seen_recipes, tmp_satisfied_devotees) not in visited_states :
            visited_states.append((curr_v, tmp_seen_recipes, tmp_satisfied_devotees))
        else :
            continue
        path = deepcopy(tmp_path)
        seen_recipes = deepcopy(tmp_seen_recipes)
        satisfied_devotees = deepcopy(tmp_satisfied_devotees)
        required_recipes = {key: list(val) for key, val in tmp_required_recipes.items()}
        path.append(curr_v)
        
        if curr_v in impassable_vertexes :
            n = path.count(curr_v)
            if n > 1 and spent_time < n :
                q.append((curr_v, spent_time + 1, satisfied_devotees, path, seen_recipes, required_recipes))
                continue

        check_recipe(curr_v, seen_recipes, required_recipes)
        check_devotee(curr_v, required_recipes, satisfied_devotees)

        for vertex in adj_vertexes[curr_v] :
            if (vertex, seen_recipes, satisfied_devotees) not in visited_states :
                if (vertexes[vertex].includes_devotee and len(list(required_recipes.keys())) == 1
                    and len(seen_recipes) == recipes_count) :
                    if vertex in list(required_recipes.keys()) :
                        path.append(vertex)
                        return path
                q.append((vertex, 1, satisfied_devotees, path, seen_recipes, required_recipes))

def print_solution() :
    s_time = time.time()
    path = BFS()
    e_time = time.time()
    exec_time = e_time - s_time
    file_times = open('BFS_times.txt', 'a')
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
    print(f'BFS execution time = {e_time - s_time} seconds')
    print(f'visited states count = {len(visited_states)}')

print_solution()
