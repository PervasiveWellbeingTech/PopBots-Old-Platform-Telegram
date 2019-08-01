import csv
import re
import os
from gibberish_filter import isGibberish

DATA_FOLDER = "conversationData"
OUTPUT_FILE = "userConvInput.csv"

with open(OUTPUT_FILE, 'w', newline='') as csvFile:
    if not os.path.exists('../' + DATA_FOLDER):
        print("No folder with name " + DATA_FOLDER + " detected")
    fileWriter = csv.writer(csvFile, delimiter = ',')
    fileWriter.writerow(['File', 'User input', 'isGibberish() Output'])

    fileList = os.listdir('../' + DATA_FOLDER)
    for file in fileList:
        # Ignore any file that is not a txt file
        if file[-4:] != ".txt":
            print("Ignoring " + file + " file")
        else:
            # Open file
            openFile = open(file, "r", encoding='utf8')
            for line in openFile:
                if("U:" in line[:3]):
                    line = line[2:]
                    fileWriter.writerow([file, line, str(isGibberish(line))])
