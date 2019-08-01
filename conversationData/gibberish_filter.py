from nltk.corpus import words
import re

GIBBERISH_THRESHOLD = .60

def pct_English(txt):
    txt = txt.split()

    englishCount = 0
    totalCount = 0
    for word in txt:
        totalCount += 1
        if word in words.words():
            englishCount += 1

    return float(englishCount/totalCount)


def isGibberish(txt):
    englishPtg = pct_English(txt)
    txt = txt.split()
    if len(txt) == 1:
        if englishPtg < 1:
            return True
    else:
        if englishPtg < GIBBERISH_THRESHOLD:
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
            text = text.lower()
            text = re.sub(r'[.?,!]','',text)
            #print("---> " + str(pct_English(text)*100) + '% of English words in input.' + '\n')

            if isGibberish(text):
                print("--->[" + text + "] classified as GIBBERISH" + '\n')
            else:
                print("--->[" + text + "] classified as ENGLISH" + '\n')
