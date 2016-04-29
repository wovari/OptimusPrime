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
    tree = ET.parse("songs-xml/"+id + ".xml")
    root = tree.getroot()
    noteCtr = 0
    durCtr = 0
    for measure in root.findall("part/measure"):
        for note in measure.findall("note"):
            rest = note.find("rest")
            if rest is None:
                element = note.find("type")
                # if not element is None and element.text == "quarter":
                noteCtr += 1
            durCtr += int(note.find("duration").text)

    print("ID: %s \n ======================"%(id))
    print("Amount of notes: %d"%(noteCtr))
    print("Duration: %d"%(durCtr))
    print("Tempo: %d"%(durCtr/noteCtr))


test = open(sys.argv[2])



testset = csv.reader(test, delimiter=";")




with open(sys.argv[3], 'w') as csvfile:
    fieldnames = ['id','Performer','Inst','Style','Year','Tempo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,  delimiter=";")
    writer.writeheader()
    for row in testset:
        id = row[0]
        writer.writerow({'id': id ,'Performer': (random.sample(Performers, 1))[0] ,'Inst': (random.sample(Insts, 1))[0],'Style': (random.sample(Styles, 1))[0],'Year': (random.sample(Years, 1))[0],'Tempo' : (random.sample(Tempos, 1))[0]})
        tree = ET.parse("songs-xml/" + id + ".xml")
        root = tree.getroot()
