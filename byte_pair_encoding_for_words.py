from os import sep
import nltk
import pickle
from pprint import pprint
from nltk import corpus

unicodeBase = 0xF000
unicodeNum = unicodeBase


# Byte pair encoding for word separation: A simple example

# By Erika Nesse, 2021. MIT License (see LICENSE)

def countLetterBigrams(text):

    text = list(text)
    bigrams = nltk.bigrams(text)
    freq = nltk.FreqDist(bigrams)
    return freq

def letters(text):
    return set(list(text))

def unicodeLetters(text):
    global unicodeBase

    return [letter for letter in letters(text) if ord(letter) >= unicodeBase ]


def nextUnicodeLetter():
    # Using chars from Unicode private area for string substitution
    global unicodeNum
    uChr = chr(unicodeNum)
    unicodeNum = unicodeNum + 1
    return uChr

def rApplyCodes(text, letter, node, nodes, depth=0, ignore_until_depth=None, separate_at_depth=None, left_separator = ' ', right_separator = ' '):

    if len(unicodeLetters(text)) <= 0:
        print('stopped at depth ', depth)
        return text
    nodeleft = node['members'][0][0]
    noderight = node['members'][0][1]
    subst = nodeleft + noderight 

    if depth == 0:
        left_separator = "[ "
        right_separator = " ]\n"
    else:
        left_separator = "< "
        right_separator = " >"

    if (separate_at_depth is None) or  (depth in separate_at_depth) :
        subst = left_separator + subst + right_separator
    text = text.replace(letter, subst)

        

    if nodeleft in nodes:
        text = rApplyCodes(text, nodeleft, nodes[nodeleft], nodes, depth=depth + 1, ignore_until_depth=ignore_until_depth, left_separator=left_separator, right_separator=right_separator, separate_at_depth=separate_at_depth)
    if noderight in nodes:
        text = rApplyCodes(text, noderight, nodes[noderight], nodes, depth=depth + 1, ignore_until_depth=ignore_until_depth,  left_separator=left_separator, right_separator=right_separator, separate_at_depth=separate_at_depth)
    return text


def applyCodes(text, nodes, left_separator = '', right_separator = '', separate_at_depth = None):
    uLetters = unicodeLetters(text)
    for uLetter in uLetters:
        uNode = nodes[uLetter]
        text = rApplyCodes(text, uLetter, uNode, nodes, separate_at_depth=separate_at_depth, left_separator=left_separator, right_separator=right_separator)
    return text

def makeOneReplacement(text, nodes={}):

    replaceChar = nextUnicodeLetter()

    freqDist = countLetterBigrams(text)

    if freqDist.N() == 0:
        return False
    # Find the highest count bigram
    
    maxBigram = freqDist.max()
    bMax = freqDist[maxBigram]
    if bMax < 2:
        return False
    maxBigramString = maxBigram[0] + maxBigram[1]

    # Add replacement character to the nodes list
    newNode = {}
    members = []
    members.append(maxBigram)
    newNode['members'] = members

    newNode['count'] = bMax
    nodes[replaceChar] = newNode

    # Do the substitution in the text
    text = text.replace(maxBigramString, replaceChar)
    return text

def buildModel(text):
    nodes = {}
    for i in range(0, 5000):

        # Find the frequency of bigrams (including unicode codes) in string
        ans = makeOneReplacement(text, nodes)
        if not ans:
            break
        text = ans

    return nodes, text

def saveModel(model, encoded_text, model_name):
    with open('models/' + model_name + '.pickle', 'wb') as f:
        pickle.dump((model, encoded_text), f, pickle.HIGHEST_PROTOCOL)

def loadModel(model_name):
    with open(model_name + '.pickle', 'rb') as f:
        model, encoded_text = pickle.load(f)
    return model, encoded_text


def run(model_name, words, build=True, limit=None):
    trim = 9
    if limit is not None:
        words = words[trim:limit + trim]
    plaintext = ''.join(words).lower()
    baseline = ' '.join(words)


    print(baseline[0:100])
    if build:
        model, encoded_text = buildModel(plaintext)
        saveModel(model, encoded_text, model_name)
        print("model", model_name, "created and saved")
    else:
        model, encoded_text = loadModel(model_name)
        print("model", model_name, "loaded")
    

    result = applyCodes(encoded_text, model, left_separator='[', right_separator = ']', separate_at_depth=[0, 1])
    print(result[0:5000])

if __name__ == "__main__":
    
    model_name = 'austen-persuasion'


    text = corpus.gutenberg.words('austen-persuasion.txt')
    print('words:', len(text))
    word_limit=100000
    print('limit:', word_limit)
    run(model_name, text, build=True, limit=word_limit)