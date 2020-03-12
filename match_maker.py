from model_maker import *
from graph_maker import *
from tkinter import *
from tkinter import scrolledtext

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
    #generate_model(positives_filter)
    model = load_model()

    window = Tk()

    window.title("Match Makers")

    window.geometry('350x200')

    lbl = Label(window, text="Name")

    lbl.grid(column=0, row=0)

    target = Entry(window,width=30)

    target.grid(column=1, row=0)

    lbl2 = Label(window, text="Topic")

    lbl2.grid(column=0, row=1)

    topic = Entry(window, width=30)

    topic.grid(column=1, row=1)

    lbl3 = Label(window, text="Results")

    lbl3.grid(column=0, row=3)
    
    results = scrolledtext.ScrolledText(window,width=40,height=10)

    results.grid(column=0, row=4)

    def clicked():

        #res = "Welcome to " + target.get()
        reccomendations = generate_reccomendations(network, model, positives_filter, target.get(), topic.get())
        if len(reccomendations) > 5:
            reccomendations = reccomendations[:5]
        final_result = "\n".join(reccomendations)

        results.delete(1.0,END)
        results.insert(INSERT,final_result)

    btn = Button(window, text="Process", command=clicked)

    btn.grid(column=0, row=2)

    window.mainloop()


#    reccomendations = generate_reccomendations(network, model, positives_filter, "Bruce DeBruhl", "artificial intelligence")
#    if len(reccomendations) > 5:
#        reccomendations = reccomendations[:5]
#    print(reccomendations)



if __name__=="__main__":
        main()
