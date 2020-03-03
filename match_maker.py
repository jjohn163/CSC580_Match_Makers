from model_maker import *
from graph_maker import *

import numpy as np
import pandas as pd
import ampligraph


import requests
from ampligraph.datasets import load_from_csv




def main():
#    from graph_maker import read_network
#    network = read_network()
#    print(network[1])
#    import model_maker
    X = load_from_csv('.', 'network.csv', sep=',')
    positives_filter = X
    #X_test = generate_model(X)
    model = load_model()
    #evaluate_model(X_test, model, positives_filter)
    X_unseen = np.array([
        ['Franz J Kurfess', 'STRONGLY_CONNECTED', 'Daniel Kauffman']
        ])
    """
    X_unseen = np.array([
        ['Jorah Mormont', 'SPOUSE', 'Daenerys Targaryen'],
        ['Tyrion Lannister', 'SPOUSE', 'Missandei'],
        ["King's Landing", 'SEAT_OF', 'House Lannister of Casterly Rock'],
        ['Sansa Stark', 'SPOUSE', 'Petyr Baelish'],
        ['Daenerys Targaryen', 'SPOUSE', 'Jon Snow'],
        ['Daenerys Targaryen', 'SPOUSE', 'Craster'],
        ['House Stark of Winterfell', 'IN_REGION', 'The North'],
        ['House Stark of Winterfell', 'IN_REGION', 'Dorne'],
        ['House Tyrell of Highgarden', 'IN_REGION', 'Beyond the Wall'],
        ['Brandon Stark', 'ALLIED_WITH', 'House Stark of Winterfell'],
        ['Brandon Stark', 'ALLIED_WITH', 'House Lannister of Casterly Rock'],
        ['Rhaegar Targaryen', 'PARENT_OF', 'Jon Snow'],
        ['House Hutcheson', 'SWORN_TO', 'House Tyrell of Highgarden'],
        ['Daenerys Targaryen', 'ALLIED_WITH', 'House Stark of Winterfell'],
        ['Daenerys Targaryen', 'ALLIED_WITH', 'House Lannister of Casterly Rock'],
        ['Jaime Lannister', 'PARENT_OF', 'Myrcella Baratheon'],
        ['Robert I Baratheon', 'PARENT_OF', 'Myrcella Baratheon'],
        ['Cersei Lannister', 'PARENT_OF', 'Myrcella Baratheon'],
        ['Cersei Lannister', 'PARENT_OF', 'Brandon Stark'],
        ["Tywin Lannister", 'PARENT_OF', 'Jaime Lannister'],
        ["Missandei", 'SPOUSE', 'Grey Worm'],
        ["Brienne of Tarth", 'SPOUSE', 'Jaime Lannister']
    ])
    """
    scores = evaluate_predictions(X_unseen, positives_filter, model)
    for score in scores:
        print(score)



if __name__=="__main__":
        main()
