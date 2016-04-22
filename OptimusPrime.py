import csv
import sys
import random
import xml.etree.ElementTree as ET

#id;Performer;Title;Inst.;Style;Year;Tempo;Number of Notes

training = open(sys.argv[1])

trainingset = csv.reader(training, delimiter=";")

Performers = set()
Insts = set()
Styles = set()
Years = set()
Tempos = set()


for row in trainingset:
    id = row[0]
    Performers.add(row[1])
    Insts.add(row[3])
    Styles.add(row[4])
    Years.add(row[5])
    Tempos.add(row[6])
    # tree = ET.parse(id + ".xml")
    # root = tree.getroot()


test = open(sys.argv[2])



testset = csv.reader(test, delimiter=";")


   

with open(sys.argv[3], 'w') as csvfile:
    fieldnames = ['id','Performer','Inst','Style','Year','Tempo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter=";")
    writer.writeheader()
    for row in testset:
        id = row[0]
        writer.writerow({'id': id ,'Performer': (random.sample(Performers, 1))[0] ,'Inst': (random.sample(Insts, 1))[0],'Style': (random.sample(Styles, 1))[0],'Year': (random.sample(Years, 1))[0],'Tempo' : (random.sample(Tempos, 1))[0]})
        # tree = ET.parse(id + ".xml")
        # root = tree.getroot()


