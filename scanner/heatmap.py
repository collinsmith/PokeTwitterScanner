'''
Created on Sep 29, 2016

@author: csmith
'''
import codecs
import csv
import gmaps
import gmaps.datasets

from codes import google_api_key

def _read_rows(f):
    f.readline() # skip header line
    reader = csv.reader(codecs.iterdecode(f, "utf-8"))
    rows = [tuple(map(float, row)) for row in reader]
    return rows

def load_dataset(filename):
    f = open(filename)
    data = _read_rows(f)
    f.close()
    return data

gmaps.configure(api_key=google_api_key)

# load a Numpy array of (latitude, longitude) pairs
#data = load_dataset("pokemon.snorlax.csv")
data = gmaps.datasets.load_dataset("starbucks_uk")

m = gmaps.Map()
m.add_layer(gmaps.Heatmap(data=data))
m