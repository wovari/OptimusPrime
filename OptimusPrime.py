import csv
import sys
import random
import xml.etree.ElementTree as ET
import numpy as np
from utillities import *
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

#id;Performer;Title;Inst.;Style;Year;Tempo;Number of Notes

training = open(sys.argv[1])

trainingset = csv.reader(training, delimiter=";")

Performers = set()
Insts = set()
Styles = set()
Years = set()
Tempos = set()



#General Statistics
Performers_solution = []
Insts_solution = []
Styles_solution = []
Years_solution = []
Tempos_solution = []
analytics_matrices = []

for row in trainingset:
    #Construct for every song a matrix and calculate analytics on it
    # columns are: C   C#  D   D#  E   F   F#  G   G#  A   A#  B
    # rows are :  0   1   2   3   4   5   6   7   8   9   10

    
    analytics_matrix = np.zeros((12,11))

    #get information of trainingsset
    id = row[0]
    Performers.add(row[1])
    Insts.add(row[3])
    Styles.add(row[4])
    Years.add(row[5])
    Tempos.add(row[6])

    #Load in songxml
    tree = ET.parse("songs-xml/"+id + ".xml")
    
    #get root 
    root = tree.getroot()

    #parse the file

    for measure in root.findall("part/measure"):
        for note in measure.findall("note"):
            rest = note.find("rest")
            if rest is None:

                Step = map_step_to_index(note.find("pitch/step").text)
                Octave = int(note.find("pitch/octave").text)
                #mark in matrix
                analytics_matrix[Step,Octave] += 1

    total_sum_of_notes = analytics_matrix.sum()
    analytics_matrix = np.divide(analytics_matrix, total_sum_of_notes)
    

    Performers_solution.append(row[1])
    Insts_solution.append(row[3])
    Styles_solution.append(row[4])
    Years_solution.append(row[5])
    Tempos_solution.append(row[6])
    analytics_matrices.append(analytics_matrix.flatten())


#pretty plot


Solutions = [Performers_solution,Insts_solution,Styles_solution,Years_solution,Tempos_solution]
Outputfiles = ['Performers.png','Insts.png','Styles.png','Years.png','Tempos.png']
svd = TruncatedSVD()
result = svd.fit_transform(analytics_matrices)
for i in range(len(Solutions)):
    pretty_scatter(result, Solutions[i], Outputfiles[i])




Performers_SVC = SVC()
Performers_SVC.fit(analytics_matrices,Performers_solution)

Insts_SVC = SVC()


Insts_SVC.fit(analytics_matrices,Insts_solution)

Styles_SVC = SVC()
# print(Styles_solution)
Styles_SVC.fit(analytics_matrices,Styles_solution)

Years_SVC = SVC()
# print(Years_solution)
Years_SVC.fit(analytics_matrices,Years_solution)

Tempos_SVC = SVC()
# print(Tempos_solution)
Tempos_SVC.fit(analytics_matrices,Tempos_solution)

 
test = open(sys.argv[2])

testset = csv.reader(test, delimiter=";")



analytics_matrices_testset = []
testset_id = []

for row in testset:

    analytics_matrix = np.zeros((12,11))

    #get information of trainingsset
    id = row[0]

    #Load in songxml
    tree = ET.parse("songs-xml/"+id + ".xml")
    
    #get root 
    root = tree.getroot()

    #parse the file

    for measure in root.findall("part/measure"):
        for note in measure.findall("note"):
            rest = note.find("rest")
            if rest is None:

                Step = map_step_to_index(note.find("pitch/step").text)
                Octave = int(note.find("pitch/octave").text)
                #mark in matrix
                analytics_matrix[Step,Octave] += 1

    total_sum_of_notes = analytics_matrix.sum()
    analytics_matrix = np.divide(analytics_matrix, total_sum_of_notes)
    
    analytics_matrices_testset.append(analytics_matrix.flatten())
    testset_id.append(id)


Performers_predictions = Performers_SVC.predict(analytics_matrices_testset)
Insts_predictions = Insts_SVC.predict(analytics_matrices_testset)
Styles_predictions = Styles_SVC.predict(analytics_matrices_testset)
Years_predictions = Years_SVC.predict(analytics_matrices_testset)
Tempos_predictions = Tempos_SVC.predict(analytics_matrices_testset)



with open(sys.argv[3], 'w') as csvfile:
    fieldnames = ['id','Performer','Inst','Style','Year','Tempo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter=";")
    writer.writeheader()
    for i in range(len(analytics_matrices_testset)):
        id = testset_id[i]
        writer.writerow({'id': id ,'Performer': Performers_predictions[i] ,'Inst': Insts_predictions[i],'Style': Styles_predictions[i],'Year': Years_predictions[i],'Tempo' : Tempos_predictions[i]})
