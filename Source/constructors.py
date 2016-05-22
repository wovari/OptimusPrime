import csv
import sys
import random
import pprint
import itertools
import xml.etree.ElementTree as ET
import numpy as np
from sets import Set
from utillities import *
from constructors import *
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

#Constructs a analytics matrix for trainingsset
def construct_analytics_matrix_trainset(filename, features_selection_procedure ):
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

        analytics_matrix = features_selection_procedure(id_file)

        Performers_solution.append(row[1])
        Insts_solution.append(row[3])
        Styles_solution.append(row[4])
        Years_solution.append(row[5])
        Tempos_solution.append(row[6])
        set_ids.append(id_file)
        analytics_matrices_set.append(analytics_matrix.flatten())


    return analytics_matrices_set,set_ids,Performers_solution,Insts_solution,Styles_solution,Years_solution,Tempos_solution


#Constructs a analytics matrix for testset
def construct_analytics_matrix_testset(filename, features_selection_procedure):
    set_ids = []
    analytics_matrices_set = []
    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")
    for row in reader:
        #get information of trainingsset
        id = row[0]

        analytics_matrix = features_selection_procedure(id)

        #add elements to result
        analytics_matrices_set.append(analytics_matrix.flatten())

        set_ids.append(id)
    return analytics_matrices_set,set_ids

def construct_tempo_array(filename):
    set_ids = []
    tempo_list = []
    setfile = open(filename)
    reader = csv.reader(setfile, delimiter=";")
    for row in reader:
        id = row[0]
        tempo = calculate_tempo(id)
        tempo_list.append(tempo)
    return tempo_list



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




def construct_note_type_feature_matrix(id):
    #1,half,quarter,eight,16th
    analytics_matrix = np.zeros(14)


    #Load in songxml
    tree = ET.parse("songs-xml/"+ id + ".xml")

    #get root
    root = tree.getroot()

     #parse the file

    for measure in root.findall("part/measure"):
        for note in measure.findall("note"):
            rest = note.find("rest")
            if rest is None:
                #get right index
                index = map_type_to_index(note.find("type").text)

                #mark in matrix
                analytics_matrix[index] += 1

    total_sum_of_notes = analytics_matrix.sum()
    analytics_matrix = np.divide(analytics_matrix, total_sum_of_notes)
    return analytics_matrix




def construct_note_pattern_matrix_trainset(filename):
    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")

    #General Statistics
    Performers_solution = []
    Insts_solution = []
    Styles_solution = []
    Years_solution = []
    Tempos_solution = []
    pop_notes_matrices_set = []
    set_ids = []

    different_comb = Set([])

    for row in reader:
        #get information of trainingsset
        id_file = row[0]

        pop_notes_matrix = get_most_pop_comb(id_file, 3, 2)

        Performers_solution.append(row[1])
        Insts_solution.append(row[3])
        Styles_solution.append(row[4])
        Years_solution.append(row[5])
        Tempos_solution.append(row[6])
        set_ids.append(id_file)
        pop_notes_matrices_set.append(pop_notes_matrix)
        different_comb = different_comb | Set(np.rot90(pop_notes_matrix)[1])

    global_combinations = []
    different_comb = list(different_comb)
    for i in range(len(different_comb)):
        count = sum(sum(row[1] for row in matrix if row[0] == different_comb[i]) for matrix in pop_notes_matrices_set)
        global_combinations.append([different_comb[i], count])
    global_combinations = sorted(global_combinations, key=lambda row: row[1])
    best_global_combinations = np.rot90(global_combinations)[1][-100:]

    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")

    compared_notes_matrices = []
    for row in reader:
        id_file = row[0]
        tree = ET.parse("songs-xml/"+ id_file + ".xml")
        root = tree.getroot()
        list_of_notes = list_of_note_comb(root)
        compare_notes = []
        for i in range(len(best_global_combinations)):
            count = sum(row[1] for row in list_of_notes if row[0] == best_global_combinations[i])
            compare_notes.append(count)
        compared_notes_matrices.append(compare_notes)


    return compared_notes_matrices, best_global_combinations


#Constructs a analytics matrix for testset
def construct_note_pattern_testset(filename, global_combinations):
    set_ids = []
    analytics_matrices_set = []
    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")
    compared_notes_matrices = []
    for row in reader:
        id_file = row[0]
        tree = ET.parse("songs-xml/"+ id_file + ".xml")
        root = tree.getroot()
        list_of_notes = list_of_note_comb(root)
        compare_notes = []
        for i in range(len(global_combinations)):
            count = sum(row[1] for row in list_of_notes if row[0] == global_combinations[i])
            compare_notes.append(count)
        compared_notes_matrices.append(compare_notes)
        set_ids.append(id_file)



    return compared_notes_matrices,set_ids



def get_most_pop_comb(id, min_size, min_occ):
    #Load in songxml
    tree = ET.parse("songs-xml/"+ id + ".xml")
    root = tree.getroot()

    pop_comb_list = []
    for row in list_of_note_comb(root):
        if len(row[0]) >= (min_size * 2) and row[1] > min_occ:
            pop_comb_list.append(row)

    pop_comb_list = sorted(pop_comb_list, key=lambda row: row[1])
    return pop_comb_list

def list_of_note_comb(root):
    set_of_notes = Set([])
    list_of_measures = []
    for measure in root.findall("part/measure"):
        substrings = all_ordered_measure_substrings(measure)
        temp_set = Set(list(substrings))
        set_of_notes = set_of_notes | temp_set
        list_of_measures.append(substrings)

    list_of_notes = sorted(list(set_of_notes), key=lambda row: len(row))

    note_comb_ctr = []

    for i in range(len(list_of_notes)):
        comb = list_of_notes[i]
        count = sum(sum(1 for i in row if i == comb) for row in list_of_measures)
        note_comb_ctr.append([comb, count])

    return note_comb_ctr

# Returns all posible ordered substrings in a measure
def all_ordered_measure_substrings(measure):

    # Make a list with all notes in the measure in stringform
    notes = []
    for note in measure.findall("note"):
        rest = note.find("rest")
        if rest is None :
            step = note.find("pitch/step").text
            octave = note.find("pitch/octave").text
            notes.append(step + octave)
        else:
            notes.append("R0")

    #Make all the possible combinations and return the list
    resultList= []

    for i in range(len(notes)):
        prev = notes[i]
        resultList.append(notes[i])
        if i != notes[-1]:
            for j in range(i+1,len(notes)):
                prev += notes[j]
                resultList.append(prev)

    return resultList

# updates the values in the matrix according to constrast mininig
def update_contrast_values(key, dictionary, newvalue):
    
    #if key is already in the dictionary and value needs to be updated
    if key in dictionary:

        pair = dictionary[key]
        count = pair[0] + 1
        dic = pair[1]
        result = np.zeros((12,11))
        # iterate through rows
        for i in range(len(dic)):
           # iterate through columns
           for j in range(len(dic[0])):
               result[i][j] = dic[i][j] + newvalue[i][j]
        #store results in dictionary 
        dictionary[key]  = (count,dic)
    #add new value to dictionary
    else:
        dictionary[key]  = (1,newvalue)


#takes the average of every group
def normalize_constrast_values(dictionary):

    for x in dictionary:
        pair = dictionary[x[]
        count = pair[0]
        dic = pair[1]
        #normalize dictionaries
        dictionary[x] = [y / float(count) for y in dic]



def construct_analytics_matrix_constrast_mining(filename, features_selection_procedure):
    setfile= open(filename)
    reader = csv.reader(setfile, delimiter=";")

    #gather for each set information
    Performers_solution = {}
    Insts_solution = {}
    Styles_solution = {}
    Years_solution = {}
    Tempos_solution = {}

    #parse each element of trainingsset
    for row in reader:

        #get information of trainingsset
        id_file = row[0]
        
        analytics_matrix = construct_analytics_matrix(id_file)

        #add element to dictionaries and update accodingly
        update_contrast_values(row[1],Performers_solution,analytics_matrix)
        update_contrast_values(row[3],Insts_solution,analytics_matrix)
        update_contrast_values(row[4],Styles_solution,analytics_matrix)
        update_contrast_values(row[5],Years_solution,analytics_matrix)
        update_contrast_values(row[6],Tempos_solution,analytics_matrix)



    #take average values of grouped features
    normalize_constrast_values(Performers_solution)
    normalize_constrast_values(Insts_solution)
    normalize_constrast_values(Styles_solution)
    normalize_constrast_values(Years_solution)
    normalize_constrast_values(Tempos_solution)


    return Performers_solution,Insts_solution,Styles_solution,Years_solution,Tempos_solution
    




