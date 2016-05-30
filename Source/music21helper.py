from music21 import *

def create_m21_dataset():
    ds = features.DataSet(classLabel="ID")
    #p => pitch based features
    #r => rythm based featurs
    fes = features.extractorsById(['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p19','p20','p21',
                                    'r31','r32','r33','r34','r35'])
    ds.addFeatureExtractors(fes)
    return ds

def add_song_to_dataset(song_id, ds):
    print "Add song: %s"%(song_id)
    filename = "songs-xml/"+ song_id + ".xml"
    ds.addData(filename, classValue=song_id)
    return ds

def process_dataset(ds):
    ds.process()
    return ds

def create_list(ds):
    fList = ds.getFeaturesAsList()
    newList = []
    for feature in fList:
        print feature
        newFeature = feature[1:-1]
        newList.append(newFeature)
        print newFeature
    return newList
