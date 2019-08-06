import csv
import re
import os

DATA_FOLDER = "conversationData"
OUTPUT_FILE = "userConvInput.csv"

with open(OUTPUT_FILE, 'w', newline='') as csvFile:
    if not os.path.exists('../' + DATA_FOLDER):
        print("No folder with name " + DATA_FOLDER + " detected")
    fileWriter = csv.writer(csvFile, delimiter = ',')
    fileWriter.writerow(['File', 'User input', 'Gibberish?'])

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
                    line = line.split("U:")
                    fileWriter.writerow([file, line[1]])
