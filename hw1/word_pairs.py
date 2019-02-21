import re
import math
from string import punctuation

file = open('/pine/scr/j/i/jiaming/homework/question1-output.txt', 'a')

tweets = []
with open('/pine/scr/j/i/jiaming/homework/tweets.txt', 'r') as f:
    for line in f:

        # 1-remove space and newline character
        line = line.strip()

        # 2-remove user names and hashtags
        line = re.sub(r'\@[a-zA-Z0-9_.]+', '', line)
        line = re.sub(r'\#[a-zA-Z0-9_.]+', '', line)
        line = line.strip()

        # 3-remove punctuation marks
        for p in punctuation:
            line = line.replace(p, "")

        # exclude empty line
        if line != "":
            tweets.append(line)


# use a dictionary to store the document frequency of each term
word_df = {}
for tweet in tweets:
    word_list = tweet.split()
    # to set
    s = set(word_list)
    for word in s:
        if word not in word_df:
            word_df[word] = 1
        else:
            word_df[word] += 1


# use a dictionary to store the document frequency of each pair
pair_df = {}
for tweet in tweets:
    word_list = tweet.split()
    word_pairs = []
    if len(word_list) >= 2:
        # construct the list of word pairs
        for i in range(0, len(word_list) - 1):
            wordpair = (word_list[i], word_list[i + 1])
            word_pairs.append(wordpair)
        # to set
        s = set(word_pairs)
        for pair in s:
            if pair not in pair_df:
                pair_df[pair] = 1
            else:
                pair_df[pair] += 1


# compute the mutual information
pair_df_mi = {}
N = len(tweets)
for k, v in pair_df.items():
    wordpair = k
    wordpairfrequency = v
    word1freq = word_df[wordpair[0]]
    word2freq = word_df[wordpair[1]]

    word1 = word1freq
    word2 = word2freq
    notword1 = N - word1
    notword2 = N - word2

    word1_and_word2 = wordpairfrequency
    word1_not_word2 = word1 - wordpairfrequency
    word2_not_word1 = word2 - wordpairfrequency
    not_word1_not_word2 = N - word1_and_word2 - word1_not_word2 - word2_not_word1

    #print(word1, word2, word1_and_word2, word1_not_word2, word2_not_word1, not_word1_not_word2)
    if word1_and_word2 != 0:
        upper_left = (word1_and_word2 / N) * math.log((word1_and_word2 / N) / ((word1 / N) * (word2 / N)))
    else:
        upper_left = 0

    if word1_not_word2 != 0:
        upper_right = (word1_not_word2 / N) * math.log((word1_not_word2 / N) / ((word1 / N) * (notword2 / N)))
    else:
        upper_right = 0

    if word2_not_word1 != 0:
        lower_left = (word2_not_word1 / N) * math.log((word2_not_word1 / N) / ((word2 / N) * (notword1 / N)))
    else:
        lower_left = 0

    if not_word1_not_word2 != 0:
        lower_right = (not_word1_not_word2 / N) * math.log((not_word1_not_word2 / N) / ((notword1 / N) * (notword2 / N)))
    else:
        lower_right = 0

    mi = upper_left + upper_right + lower_left + lower_right
    pair_df_mi[wordpair] = mi


sorted_mi = sorted(pair_df_mi.items(), reverse=True, key=lambda x: x[1])

file.write("Results of MI\n")
for i in range(0, 100):
    result = sorted_mi[i]
    wordpair = result[0]
    similarity = result[1]
    file.write("{}\t\t{}\n".format(wordpair, similarity))

# compute pointwise mutual information
pair_df_pointmi = {}
N = len(tweets)
for k, v in pair_df.items():
    wordpair = k
    wordpairfrequency = v
    word1freq = word_df[wordpair[0]]
    word2freq = word_df[wordpair[1]]
    point_mi = math.log((wordpairfrequency / N) / ((word1freq / N) * (word2freq / N)))
    pair_df_pointmi[wordpair] = point_mi


sorted_pointmi = sorted(pair_df_pointmi.items(), reverse=True, key=lambda x: x[1])
file.write("Results of PMI\n")
for i in range(0, 100):
    result = sorted_pointmi[i]
    wordpair = result[0]
    similarity = result[1]
    file.write("{}\t\t{}\n".format(wordpair, similarity))


# compute the Chi-squre
pair_df_chi = {}
N = len(tweets)
for k, v in pair_df.items():
    wordpair = k
    wordpairfrequency = v
    word1freq = word_df[wordpair[0]]
    word2freq = word_df[wordpair[1]]

    word1 = word1freq
    word2 = word2freq
    notword1 = N - word1
    notword2 = N - word2

    word1_and_word2 = wordpairfrequency
    word1_not_word2 = word1 - wordpairfrequency
    word2_not_word1 = word2 - wordpairfrequency
    not_word1_not_word2 = N - word1_and_word2 - word1_not_word2 - word2_not_word1

    upper_left = (word1_and_word2 - (word1 * word2 / N))**2 / (word1 * word2 / N)
    upper_right = (word1_not_word2 - (word1 * notword2 / N))**2 / (word1 * notword2 / N)
    lower_left = (word2_not_word1 - (word2 * notword1 / N))**2 / (word2 * notword1 / N)
    lower_right = (not_word1_not_word2 - (notword1 * notword2 / N))**2 / (notword1 * notword2 / N)

    chisquare = upper_left + upper_right + lower_left + lower_right
    pair_df_chi[wordpair] = chisquare


sorted_chi = sorted(pair_df_chi.items(), reverse=True, key=lambda x: x[1])

file.write("Results of Chi-square\n")
for i in range(0, 100):
    result = sorted_chi[i]
    wordpair = result[0]
    similarity = result[1]
    file.write("{}\t\t{}\n".format(wordpair, similarity))
