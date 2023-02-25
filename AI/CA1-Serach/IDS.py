from copy import deepcopy
from heapq import heappush, heappop
import time

class Vertex :
    def __init__(self, number, includes_devotee) :
        self.number = number
        self.includes_devotee = includes_devotee
        self.includes_recipe = False


dir_address = 'testcases (easy)/'
file_name = 'input.txt'

input_file = open(dir_address+file_name, 'r')
input_lines = input_file.readlines()
input_file.close()

first_line = input_lines[0].split(' ')
n, m = map(int, first_line)

adj_vertexes = [[] for i in range(n + 1)]

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

required_recipes = {}
recipes = []

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

solution_paths = []
ans_depth = 0
ans_found = False

visited_states_count = 0

def IDS(curr_v, visited_states, satisfied_devotees, seen_recipes, required_recipes, path, depth, depth_limit) :
    global solution_path, ans_depth, ans_found, visited_states_count

    if ans_found and depth > ans_depth :
        return

    if (vertexes[curr_v].includes_devotee and len(list(required_recipes.keys())) == 1
    and len(seen_recipes) == recipes_count and curr_v in list(required_recipes.keys())) :
        path.append(curr_v)
        solution_paths.append(path)
        ans_depth = depth
        ans_found = True

    if depth > depth_limit :
        visited_states_count += len(visited_states)
        return

    tmp_visited_states = deepcopy(visited_states)
    tmp_satisfied_devotees = deepcopy(satisfied_devotees)
    tmp_seen_recipes = deepcopy(seen_recipes)
    tmp_required_recipes = {key : list(val) for key, val in required_recipes.items()}
    tmp_path = deepcopy(path)

    if (curr_v, tmp_seen_recipes, tmp_satisfied_devotees) not in visited_states :
        tmp_visited_states.append((curr_v, tmp_seen_recipes, tmp_satisfied_devotees))
                
    if vertexes[curr_v].includes_recipe :
        if curr_v not in tmp_seen_recipes :
            tmp_seen_recipes.append(curr_v)
            del_recipe(curr_v, tmp_required_recipes)
        
    if vertexes[curr_v].includes_devotee :
        if curr_v in list(tmp_required_recipes.keys()) :
            if len(tmp_required_recipes[curr_v]) == 0 :
                tmp_required_recipes.pop(curr_v)
                if curr_v not in tmp_satisfied_devotees :
                    tmp_satisfied_devotees.append(curr_v)
    
    tmp_path.append(curr_v)
    for vertex in adj_vertexes[curr_v] :
        if (vertex, tmp_seen_recipes, tmp_satisfied_devotees) not in tmp_visited_states :
            IDS(vertex, tmp_visited_states, tmp_satisfied_devotees, tmp_seen_recipes,
                tmp_required_recipes, tmp_path, depth + 1, depth_limit)

depth_limit = -1

s_time = time.time()

while len(solution_paths) == 0 :
    depth_limit += 1
    IDS(seyed_loc, [], [], [], required_recipes, [], 0, depth_limit)

e_time = time.time()

exec_time = e_time - s_time

path_cost = 10 ** 9
solution_path = []

for path in solution_paths :
    path_time = calc_path_time(path)
    if path_time < path_cost :
        path_cost = path_time
        solution_path = path

def print_solution() :
    l = len(solution_path)
    print('path : ', end = '')
    for i in range(l) :
        if i == l - 1 :
            print(solution_path[i])
        else :
            print(solution_path[i], end = ' -> ')
    print(f'path time = {path_cost}')
    print(f'IDS execution time = {exec_time} seconds')
    print(f'visited states count = {visited_states_count}')

file_times = open('IDS_times.txt', 'a')
file_times.write(str(exec_time)+'\n')
file_times.close()

print_solution()