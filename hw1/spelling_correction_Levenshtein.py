def LevenshteinSimilarity(s, t):
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    distance = v1[len(t)]
    similarity = 1 / distance
    return similarity


def ReadFile():
    # a list of all the words
    words = []
    with open('/pine/scr/j/i/jiaming/homework/enwiktionary.a.list', 'r') as f:
        for line in f:
            line = line.strip()
            words.append(line)
    return words


def FindSimilar(word, words):
    '''
    This function generates similar words for each input word
    Input: String word
    '''

    wordsimilarity = {}

    for i in words:
        # exclude itself
        if i != word:
            similarity = LevenshteinSimilarity(i, word)
            wordsimilarity[i] = similarity

    return wordsimilarity


def main():

    wordlist = ReadFile()

    file = open("/pine/scr/j/i/jiaming/homework/output.txt", 'a')
    file.write("Results of Levenshtei Distance\n")

    l = ['abreviation', 'abstrictiveness', 'accanthopterigious', 'artiﬁtial inteligwnse', 'agglumetation']
    for word in l:
        # compute the similarities with other words
        neighbours = FindSimilar(word, wordlist)
        results = sorted(neighbours.items(), reverse=True, key=lambda x: x[1])[:10]
        # get the top 10
        for j in range(len(results)):
            result = "The No.{} similar word of {} is {} with a similarity of {} \n".format(j + 1, word, results[j][0], results[j][1])
            file.write(result)


if __name__ == "__main__":
    main()
