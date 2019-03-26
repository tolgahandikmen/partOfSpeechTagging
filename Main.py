
stateDictionary = {}


def main():
    # file = open("metu.txt", "r")
    # lineCounter = 0
    # for counter in file:
    #     lineCounter = lineCounter + 1

    non_blank_count = 0

    with open('metu.txt',encoding="utf8") as f:
        for line in f:
            if line.strip():
                non_blank_count += 1

    print(non_blank_count)

    file = open("metu.txt", "r",encoding="utf8")
    for index in range(0, int(non_blank_count * 0.7)):
        line = file.readline()

        words = line.split()
        words.insert(0, '<s>/Start')
        words.append('<e>/Stop')

        for wordTagPair in words:
            word = wordTagPair.split("/")
            if word[1] in stateDictionary:



    print(wordTagPair)

main()
