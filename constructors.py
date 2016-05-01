import csv
import sys
import random
import xml.etree.ElementTree as ET
import numpy as np
from utillities import *
from constructors import *
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
#Constructs a analytics matrix for trainingsset
def construct_analytics_matrix_trainset(filename):
    setfile= open(filename)
    print(filename)
    reader = csv.reader(setfile, delimiter=";")
    #General Statistics
    Performers_solution = []
    Insts_solution = []
    Styles_solution = []
    Years_solution = []
    Tempos_solution = []
    analytics_matrices_set = []
    set_ids = []

    for row in reader:
  
        #get information of trainingsset
        id_file = row[0]

        analytics_matrix = construct_analytics_matrix(id_file)
        
        Performers_solution.append(row[1])
        Insts_solution.append(row[3])
        Styles_solution.append(row[4])
        Years_solution.append(row[5])
        Tempos_solution.append(row[6])
        set_ids.append(id_file)
        analytics_matrices_set.append(analytics_matrix.flatten())
    return analytics_matrices_set,set_ids,Performers_solution,Insts_solution,Styles_solution,Years_solution,Tempos_solution


#Constructs a analytics matrix for testset
def construct_analytics_matrix_testset(filename):
    set_ids = []
    analytics_matrices_set = []
    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")
    for row in reader:
        #get information of trainingsset
        id = row[0]

        analytics_matrix = construct_analytics_matrix(id)

        #add elements to result
        analytics_matrices_set.append(analytics_matrix.flatten())

        set_ids.append(id)
    return analytics_matrices_set,set_ids


def construct_analytics_matrix(id):
    # columns are: C   C#  D   D#  E   F   F#  G   G#  A   A#  B
    # rows are :  0   1   2   3   4   5   6   7   8   9   10
    analytics_matrix = np.zeros((12,11))

    #Load in songxml
    tree = ET.parse("songs-xml/"+ id + ".xml")
    
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

    return analytics_matrix

