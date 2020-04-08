# import enchant
adjacencyMatrix = {0: [1, 4, 5], 1: [0, 2, 3, 4, 5], 2: [1, 3, 5, 6, 7], 3: [2, 6, 7],
                  4: [0, 1, 5, 8, 9], 5: [0, 1, 4, 6, 8, 9, 10], 6: [1, 2, 3, 5, 7, 9, 10, 11], 7: [2, 3, 6, 10, 11],
                  8: [4, 5, 9, 12, 13], 9: [4, 5, 8, 10, 12, 13, 14], 10: [5, 6, 7, 9, 11, 13, 14, 15], 11: [6, 7, 10, 14, 15],
                  12: [13, 8, 9], 13: [12, 14, 8, 9, 10], 14: [9, 10, 11, 13, 15], 15: [10, 11, 14]}
scoreMapping = {"A" : 1, "B" : 3, "C": 3, "D" : 2, "E" : 1, "F" : 4, "G" : 2, "H" : 4, "I" : 1, "J" : 8, "K" : 5,
    "L" : 1, "M" : 3, "N" : 1, "O" : 1, "P" : 3, "Q" : 10, "R" : 1, "S" : 1, "T" : 1, "U" : 1, "V" : 4,
    "W" : 4, "X" : 8, "Y" : 4, "Z" : 10}

exampleBlitz = "EMT5Y4AAA3OG2KNE3F2ECE4"
filename = "C:/Users/dprim/PycharmProjects/Downloads/csw15.txt"

def file_read(fname):
    content_array = {}
    with open(fname) as f:
        # Content_list is the list that contains the read lines.
        for line in f:
            content_array[(line[:len(line) - 1])] = 69420
        return content_array
scrabble_dict = (file_read(filename))

# d = enchant.Dict("en_US")
def scoreCalculator(combination, indices, adjacencyMatrixMultiplier):
    totalScore = 0
    totalMultiplier = 1
    for index, tileNum in enumerate(indices):
        numIndex = int(tileNum)
        letter = combination[index]
        multipliers = adjacencyMatrixMultiplier[numIndex]
        if multipliers[0] != 0:
            totalScore += scoreMapping[letter] * multipliers[0]
        else:
            totalScore += scoreMapping[letter]
        if multipliers[1] != 0:
            totalMultiplier *= multipliers[1]
    totalScore *= totalMultiplier
    return totalScore


def adjacencyMatrixMultiplierFinder(tiles):
    adjacencyMatrixMultiplier = {0: [0, 0], 1: [0, 0], 2: [0, 0], 3: [0, 0],
                                 4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [0, 0],
                                 8: [0, 0], 9: [0, 0], 10: [0, 0], 11: [0, 0],
                                 12: [0, 0], 13: [0, 0], 14: [0, 0], 15: [0, 0]}
    tileMatrix = ""
    indexModifier = -1
    for index, letter in enumerate(tiles):
        if letter.isalpha():
            tileMatrix += letter
        else:
            realIndex = index + indexModifier
            if letter == str(2) or letter == str(3):
                adjacencyMatrixMultiplier[realIndex][0] = int(letter)
            else:
                adjacencyMatrixMultiplier[realIndex][1] = int(letter) - 2
            indexModifier -= 1
    return adjacencyMatrixMultiplier, tileMatrix

# Find every possible combination

def dfs(start, visited, path, allPaths):
    visited[start] = True
    path.append(start)
    # print(path)

    allPaths.append(list(path))
    if len(path) < 11:
        for neighbour in adjacencyMatrix[start]:
            if visited[neighbour] == False:
                dfs(neighbour, visited, path, allPaths)
    path.pop()
    visited[start] = False

def findWords(tiles):
    #construct tiles and associate indices with multipliers
    adjacencyMatrixMultiplier, tileMatrix = adjacencyMatrixMultiplierFinder(tiles)

    allWords = {}
    for i in range(16):
        allPaths = []
        path = []  # Array to keep track of visited nodes.
        visited = [False] * 16

        dfs(i, visited, path, allPaths)

        for indices in allPaths:
            #search through every possible combination
            combination = ""
            for index in indices:
                combination += tileMatrix[index]
            #if a legit word is found calculate its value and store the word/value pair in a dictionary
            if (combination in scrabble_dict):
                score = scoreCalculator(combination, indices, adjacencyMatrixMultiplier)
                if combination in allWords:
                    if allWords[combination] < score:
                        allWords[combination] = score
                else:
                    allWords[combination] = score
        # once finished, order the dictionary by value and return it
    return {k: v for k, v in sorted(allWords.items(), key=lambda item: item[1], reverse= True)}

print(findWords(exampleBlitz))


# allPaths = []
# path = []  # Array to keep track of visited nodes.
# visited = [False] * 16
# Driver Code
# adjacencyMatrixMultipler1, tiles = (adjacencyMatrixMultiplierFinder(exampleBlitz))
# dfs(0, visited, path, allPaths)
# print(allPaths)
# print(allPaths)
# print(scoreCalculator("LAPS", "0123", adjacencyMatrixMultipler1))
# print(findWords(exampleBlitz))
