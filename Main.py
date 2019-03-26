
stateDictionary = {}
tagWordDictionary = {}

statePossibilitiesDictionary = {}
tagWordPossibilitiesDictionary = {}

def main():
    # file = open("metu.txt", "r")
    # lineCounter = 0
    # for counter in file:
    #     lineCounter = lineCounter + 1

    non_blank_count = 0

    with open('metu.txt', encoding="utf8") as f:
        for line in f:
            if line.strip():
                non_blank_count += 1

    print(non_blank_count)

    file = open("metu.txt", "r", encoding="utf8")
    for index in range(0, int(non_blank_count * 0.7)):
        line = file.readline()

        words = line.split()
        words.insert(0, '<s>/Start')
        words.append('<e>/Stop')

        previousState = ''

        for wordTagPair in words:
            word = wordTagPair.split("/")
            currentState = word[1]

            ###  State Model Building Part  ###
            if previousState == '':
                previousState = currentState
            else:
                if previousState in stateDictionary.keys():
                    if currentState in stateDictionary[previousState]:
                        stateDictionary[previousState][currentState] += 1
                    else:
                        stateDictionary[previousState][currentState] = 1
                else:
                    stateDictionary[previousState] = {}
                    stateDictionary[previousState][currentState] = 1
            ###  State Model Building Part  ###

            ###  Tag-Word Dictionary Building Part  ###
            currentWord = word[0].lower()

            if currentState in tagWordDictionary.keys():
                if currentWord in tagWordDictionary[currentState]:
                    tagWordDictionary[currentState][currentWord] += 1
                else:
                    tagWordDictionary[currentState][currentWord] = 1
            else:
                tagWordDictionary[currentState] = {}
                tagWordDictionary[currentState][currentWord] = 1
            ###  Tag-Word Dictionary Building Part  ###

            previousState = currentState

            ###  State Model Dictionary Possibilities Calculating Part  ###
            # bu kısımda hata var buraya bak
            for key in stateDictionary:
                totalValueOfTheState = 0
                for state2 in stateDictionary[key]:
                    totalValueOfTheState += 1
                for state2 in stateDictionary[key]:
                    statePossibilitiesDictionary[key][state2] = stateDictionary[key][state2] / totalValueOfTheState
            ###  State Model Dictionary Possibilities Calculating Part  ###

            print(statePossibilitiesDictionary)

#    print(stateDictionary)
#    print(tagWordDictionary)


            # print(wordTagPair)

main()
