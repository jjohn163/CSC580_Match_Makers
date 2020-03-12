from model_maker import *
from graph_maker import *

import numpy as np
import pandas as pd
import ampligraph


import requests
from ampligraph.datasets import load_from_csv

def get_candidates(network, target, topic=""):
    immediate_connections = network[target].connections.keys()
    candidates = []
    if topic != "":
        for researcher in network.keys():
            if (researcher not in immediate_connections) and (researcher != target) and (topic in network[researcher].interests):
                candidates.append(researcher)
    else:
        for researcher in immediate_connections:
            for indirect_researcher in network[researcher].connections.keys():
                if (indirect_researcher not in immediate_connections) and (indirect_researcher not in candidates) and (indirect_researcher != target):
                    candidates.append(indirect_researcher)
    return candidates
    
def get_predictions(target, candidates):
    predictions = []
    for researcher in candidates:
        predictions.append([target, 'STRONGLY_CONNECTED', researcher])
        predictions.append([target, 'NORMALLY_CONNECTED', researcher])
        predictions.append([target, 'WEAKLY_CONNECTED', researcher])
    return np.array(predictions)

def generate_reccomendations(network, model, positives_filter, target, topic):
    if target not in network.keys():
        return ["NAME NOT FOUND"]
    candidates = get_candidates(network, target, topic)
    if len(candidates) == 0:
        return ["NO RESULTS FOUND"]
    X_unseen = get_predictions(target, candidates)
    scores = evaluate_predictions(X_unseen, positives_filter, model)

    results = []
    for i in range(len(candidates)):
        score = (scores[3 * i]*100) + (scores[3 * i + 1]*10) + (scores[3 * i + 2])
        results.append([candidates[i], score])
        j = len(results)-1
        while j > 0 and results[j][1] > results[j-1][1]:
            temp = results[j]
            results[j] = results[j-1]
            results[j-1] = temp
            j -= 1
    reccomendations = []
    for result in results:
        reccomendations.append(result[0])

    return reccomendations

def main():
    network = read_network()
    positives_filter = load_from_csv('.', 'network.csv', sep=',')
    model = load_model()
    reccomendations = generate_reccomendations(network, model, positives_filter, "Bruce DeBruhl", "artificial intelligence")
    if len(reccomendations) > 5:
        reccomendations = reccomendations[:5]
    print(reccomendations)



if __name__=="__main__":
        main()
