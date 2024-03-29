import numpy as np
import math
from nltk.stem import PorterStemmer
from TurkishStemmer import TurkishStemmer


ps = TurkishStemmer()


stateDictionary = {}
tagWordDictionary = {}

statePossibilitiesDictionary = {}
tagWordPossibilitiesDictionary = {}


def main():
    vocabularySize = 0
    tagWordVocabularySize = 0
    non_blank_count = 0
    testSetTotalTagCount = 0
    testSetTotalTrueTaggingCounter = 0

    punctuationList = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '"', "'"]

    with open('metu.txt', encoding="utf8") as f:
        for line in f:
            if line.strip():
                non_blank_count += 1

    # print(non_blank_count)

    file = open("metu.txt", "r", encoding="utf8")
    for index in range(0, int(non_blank_count * 0.7)-1):
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
            # currentWord = ps.stem(currentWord)

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

    ###  TASK I  ###
    ###  State Model Dictionary Possibilities Calculating Part  ###
    for key in stateDictionary:
        statePossibilitiesDictionary[key] = {}
        for crt in stateDictionary[key]:
            if crt != "totalValueOfTheState":
                statePossibilitiesDictionary[key][crt] = stateDictionary[key][crt] / stateDictionary[key]["totalValueOfTheState"]
                vocabularySize += 1
    ###  State Model Dictionary Possibilities Calculating Part  ###


    ###  Tag-Word Model Dictionary Possibilities Calculating Part  ###
    for key in tagWordDictionary:
        tagWordPossibilitiesDictionary[key] = {}
        for wrd in tagWordDictionary[key]:
            if wrd != "totalValueOfTheState":
                tagWordPossibilitiesDictionary[key][wrd] = tagWordDictionary[key][wrd] / tagWordDictionary[key]["totalValueOfTheState"]
                tagWordVocabularySize += 1
    ###  Tag-Word Model Dictionary Possibilities Calculating Part  ###
    ###  TASK I  ###


    ###  TASK II  ###
    stateDictionaryKeyCount = len(stateDictionary.keys())
    tagWordDictionaryKeyCount = len(tagWordDictionary.keys())
    puncIndexInMatrix = 0
    for index in range(0, int(non_blank_count * 0.3)+2):
        line = file.readline()
        words = line.split()
        words.append('<e>/Stop')

        trueTags = []


        matrix = [[0 for x in range(len(words)+1)] for y in range(stateDictionaryKeyCount)]

        tempList = list(stateDictionary.keys())
        tempList.remove("Start")
        tempListForStartState = list(stateDictionary["Start"])
        tempListForStartState.remove("totalValueOfTheState")
        # print(tempListForStartState)

        ## Creating matrix structure ##
        for k in range(0, stateDictionaryKeyCount-1):
            matrix[k+1][0] = tempList[k]
            if 'Punc' == tempList[k]:
                puncIndexInMatrix = k+1

        for k in range(0, len(words)):
            word = words[k].split("/")
            word[0] = word[0].lower()
            # word[0] = ps.stem(word[0])
            matrix[0][k+1] = word[0]
            trueTags.append(word[1])
            testSetTotalTagCount += 1
        ## Creating matrix structure ##


        ## For initial probabilities, building first column of the matrix ##
        for k in range(1, stateDictionaryKeyCount):
            if matrix[0][1] not in punctuationList:
                if matrix[k][0] in tempListForStartState:
                    if matrix[0][1] in tagWordDictionary[matrix[k][0]]:
                        matrix[k][1] = [math.log10((1 + stateDictionary["Start"][matrix[k][0]]) / (vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                                   ((1 + tagWordDictionary[matrix[k][0]][matrix[0][1]]) / (tagWordDictionary[matrix[k][0]]["totalValueOfTheState"] + tagWordVocabularySize))), matrix[k][0]]
                    else:
                        matrix[k][1] = [math.log10((1 + stateDictionary["Start"][matrix[k][0]]) / (vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                                   (1 / (tagWordDictionary[matrix[k][0]]["totalValueOfTheState"] + tagWordVocabularySize))), matrix[k][0]]
                else:
                    if matrix[0][1] in tagWordDictionary[matrix[k][0]]:
                        matrix[k][1] = [math.log10(1 / (vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                                   ((1 + tagWordDictionary[matrix[k][0]][matrix[0][1]]) / (tagWordDictionary[matrix[k][0]]["totalValueOfTheState"] + tagWordVocabularySize))), matrix[k][0]]
                    else:
                        matrix[k][1] = [math.log10(1 / (vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                                   (1 / (tagWordDictionary[matrix[k][0]]["totalValueOfTheState"] + tagWordVocabularySize))), matrix[k][0]]
            else:
                if matrix[k][0] in tempListForStartState:
                    if matrix[0][1] in tagWordDictionary[matrix[k][0]]:
                        matrix[k][1] = [math.log10((1 + stateDictionary["Start"][matrix[k][0]]) / (
                                    vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                                   ((1 + tagWordDictionary[matrix[k][0]][matrix[0][1]]) / (
                                                               tagWordDictionary[matrix[k][0]][
                                                                   "totalValueOfTheState"] + tagWordVocabularySize))),
                                        matrix[k][0]]
                    else:
                        matrix[k][1] = [math.log10((1 + stateDictionary["Start"][matrix[k][0]]) / (
                                    vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                                   (1 / (tagWordDictionary[matrix[k][0]][
                                                             "totalValueOfTheState"] + tagWordVocabularySize))),
                                        matrix[k][0]]
                else:
                    if matrix[0][1] in tagWordDictionary[matrix[k][0]]:
                        matrix[k][1] = [
                            math.log10(1 / (vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                       ((1 + tagWordDictionary[matrix[k][0]][matrix[0][1]]) / (
                                                   tagWordDictionary[matrix[k][0]][
                                                       "totalValueOfTheState"] + tagWordVocabularySize))), matrix[k][0]]
                    else:
                        matrix[k][1] = [
                            math.log10(1 / (vocabularySize + stateDictionary["Start"]["totalValueOfTheState"]) *
                                       (1 / (tagWordDictionary[matrix[k][0]][
                                                 "totalValueOfTheState"] + tagWordVocabularySize))), matrix[k][0]]
                matrix[puncIndexInMatrix][1] = [math.log10(1), matrix[puncIndexInMatrix][0]]

        ## For initial probabilities, building first column of the matrix ##

        ## For rest of the matrix cells ##
        for j in range(2, len(words)+1):
            for k in range(1, stateDictionaryKeyCount):
                findMaxArray = []
                pathArray = []
                # print(k, j-1)
                # print(matrix[k][j - 1][0])

                currentPosition = matrix[k][0]
                for t in range(1, stateDictionaryKeyCount):
                    arrangePosition = matrix[t][0]
                    # print(currentPosition, arrangePosition, k, j)
                    if matrix[0][1] not in punctuationList:
                        if currentPosition in stateDictionary[arrangePosition]:
                            if matrix[0][j] in tagWordDictionary[currentPosition]:
                                total = math.log10(((1 + stateDictionary[arrangePosition][currentPosition]) / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * ((1 + tagWordDictionary[currentPosition][matrix[0][j]]) / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize)))\
                                        + (matrix[t][j-1][0])
                            else:
                                total = math.log10(((1 + stateDictionary[arrangePosition][currentPosition]) / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * (1 / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize))) \
                                        + (matrix[t][j - 1][0])
                        else:
                            if matrix[0][j] in tagWordDictionary[currentPosition]:
                                total = math.log10((1 / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * ((1 + tagWordDictionary[currentPosition][matrix[0][j]]) / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize)))\
                                        + (matrix[t][j-1][0])
                            else:
                                total = math.log10((1 / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * (1 / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize))) \
                                        + (matrix[t][j - 1][0])
                    else:
                        if currentPosition in stateDictionary[arrangePosition]:
                            if matrix[0][j] in tagWordDictionary[currentPosition]:
                                total = math.log10(((1 + stateDictionary[arrangePosition][currentPosition]) / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * ((1 + tagWordDictionary[currentPosition][matrix[0][j]]) / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize)))\
                                        + (matrix[t][j-1][0])
                            else:
                                total = math.log10(((1 + stateDictionary[arrangePosition][currentPosition]) / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * (1 / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize))) \
                                        + (matrix[t][j - 1][0])
                        else:
                            if matrix[0][j] in tagWordDictionary[currentPosition]:
                                total = math.log10((1 / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * ((1 + tagWordDictionary[currentPosition][matrix[0][j]]) / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize)))\
                                        + (matrix[t][j-1][0])
                            else:
                                total = math.log10((1 / (stateDictionary[arrangePosition]["totalValueOfTheState"] + vocabularySize)) \
                                        * (1 / (tagWordDictionary[currentPosition]["totalValueOfTheState"] + tagWordVocabularySize))) \
                                        + (matrix[t][j - 1][0])

                    findMaxArray.append(total)
                    pathArray.append(matrix[t][0])
                maxValue = max(findMaxArray)
                maxValueIndex = findMaxArray.index(maxValue)
                matrix[k][j] = [maxValue, pathArray[maxValueIndex]]
                # print(findMaxArray, maxValue, maxValueIndex, matrix[k][j], k, j)
        ## For rest of the matrix cells ##
        path = []
        findMaxArray.clear()
        for t in range(1, stateDictionaryKeyCount):
            findMaxArray.append(matrix[t][len(words)][0])
        maxValue = max(findMaxArray)
        maxValueIndex = findMaxArray.index(maxValue)
        camePath = matrix[maxValueIndex+1][len(words)][1]
        path.insert(0, camePath)

        j = len(words)
        for i in range(len(words)-1, 1, -1):
            index = tempList.index(path[0]) + 1
            path.insert(0, matrix[index][i][1])

        # for i in range(1,len(words)):
        #     print(matrix[0][i], end = ' ')
        # print(path)

        # burayı aç!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        # print(np.matrix(matrix))
        # print(stateDictionary)

        for i in range(0,len(path)-1):
            if path[i] == trueTags[i]:
                testSetTotalTrueTaggingCounter += 1

    ###  TASK II  ###


    ###  TASK III  ###
    print(testSetTotalTrueTaggingCounter/testSetTotalTagCount, testSetTotalTrueTaggingCounter, testSetTotalTagCount)
    ###  TASK III  ###


    # for i in stateDictionary:
    #     print(i, stateDictionary[i]["totalValueOfTheState"])


    ###  State Model Dictionary Possibilities (Transition Probability) Printing  ###
    # for key in statePossibilitiesDictionary:
    #     print(key)
    #     print(statePossibilitiesDictionary[key])
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
