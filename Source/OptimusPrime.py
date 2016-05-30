import csv
import sys
import random
import xml.etree.ElementTree as ET
import numpy as np
from utillities import *
from constructors import *
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
from sklearn import linear_model
import matplotlib.pyplot as plt

#id;Performer;Title;Inst.;Style;Year;Tempo;Number of Notes

# fp_matrix, freq_notes = construct_fp_train(sys.argv[1])

# analytics_matrices_trainingsset, \
# trainingsset_id,\
# Performers_solution,\
# Insts_solution,\
# Styles_solution,\
# Years_solution,\
# Tempos_solution = construct_analytics_matrix_trainset(sys.argv[1],construct_analytics_matrix)

fList, \
trainingsset_id,\
Performers_solution,\
Insts_solution,\
Styles_solution,\
Years_solution,\
Tempos_solution = construct_feature_list(sys.argv[1])


# pop_notes_matrices_trainingsset, best_global = construct_note_pattern_matrix_trainset(sys.argv[1])

# new_matrix_set,index_set = extract_useful_features(analytics_matrices_trainingsset)

# analytics_matrices_trainingsset = new_matrix_set

# tempo_training = construct_tempo_array(sys.argv[1])


#code to make scatter plots
#pretty plot
# Solutions = [Performers_solution,Insts_solution,Styles_solution,Years_solution,Tempos_solution]
# Outputfiles = ['Performers.png','Insts.png','Styles.png','Years.png','Tempos.png']
# svd = TruncatedSVD()
# result = svd.fit_transform(analytics_matrices_trainingsset)
# result = svd.fit_transform(pop_notes_matrices_trainingsset)
# result = svd.fit_transform(fp_matrix)
# result = svd.fit_transform(fList)
# for i in range(len(Solutions)):
#     pretty_scatter(result, Solutions[i], Outputfiles[i])




Performers_SVC = SVC()
# Performers_SVC.fit(analytics_matrices_trainingsset,Performers_solution)
# Performers_SVC.fit(pop_notes_matrices_trainingsset,Performers_solution)
# Performers_SVC.fit(fp_matrix,Performers_solution)
Performers_SVC.fit(fList,Performers_solution)



Insts_SVC = SVC()
# Insts_SVC.fit(analytics_matrices_trainingsset,Insts_solution)
# Insts_SVC.fit(pop_notes_matrices_trainingsset,Insts_solution)
# Insts_SVC.fit(fp_matrix,Insts_solution)
Insts_SVC.fit(fList,Insts_solution)

Styles_SVC = SVC()
# print(Styles_solution)
# Styles_SVC.fit(analytics_matrices_trainingsset,Styles_solution)
# Styles_SVC.fit(pop_notes_matrices_trainingsset,Styles_solution)
# Styles_SVC.fit(fp_matrix,Styles_solution)
Styles_SVC.fit(fList,Styles_solution)


Years_SVC = SVC()
# print(Years_solution)
# Years_SVC.fit(analytics_matrices_trainingsset,Years_solution)
# Years_SVC.fit(pop_notes_matrices_trainingsset,Years_solution)
# Years_SVC.fit(fp_matrix,Years_solution)
Years_SVC.fit(fList,Years_solution)


Tempos_SVC = SVC()
# print(Tempos_solution)
# Tempos_SVC.fit(analytics_matrices_trainingsset,Tempos_solution)
#Tempos_SVC.fit(pop_notes_matrices_trainingsset,Tempos_solution)
# Tempos_SVC.fit(fp_matrix,Tempos_solution)
Tempos_SVC.fit(fList,Tempos_solution)



# analytics_matrices_testset, testset_id =  construct_analytics_matrix_testset(sys.argv[2],construct_analytics_matrix)


# pop_notes_matrices_testset, testset_id = construct_note_pattern_testset(sys.argv[2], best_global)
# fp_testset, testset_id = construct_fp_test(sys.argv[2], freq_notes)
fp_testset, testset_id = construct_test_feature_list(sys.argv[2])

# analytics_matrices_testset = extract_features_of_trainingsset(analytics_matrices_testset,index_set)

# Performers_predictions = Performers_SVC.predict(analytics_matrices_testset)
# Performers_predictions = Performers_SVC.predict(pop_notes_matrices_testset)
Performers_predictions = Performers_SVC.predict(fp_testset)

# Insts_predictions = Insts_SVC.predict(analytics_matrices_testset)
# Insts_predictions = Insts_SVC.predict(pop_notes_matrices_testset)
Insts_predictions = Insts_SVC.predict(fp_testset)

# Styles_predictions = Styles_SVC.predict(analytics_matrices_testset)
# Styles_predictions = Styles_SVC.predict(pop_notes_matrices_testset)
Styles_predictions = Styles_SVC.predict(fp_testset)

# Years_predictions = Years_SVC.predict(analytics_matrices_testset)
# Years_predictions = Years_SVC.predict(pop_notes_matrices_testset)
Years_predictions = Years_SVC.predict(fp_testset)

# Tempos_predictions = Tempos_SVC.predict(analytics_matrices_testset)
#Tempos_predictions = Tempos_SVC.predict(pop_notes_matrices_testset)
# Tempos_predictions = Tempos_SVC.predict(fp_testset)


Tempos_predictions = construct_tempo_array(sys.argv[2])

with open(sys.argv[3], 'w') as csvfile:
    fieldnames = ['id','Performer','Inst','Style','Year','Tempo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter=";")
    writer.writeheader()
    for i in range(len(fp_testset)):
        id = testset_id[i]
        writer.writerow({'id': id ,'Performer': Performers_predictions[i] ,'Inst': Insts_predictions[i],'Style': Styles_predictions[i],'Year': Years_predictions[i],'Tempo' : Tempos_predictions[i]})
