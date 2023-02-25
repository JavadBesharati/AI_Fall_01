from __future__ import unicode_literals
from hazm import *
from math import inf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from operator import itemgetter
from arabic_reshaper import reshape
from bidi.algorithm import get_display

######################### observing data format ##############

trainData = pd.read_csv('Dataset/train.csv')
testData = pd.read_csv('Dataset/test.csv')

#print(trainData)
#print(testData)

########### example of using lemmatization and stemming ########

lemmatizer = Lemmatizer()
stemmer = Stemmer()

sampleWords = ['رفتم', 'رفت', 'رفتند', 'رفتی']

#for word in sampleWords :
#    print(lemmatizer.lemmatize(word))
#    print(stemmer.stem(word))
#################################################################

normalizer = Normalizer()
stopWords = stopwords_list()
punctuations = ['(', ')', '"', "'", '.', ',', '،', ':', ';', '؛', '!', '?', '»', '«', '{', '}', ']', '[']

def preprocesser(text) :    
    tmpTxt = []
    #delete numbers
    for letter in text :
        if not letter.isdigit() :
            tmpTxt.append(letter)
    text = ''.join(tmpTxt)
    #using semi space
    text = normalizer.normalize(text)
    words = word_tokenize(text)
    words = [word for word in words if word not in punctuations]
    words = [lemmatizer.lemmatize(word).split('#', 1)[0] for word in words]
    words = [word for word in filter(None, words) if word not in stopWords]
    return words

#print(preprocesser(trainData['content'][0]))

titles, wordsCount = {}, {}
#titles is dictionary that its keys are titles and its values is count of each title
# wordsCount shows count of each word in all data
#wordsCountInTitles shows the count of each word for each title
totalWordsCount, distinctWordsCount = 0, 0
wordsCountInTitles, totalWordsOfTitles, seenWords = {}, {}, {}

def calc_titles_frequency() :
    for _, row in trainData.iterrows() :
        if row.isnull().values.any() :
            continue
        title = row['label']
        if title in titles :
            titles[title] += 1
        else :
            titles[title] = 1

calc_titles_frequency()
#print(titles)

for title in titles.keys() :
    wordsCountInTitles[title] = {}
    totalWordsOfTitles[title] = 0

def calc_words_frequency() :
    global totalWordsCount, distinctWordsCount
    for _, row in trainData.iterrows() :
        if row.isnull().values.any() :
            continue
        title = row['label']
        content = row['content']
        words = preprocesser(content)
        n = len(words)
        totalWordsOfTitles[title] += n
        totalWordsCount += n
        for word in words :
            if word not in seenWords.keys() :
                distinctWordsCount += 1
                seenWords[word] = True
            if word in wordsCountInTitles[title].keys() :
                wordsCountInTitles[title][word] += 1
            else :
                wordsCountInTitles[title][word] = 1
            if word in wordsCount.keys() :
                wordsCount[word] += 1
            else :
                wordsCount[word] = 1

calc_words_frequency()

def draw_plot(title) :
    result = dict(sorted(wordsCountInTitles[title].items(), key = itemgetter(1), reverse=True)[0:6])
    repetitiveWords = list(result.keys())
    repetitiveWords = [get_display(reshape(word)) for word in repetitiveWords]
    plt.bar(repetitiveWords, result.values())
    plt.ylabel('frequency')
    plt.xlabel(f'words appeared in news with title {get_display(reshape(title))}')
    plt.show()

for title in titles.keys() :
    draw_plot(title)

stopWords.append('توانست')
stopWords.append('ایران')

wordsCount = {}
totalWordsCount, distinctWordsCount = 0, 0
wordsCountInTitles, totalWordsOfTitles, seenWords = {}, {}, {}

for title in titles.keys() :
    wordsCountInTitles[title] = {}
    totalWordsOfTitles[title] = 0

calc_words_frequency()

for title in titles.keys() :
    draw_plot(title)

def calc_probabilities(alpha, text) :
    newsCount = len(trainData)
    words = preprocesser(text)
    probabilities = {}
    #the loop below calculates p(c) for each news title (c : news title)
    for title in titles.keys() :
        probabilities[title] = np.log(titles[title] / newsCount)
    # what has been calculated till here is p(c) and we put p(c|x) = p(c) --> In the following to calculate the correct value of 
    #p(c|x), we'll have : p(c|x) = p(c|x) * p(x|c) / p(x)
    #to have easier calculations we use log, so * becomes +
    for word in words :
        for title in titles.keys() :
            if word not in wordsCountInTitles[title] :
                wordsCountInTitles[title][word] = 0
            #if alpha == 0, additive smoothing is off else is on
            if alpha == 0 :
                probabilities[title] += np.log(wordsCountInTitles[title][word] / totalWordsOfTitles[title])
            else :
                probabilities[title] += np.log((wordsCountInTitles[title][word] + alpha) / (totalWordsOfTitles[title] + alpha * distinctWordsCount))
    return probabilities


def predict_title(alpha, text) :    
    probabilities = calc_probabilities(alpha, text)
    title = 'فناوری'
    max_probability = -1 * inf
    for key, value in probabilities.items() :
        if value > max_probability :
            title = key
            max_probability = value
    return title

predictedTitlesWithSmoothing, predictedTitlesWithoutSmoothing = [], []

for _,row in testData.iterrows() :
    if row.isnull().values.any() :
        continue
    predictedTitlesWithSmoothing.append(predict_title(1, row['content']))
    predictedTitlesWithoutSmoothing.append(predict_title(0, row['content']))

testData['predicted titles with smoothing'], testData['predicted titles without smoothing'] = predictedTitlesWithSmoothing, predictedTitlesWithoutSmoothing

correctTitles = testData['label']

def calc_accuracy(predictedTitles) :
    correctPredictionsCount = 0
    for i in range(len(correctTitles)) :
        if predictedTitles[i] == correctTitles[i] :
            correctPredictionsCount += 1
    return correctPredictionsCount / len(correctTitles)

def calc_precision(predictedTitles, label) :
    correctPredictionsCount, allPredictionsCount = 0, 0
    for i in range(len(correctTitles)) :
        if predictedTitles[i] == label :
            allPredictionsCount += 1
            if predictedTitles[i] == correctTitles[i] :
                correctPredictionsCount += 1
    if allPredictionsCount == 0 : return 0
    else : return correctPredictionsCount / allPredictionsCount
        
def calc_recall(predictedTitles, label) :
    correctPredictionsCount, totalPredictionsCount = 0, 0
    for i in range(len(correctTitles)) :
        if correctTitles[i] == label :
            totalPredictionsCount += 1
            if predictedTitles[i] == correctTitles[i] :
                correctPredictionsCount += 1
    if totalPredictionsCount == 0 : return 0
    else : return correctPredictionsCount / totalPredictionsCount

def calc_f1(predictedTitles, label) :
    precision = calc_precision(predictedTitles, label)
    recall = calc_recall(predictedTitles, label)
    if (precision + recall) == 0 : return 0
    else : return (2 * precision * recall) / (precision + recall)

def calc_macro(predictedTitles) :
    f1Score, counter = 0, 0
    for title, _ in titles.items() :
        f1Score += calc_f1(predictedTitles, title)
        counter += 1
    return f1Score / counter

def calc_weighted(predictedTitles) :
    weights, f1 = {}, {}
    for title, _ in titles.items() :
        weights[title] = 0
        f1[title] = calc_f1(predictedTitles, title)
    for title in correctTitles :
        weights[title] += 1
    f1score = 0
    for title, value in f1.items() :
        f1score += value * weights[title]
    return f1score / sum(weights.values())

def print_result(predictions) :
    newsTitles = ['سلامت', 'سیاسی', 'ورزشی', 'فناوری', 'حوادث', 'فرهنگی/هنری']
    precision, recall, f1 = {}, {}, {}
    for title in newsTitles :
        precision[title] = calc_precision(predictions, title)
        recall[title] = calc_recall(predictions, title)
        f1[title] = calc_f1(predictions, title)
    accuracy = calc_accuracy(predictions)
    macro = calc_macro(predictions)
    micro = accuracy
    weighted = calc_weighted(predictions)
    
    print('precision:')
    for item in list(precision.items()) :
        print(item, end = ' ')
    print()    
    print('recall:')
    for item in list(recall.items()) :
        print(item, end = ' ')
    print()
    print('f1:')
    for item in list(f1.items()) :
        print(item, end = ' ')
    print()
    print(f'accuracy: {accuracy}')
    print(f'macro: {macro}')
    print(f'micro: {micro}')
    print(f'weighted: {weighted}')

print(f'results without additive smoothing:')
print_result(predictedTitlesWithoutSmoothing)
print()
print(f'result with additive smoothing:')
print_result(predictedTitlesWithSmoothing)

def print_mistakes() :
    mistakesCount = 0
    for index, row in testData.iterrows() :
        if mistakesCount >= 5 :
            return
        if row.isnull().values.any() :
            continue
        if row['label'] != predictedTitlesWithSmoothing[index] :
            print('########################')
            print('real title :')
            print(row['label'])
            print('predicted title :')
            print(predictedTitlesWithSmoothing[index])
            print(row['content'])
            mistakesCount += 1

print_mistakes()