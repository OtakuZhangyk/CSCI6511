import heapq
#from queue import PriorityQueue

def load_file(filename):
    with open(filename, "r") as file:
        # Read the first line of the file and split it by ','
        capacities = list(map(int, file.readline().strip().split(',')))
        # Read the second line of the file and convert it to an integer
        target = int(file.readline().strip())
    return capacities, target

def heuristic(pitches, target):
    return (target + max(pitches) - 1) // max(pitches)

def a_star(capacities, target):
    heap = [(0, 0, capacities)]
    visited = set(capacities)
    while heap:
        cost, moves, capacities = heapq.heappop(heap)
        if sum(capacities) == target:
            return moves
        for i, p1 in enumerate(capacities):
            for j, p2 in enumerate(capacities):
                if i == j:
                    continue
                new_pitches = list(capacities)
                if p1 + p2 <= target:
                    new_pitches[i] = 0
                    new_pitches[j] = p1 + p2
                else:
                    new_pitches[i] = p1 + p2 - target
                    new_pitches[j] = target
                if tuple(new_pitches) not in visited:
                    heapq.heappush(heap, (cost + 1 + heuristic(new_pitches, target), moves + 1, new_pitches))
                    visited.add(tuple(new_pitches))
    return -1


def main():
    test_files = ['./tests/input.txt',]
    test_results = [0,]
    for i in range(len(test_files)):
        capacities, target = load_file(test_files[i])
        steps = a_star(capacities, target)
        if steps == test_results[i]:
            print(f'{i+1}th test passed')
        else:
            print(f'''{i+1}th test failed:
                \twater pitchers: {capacities}
                \ttarget: {target}
                \tprogram result:{steps}
                \texpected result:{test_results[i]}''')

if __name__ == '__main__':
    main()
