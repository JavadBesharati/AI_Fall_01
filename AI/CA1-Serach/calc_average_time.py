def calc_average_time(file_name) :
    file = open(file_name, 'r')
    input_lines = file.readlines()

    n = len(input_lines)
    s = 0
    for i in range(n) :
        s += float(input_lines[i])
    return s / n

#bfs_average = calc_average_time('BFS_times.txt')
#ids_average = calc_average_time('IDS_times.txt')
astar_average = calc_average_time('astar_times.txt')

#print(f'Average Time for BFS = {bfs_average} seconds')
#print(f'Average Time for IDS = {ids_average} seconds')
print(f'Average Time for A* = {astar_average} seconds')