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
    text = re.sub(r'[^0-9a-zA-Z ]','',text)
    return text

def isGibberish(txt, threshold = 1, allow_one_word = True):
    txt = normalizeText(txt)
    englishPtg = pct_English(txt)
    print(englishPtg)
    txt = txt.split()
    if allow_one_word and len(txt) == 1:
        if englishPtg < 1:
            return True
    else:
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
