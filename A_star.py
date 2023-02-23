import heapq
import math
import random
import os

class Jugs:
    def __init__(self, volumns, target, capacities):
        self.volumes = volumns
        self.target = target
        self.capacities = capacities
    
    # heuristic function
    def h(self):
        h = 0
        # if you don't need to pour from infinite jug to reach the target
        if sum(self.volumes) <= self.target:
            # if goal, h(n)=0
            if self.volumes[-1] == self.target:
                return 0
            # if there is water in some jug, pour into infinite jug
            for i in self.volumes:
                if i != 0:
                    h += 1
            # to reach goal, try jugs from large to small
            var = self.target - sum(self.volumes)
            for i in sorted(self.capacities[:-1], reverse=True):
                k = var // i
                var -= k * i
                # fill and pour
                h += 2 * k
            # if simply fill and pour cannot reach goal, add difference * 2
            h += 4 * abs(var)
            h += 0.5 * abs(self.target - self.volumes[-1])
            return h
        else:
            # if to reach goal, you need to pour from infinite jug
            # if goal, h(n)=0
            if self.volumes[-1] == self.target:
                return 0

            hs = []
            # from infinite jug, pour to a jug and decide h(n)
            for i in range(len(self.volumes)-1):
                a = self.pour(-1,i).empty(i)

                if a.volumes[-1] == self.target:
                    return 1
                #print(a.volumes,'++++++++++++++')
                if sum(a.volumes) <= self.target:
                    hs.append(a.h())
                    h = 1 + min(hs)
                    #print(a.volumes, hs)
            if hs == []:
                return abs(self.target - self.volumes[-1]) + abs(self.target - sum(self.volumes))
            return h

    def is_goal(self):
        return self.volumes[-1] == self.target
    
    def __eq__(self, other):
        return self.volumes == other.volumes
    
    # for print()
    def __str__(self):
        return 'Jugs: ' + str(self.volumes)

    # for heap
    def __lt__(self, other):
        return abs(self.target - self.volumes[-1]) + abs(self.target - sum(self.volumes)) < abs(other.target - other.volumes[-1]) + abs(other.target - sum(other.volumes))

    # empty a jug
    def empty(self, jug_index):
        # use list() to create a new list object, avoid changing the original list
        new_volumes = list(self.volumes)
        new_volumes[jug_index] = 0
        # return a Jugs object
        temp = Jugs(new_volumes, self.target, self.capacities)
        return temp

    # fill a jug
    def fill(self, jug_index):
        # cannot fill the infinite jug
        if self.capacities[jug_index] != -1:
            new_volumes = list(self.volumes)
            new_volumes[jug_index] = self.capacities[jug_index]
            temp = Jugs(new_volumes, self.target, self.capacities)
            return temp

    # pour from jug A to jug B
    def pour(self, from_index, to_index):
        # if jug B will not be overflow or jug B is infinite, pour all
        if self.volumes[to_index] + self.volumes[from_index] <= self.capacities[to_index] or self.capacities[to_index] == -1:
            new_volumes = list(self.volumes)
            # volume in B = B + A
            new_volumes[to_index] += new_volumes[from_index]
            # A is empty
            new_volumes[from_index] = 0
        else:
            # if jug B will be overflow, pour part
            new_volumes = list(self.volumes)
            # how much to pour
            quant = self.capacities[to_index] - new_volumes[to_index]
            # B is full
            new_volumes[to_index] = self.capacities[to_index]
            # A = A - part
            new_volumes[from_index] -= quant
        temp = Jugs(new_volumes, self.target, self.capacities)
        return temp

    # Generate all possible next states from current state.
    def get_neighbors(self):
        neighbors = []
        for i in range(len(self.volumes)):
            # if jug i is not empty, it can be emptyed
            if self.volumes[i] > 0:
                neighbors.append(self.empty(i))
            # if jug i is not full and not infinite, it can be filled
            if i != len(self.volumes)-1 and self.volumes[i] < self.capacities[i]:
                neighbors.append(self.fill(i))
            # pour from jug i to jug j
            for j in range(len(self.volumes)):
                if i == j:
                    continue
                # if jug i is not empty and jug j is not full(or j is infinite), can pour from i to j
                if self.volumes[i] > 0 and (self.volumes[j] < self.capacities[j] or self.capacities[j] == -1):
                    neighbors.append(self.pour(i,j))
        return neighbors

def load_file(filename):
    with open(filename, "r") as file:
        # Read the first line of the file and split it by ','
        capacities = list(map(int, file.readline().strip().split(',')))
        # Read the second line of the file and convert it to an integer
        target = int(file.readline().strip())
    return capacities, target

# check if the target can be achieved by calculating GCD
def can_reach(capacities, target):
    capa = capacities[:-1]
    while len(capa) > 1:
        # math.gcd takes 2 parameters, so calculate GCD pair by pair
        n_capa = []
        for i in range(len(capa)//2):
            g = math.gcd(capa[i],capa[i+1])
            # if GCD = 1, target can be achieved
            if g == 1:
                return True
            # store GCD of the pair for further calculation
            n_capa.append(g)
        # if the length is odd, the last number is not calculated, store it in the new list
        if len(capa) % 2 != 0:
            n_capa.append(capa[-1])
        capa = n_capa
    # if target mod GCD(capacities) != 0, target cannot be achieved
    if target % capa[0]!= 0:
        return False
    else:
        return True

def a_star(capacities, target):
    # first check if the goal can be reached
    if not can_reach(capacities, target):
        return -1
    # use heap to get the neighbor with least f(n)
    # stores (f(n),g(n),state--Jugs Object)
    heap = [(0, 0, Jugs([0]*len(capacities), target, capacities))]
    # store all visited states(Jugs Object)
    visited = []
    while heap:
        # get the neighbor with least f(n) as current state
        (fn, cost, state) = heapq.heappop(heap)
        print(cost,state)

        # ensure the current state is never visited
        if state in visited:
            continue
        # clear heap and mark current state as visited
        heap = []
        visited.append(state)
        # if the goal is achieved, return g(n) as total steps
        if state.is_goal():
            return cost
        # get all neighbors and iterate through each neighbor
        for neighbor in state.get_neighbors():
            # check if neighbor is visited
            flag = True
            for i in visited:
                if i == neighbor:
                    flag = False
            if flag:
                # calculate f(n) = h(n) + g(n) and build heap
                #print(cost + 1 + neighbor.h(), cost + 1, neighbor)
                heapq.heappush(heap, (cost + 1 + neighbor.h(), cost + 1, neighbor))
        #print(heap)
    return -1# this is useless

def test(cases):
    testcases = []
    # ([capacities], target, correct answer)
    testcases.append(([1,4,10,15,22],181,20))
    testcases.append(([2,5,6,72],143,7))
    testcases.append(([3,6],2,-1))
    testcases.append(([2],143,-1))
    testcases.append(([2,3,5,19,121,852],11443,36))
    for i in cases:
        capacities = testcases[i][0]
        target = testcases[i][1]
        check = testcases[i][2]

        # sort capacities and add infinite jug
        capacities = sorted(capacities)
        capacities += [-1]

        # solve water jug problem using A*
        ans = a_star(capacities, target)

        # check answer
        if ans == check:
            print(f'Test {i} passed: \n\tcapacities = {testcases[i][0]}, target = {target}, answer = {check}')
        else:
            print(f'Test {i} failed: \n\tcapacities = {testcases[i][0]}, target = {target}, answer = {ans}, correct answer = {check}')

def main():
    
    # test
    cases = [0, 1, 2, 3, 4]
    test(cases)
    return
    

    test_path = './tests/'
    txt_files = [f for f in os.listdir(test_path) if f.endswith('.txt')]
    answers = []
    for i in range(len(txt_files)):
        capacities, target = load_file(test_path + txt_files[i])
        capacities = sorted(capacities)
        capacities += [-1]

        ans = a_star(capacities, target)
        answers.append(ans)
        print(ans)
    return answers

if __name__ == "__main__":
    main()