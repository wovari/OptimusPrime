import csv
import sys
import xml.etree.ElementTree as ET

training = open(sys.argv[1])

trainingset = csv.reader(training, delimiter=";")

for row in trainingset:
    id = row[0]
    tree = ET.parse(id + ".xml")
    root = tree.getroot()

    #Here is where a part of the magic happens

test = open(sys.argv[2])

testset = csv.reader(test, delimiter=";")
