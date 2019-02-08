def Generator(s, n):
    '''
    This function generates n overlaping grams for a word
    Input: String s; Int n
    '''
    grams = []
    for i in range(0, len(s) - n + 1):
        gram = s[i:i + n]
        grams.append(gram)
    return grams


def ReadFile(n):
    # a dictonary with words and their n-grams
    # key: word, value: ngrams
    words = {}
    with open('/pine/scr/j/i/jiaming/homework/enwiktionary.a.list', 'r') as f:
        for line in f:
            line = line.strip()
            words[line] = Generator(line, n)
    return words


def FindSimilar(word, word_dict, n):
    '''
    This function generates similarity for each input word
    Input: String word, the word dictionary
    '''

    wordsimilarity = {}

    # the word may or may not exist in the dictionary
    if word in word_dict.keys():
        word_grams = word_dict[word]
    else:
        word_grams = Generator(word, n)

    for k, v in word_dict.items():
        # exclude itself
        if k != word:
            candidate_grams = v
            # calculate the Jaccard similarity
            s1 = set(word_grams)
            s2 = set(candidate_grams)
            if len(s1.union(s2)) != 0:
                similarity = len(s1.intersection(s2)) / len(s1.union(s2))
            else:
                similarity = 0
            wordsimilarity[k] = similarity

    return wordsimilarity


def main():

    for i in range(2, 6):

        # generate a dictionary with all the words and its ngrams
        word_dict = ReadFile(i)

        file = open("/pine/scr/j/i/jiaming/homework/output.txt", 'a')
        file.write("Results of {} grams \n".format(i))

        l = ['abreviation', 'abstrictiveness', 'accanthopterigious', 'artiﬁtial inteligwnse', 'agglumetation']
        for word in l:
            # compute the similarities with other words
            neighbours = FindSimilar(word, word_dict, i)
            results = sorted(neighbours.items(), reverse=True, key=lambda x: x[1])[:10]
            # get the top 10
            for j in range(len(results)):
                result = "The No.{} similar word of {} is {} with a similarity of {} \n".format(j + 1, word, results[j][0], results[j][1])
                file.write(result)


if __name__ == "__main__":
    main()
