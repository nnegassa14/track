# Sliding 15-Puzzle
import sys
import random
# Queue to queue
from queue import PriorityQueue
import time


# python3
# import queue
# frontier = queue.PriorityQueue()

def isGoal(state):
    return state == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def neighbors(state):
    neighborhood = []

    # find blank position
    i = state.index(16)

    # move blank left?
    if i % 4 != 0:
        newState = state[:i - 1] + [state[i], state[i - 1]] + state[i + 1:]
        neighborhood.append(newState)

    # move blank right?
    if i % 4 != 3:
        newState = state[:i] + [state[i + 1], state[i]] + state[i + 2:]
        neighborhood.append(newState)

    # move blank up?
    if i > 3:
        newState = state[:i - 4] + [state[i]] + state[i - 3:i] + [state[i - 4]] + state[i + 1:]
        neighborhood.append(newState)

    # move blank down?
    if i < 12:
        newState = state[:i] + [state[i + 4]] + state[i + 1:i + 4] + [state[i]] + state[i + 5:]
        neighborhood.append(newState)

    return neighborhood


def print15(state):
    for row in range(4):
        for col in range(4):
            if state[4 * row + col] < 10:
                sys.stdout.write(" ")
            sys.stdout.write(str(state[4 * row + col]))
            sys.stdout.write("\t")
        print("")


def print15s(path):
    for i, state in enumerate(path):
        print("step " + str(i))
        print15(state)
        print("")


# TODO: don't regenerate previously generated states
def scrambler(state, n):
    for step in range(n):
        neighborList = neighbors(state)
        num = len(neighborList)
        nextNeighbor = neighborList[random.randint(0, num - 1)]
        state = nextNeighbor
    return state


def heuristicBad(state):
    return 0


def heuristicMedium(state):
    solution = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    return len([i for i in range(16) if state[i] != solution[i]])


def heuristicGood(state):
    total = 0
    for row in range(4):
        for col in range(4):
            index = 4 * row + col
            correct = index + 1
            incorrect = state[index]
            if incorrect == 16: continue
            incorrectRow = int((incorrect - 1) / 4)
            incorrectCol = (incorrect - 1) % 4
            distance = abs(incorrectRow - row) + abs(incorrectCol - col)
            total += distance
    return total


def stateInDict(state, rankdict):
    rankcheck = rankPerm(state)
    if rankcheck in rankdict:
        return True, rankcheck
    if rankcheck not in rankdict:
        return False, rankcheck


def AStar(S, neighborhoodFn, goalFn, visitFn, heuristicFn):
    global maxTime
    startTime = time.time()
    visited = {}

    frontier = PriorityQueue()
    for s in S:
        frontier.put((0, [s]))
        visited[rankPerm(s)] = 0

    while frontier.qsize() > 0:
        (_, path) = frontier.get()
        node = path[-1]

        # check time
        currentTime = time.time()
        if currentTime - startTime > maxTime:
            return [-1, None]

        if goalFn(node):
            visitFn(path)
            currentTime = time.time()
            return [currentTime - startTime, path]
        else:
            neighborhood = neighborhoodFn(node)
            for neighbor in neighborhood:
                condition, rankdict = stateInDict(neighbor, visited)
                if neighbor not in path:
                    newPath = path + [neighbor]
                    pastCost = len(newPath) - 1
                    futureCost = heuristicFn(neighbor)
                    totalCost = pastCost + futureCost
                    # marker
                    if totalCost > 80:
                        pass
                    else:
                        frontier.put((pastCost, newPath))
                    # if totalCost > 80:
                    #     pass
                    # else:
                    #     visited[rankdict] = pastCost
                    #
                    # frontier.put((pastCost, newPath))

#                     frontier.put((pastCost, newPath))

    return [-1, None]


# rankPerm(perm) returns the rank of permutation perm.
# The rank is done according to Myrvold, Ruskey "Ranking and unranking permutations in linear-time".
# perm should be a 1-based list, such as [1,2,3,4,5].
def rankPerm(perm, inverse=None, m=None):
    # if the parameters are None, then this is the initial call, so set the values
    if inverse == None:
        perm = list(perm)  # make a copy of the perm; this algorithm will sort it
        m = len(perm)
        inverse = [-1] * m
        for i in range(m):
            inverse[perm[i] - 1] = i + 1

    if m == 1:
        return 0
    s = perm[m - 1] - 1
    x = m - 1
    y = inverse[m - 1] - 1
    temp = perm[x]
    perm[x] = perm[y]
    perm[y] = temp
    x = s
    y = m - 1
    temp = inverse[x]
    inverse[x] = inverse[y]
    inverse[y] = temp
    return s + m * rankPerm(perm, inverse, m - 1)


def isSolvable(state):
    # find blank position
    z = state.index(16)

    invs = 0
    for i in range(15):
        if i == z:
            continue
        for j in range(i + 1, 16):
            if j == z:
                continue
            if state[i] > state[j]:
                invs += 1
    # changed i to z and made '/' to floor division '//'
    return (z // 4 + invs) % 2 == 1


def doNothing(path):
    pass


if __name__ == "__main__":
    global maxTime

    solved5 = 0
    solved30 = 0
    solved100 = 0

    maxTime = 100
    numTests = 100

    for test in range(numTests):

        # Make a random state.
        state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        # random.shuffle(state)
        i = random.randint(1, 80)
        state = scrambler(state, i)
        # changed the following to the scrambler, initially the code would not work for randomized states
        # while not isSolvable(state):
        #     random.shuffle(state)
        while not isSolvable(state):
            scrambler(state, 5)

        print("\nRunning test " + str(test + 1) + " out of " + str(numTests))
        print15(state)
        print("has rank " + str(rankPerm(state)))

        [runTime, path] = AStar([state], neighbors, isGoal, doNothing, heuristicGood)
        if runTime == -1:
            print("no solution found")
            continue
        else:
            print("solved in " + str(len(path) - 1) + " moves")
            print("solved in " + str(runTime) + " seconds")

        if runTime <= 101:
            solved100 += 1
        if runTime <= 30:
            solved30 += 1
        if runTime <= 5:
            solved5 += 1

    print("Solved in 5 seconds: " + str(solved5) + "/" + str(numTests))
    print("Solved in 30 seconds: " + str(solved30) + "/" + str(numTests))
    print("Solved in 100 seconds: " + str(solved100) + "/" + str(numTests))
