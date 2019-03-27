
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
                        stateDictionary[previousState]["totalValueOfTheState"] += 1
                        stateDictionary[previousState][currentState] += 1
                    else:
                        stateDictionary[previousState]["totalValueOfTheState"] += 1
                        stateDictionary[previousState][currentState] = 1
                else:
                    stateDictionary[previousState] = {}
                    stateDictionary[previousState]["totalValueOfTheState"] = 1
                    stateDictionary[previousState][currentState] = 1
            ###  State Model Building Part  ###

            ###  Tag-Word Dictionary Building Part  ###
            currentWord = word[0].lower()

            if currentState in tagWordDictionary.keys():
                if currentWord in tagWordDictionary[currentState]:
                    tagWordDictionary[currentState]["totalValueOfTheState"] += 1
                    tagWordDictionary[currentState][currentWord] += 1
                else:
                    tagWordDictionary[currentState]["totalValueOfTheState"] += 1
                    tagWordDictionary[currentState][currentWord] = 1
            else:
                tagWordDictionary[currentState] = {}
                tagWordDictionary[currentState]["totalValueOfTheState"] = 1
                tagWordDictionary[currentState][currentWord] = 1
            ###  Tag-Word Dictionary Building Part  ###

            previousState = currentState
    ###  End of the reading of the file  ###

    ###  State Model Dictionary Possibilities Calculating Part  ###
    for key in stateDictionary:
        statePossibilitiesDictionary[key] = {}
        for crt in stateDictionary[key]:
            if crt != "totalValueOfTheState":
                statePossibilitiesDictionary[key][crt] = stateDictionary[key][crt] / stateDictionary[key]["totalValueOfTheState"]
    ###  State Model Dictionary Possibilities Calculating Part  ###


    ###  Tag-Word Model Dictionary Possibilities Calculating Part  ###
    for key in tagWordDictionary:
        tagWordPossibilitiesDictionary[key] = {}
        for wrd in tagWordDictionary[key]:
            if wrd != "totalValueOfTheState":
                tagWordPossibilitiesDictionary[key][wrd] = tagWordDictionary[key][wrd] / tagWordDictionary[key]["totalValueOfTheState"]
    ###  Tag-Word Model Dictionary Possibilities Calculating Part  ###

    ###  State Model Dictionary Possibilities (Transition Probability) Printing  ###
    for key in statePossibilitiesDictionary:
        print(key)
        print(statePossibilitiesDictionary[key])
    ###  State Model Dictionary Possibilities (Transition Probability) Printing  ###

    ###  Tag-Word Dictionary Possibilities (Emission Probability) Printing  ###
    # for key in tagWordDictionary:
    #     print(key)
    #     print(tagWordPossibilitiesDictionary[key])
    ###  Tag-Word Dictionary Possibilities (Emission Probability) Printing  ###

    # print(stateDictionary)
    # print(tagWordDictionary)


            # print(wordTagPair)

main()
