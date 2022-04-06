#  Charlie Schuck! SP'22
#  COSC 410 Artificial Intelligence with Dr. Simon
#  SPAM Detector (from text file input) using a Naive Bayesian Classifier.
#  Note: The text file must be titled: 'SMSSpamCollection.txt' -- AS A .TXT
#  and it must be contained in the same dir as this program.

import re


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Node:
    def __init__(self, word):
        self.word = word
        self.probability = 0
        self.SCount = 0
        self.HCount = 0

    def updateSPAMProbability(self):
        self.probability = self.SCount / (self.SCount + self.HCount)

    def getTOTProbability(self, x):  # probability of seeing the term
        return (self.SCount + self.HCount) / x

    def updateSCount(self):
        self.SCount += 1

    def updateHCount(self):
        self.HCount += 1

    def __str__(self):
        return "{" + self.word + ": appearances: " + str(self.SCount + self.HCount) + "\n" + "probability: " + str(
            self.probability) + "\nSPAM appearances: " + str(self.SCount) + "\nHAM appearances: " + str(
            self.HCount) + "}"


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def output(cHAM, cSPAM, fHAM, fSPAM, tHAM, tSPAM):
    print("Percentage of HAM messages correctly marked HAM: " + str((cHAM / tHAM)))
    print("Percentage of SPAM messages correctly marked SPAM: " + str((cSPAM / tSPAM)))
    print("Percentage of HAM messages incorrectly marked SPAM: " + str((fSPAM / tHAM)))
    print("*NUMBER* of SPAM messages that were incorrectly marked HAM, as assignment specified: " + str(fHAM))

    print("for your convenience, percentage of SPAM messages that were incorrectly marked HAM: " + str((fHAM / tSPAM)))


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test(data, p_spam, count):
    c_ham = 0  # correctly marked HAM
    c_spam = 0  # correctly marked SPAM
    f_ham = 0  # falsely marked HAM
    f_spam = 0  # falsely marked SPAM

    t_ham = 0
    t_spam = 0

    for row in data:
        predicted_spam_probability = 0

        if row[:4] == 'spam':
            t_spam += 1
        else:
            t_ham += 1

        for key in keyNodes:
            if row.find(key.word) != -1:
                predicted_spam_probability += (key.probability * p_spam) / (key.getTOTProbability(count))

        if predicted_spam_probability > 0.5:

            if row[:4] == 'spam':
                c_spam += 1
            else:
                f_spam += 1
        else:

            if row[:4] == 'spam':
                f_ham += 1
            else:
                c_ham += 1
        #  print(str(predicted_spam_probability) + " : " + row[:4])

    output(c_ham, c_spam, f_ham, f_spam, t_ham, t_spam)


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

keywords = ['call', 'claim', 'come', 'free', 'i', 'me', 'my', 'prize', 'so', 'won']

keyNodes = []
for word in keywords:
    keyNodes.append(Node(word))  # "Put that thing right back where it came from or so help me!"

file = open('SMSSpamCollection.txt', 'r')
data = file.readlines()
lineCount = 0
normalizedData = []

for line in data:
    lineCount += 1
    inComing = line.lower()
    inComing = re.sub(r'[\s\W]', ' ', inComing)
    normalizedData.append(inComing)

#  since this isn't a dataframe, and really doesn't need to be, I'm just going to split into test and train sets the lazy way.

trainNum = round(0.90 * lineCount)

trainData = normalizedData[:trainNum]
testData = normalizedData[trainNum:]

#  print(trainData)
trainSpamCount = 0

for line in trainData:
    spamFlag = 0
    if line[:4] == "spam":
        spamFlag = 1
        trainSpamCount += 1
    for node in keyNodes:
        if line.find(node.word) != -1:
            if spamFlag == 1:
                node.updateSCount()
                #  node.updateSCount(line.count(node.word)) -- we really don't care about how many times in each expression, spam or ham, the word appears.. just whether or not it does at all is enough for this project.
            else:
                node.updateHCount()
                #  node.updateHCount(line.count(node.word))

for node in keyNodes:
    node.updateSPAMProbability()
    #  print(node.__str__())


PSpam = trainSpamCount / trainNum

print("---- ---- TRAIN ---- ----")
test(trainData, PSpam, trainNum)

print("---- ---- TEST ---- ----")
test(testData, PSpam, trainNum)
