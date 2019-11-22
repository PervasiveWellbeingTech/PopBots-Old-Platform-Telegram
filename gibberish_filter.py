from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer
import re

# Script determines if input text is english

GIBBERISH_THRESHOLD = .60

# Return percentage of English words in txt input
def pct_English(txt):
    Lem = WordNetLemmatizer()
    txt = txt.split()
    englishCount = 0
    totalCount = 0
    for word in txt:
        totalCount += 1
        word = Lem.lemmatize(word)
        if word in words.words() or word.isnumeric():
            englishCount += 1

    return float(englishCount/totalCount)

def normalizeText(text):
    text = text.lower()
    text = re.sub(r'[.?,!]','',text)
    return text

def isGibberish(txt, threshold = 1):
    txt = normalizeText(txt)
    englishPtg = pct_English(txt)
    print(englishPtg)
    txt = txt.split()
    if len(txt) == 1:
        print("text equal 1")
        if englishPtg < 1:
            return True
    else:
        print("text equal 2")
        if englishPtg < threshold:
            return True
    return False


if __name__== "__main__":
    while True:
        text = input("Write text to filter for gibberish. Enter 0 to quit: " + '\n')
        if text == '0':
            break
        elif len(text) == 0:
            print("No input. Try again." + '\n')
            continue
        else:
            text = normalizeText(text)
            #print("---> " + str(pct_English(text)*100) + '% of English words in input.' + '\n')
            if isGibberish(text, GIBBERISH_THRESHOLD):
                print("--->[" + text + "] classified as GIBBERISH" + '\n')
            else:
                print("--->[" + text + "] classified as ENGLISH" + '\n')
