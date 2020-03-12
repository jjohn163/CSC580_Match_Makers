import numpy as np
import pandas as pd
import ampligraph
import requests
from ampligraph.datasets import load_from_csv
import tensorflow as tf


#url = 'https://ampligraph.s3-eu-west-1.amazonaws.com/datasets/GoT.csv'
#open('GoT.csv', 'wb').write(requests.get(url).content)
#X = load_from_csv('.', 'GoT.csv', sep=',')
#print(X[:5, ])

#entities = np.unique(np.concatenate([X[:, 0], X[:, 2]]))
#print(entities)

#relations = np.unique(X[:, 1])
#print(relations)

from ampligraph.evaluation import train_test_split_no_unseen
from ampligraph.latent_features import ComplEx
from ampligraph.latent_features import save_model, restore_model
from ampligraph.evaluation import evaluate_performance
from ampligraph.evaluation import mr_score, mrr_score, hits_at_n_score



def generate_model(X):
    X_train, X_test = train_test_split_no_unseen(X, test_size=100)

    print('Train set size: ', X_train.shape)
    print('Test set size: ', X_test.shape)

    model = ComplEx(batches_count=100,
                    seed=0,
                    epochs=10,
                    k=150,
                    eta=5,
                    optimizer='adam',
                    optimizer_params={'lr':1e-3},
                    loss='multiclass_nll',
                    regularizer='LP',
                    regularizer_params={'p':3, 'lambda':1e-5},
                    verbose=True)


    #positives_filter = X

    tf.logging.set_verbosity(tf.logging.ERROR)

    model.fit(X_train, early_stopping = False)

    print("created the model")

    save_model(model, './best_model.pkl')
    
    return X_test

def load_model():
    model = restore_model('./best_model.pkl')

    if model.is_fitted:
        print('The model is fit!')
        return model
    else:
        print('The model is not fit! Did you skip a step?')
        raise Exception

def evaluate_model(X_test, model, positives_filter):
    ranks = evaluate_performance(X_test,
                                 model=model,
                                 filter_triples=positives_filter,   # Corruption strategy filter defined above
                                 use_default_protocol=True, # corrupt subj and obj separately while evaluating
                                 verbose=True)

    mrr = mrr_score(ranks)
    print("MRR: %.2f" % (mrr))

    hits_10 = hits_at_n_score(ranks, n=10)
    print("Hits@10: %.2f" % (hits_10))
    hits_3 = hits_at_n_score(ranks, n=3)
    print("Hits@3: %.2f" % (hits_3))
    hits_1 = hits_at_n_score(ranks, n=1)
    print("Hits@1: %.2f" % (hits_1))


def evaluate_predictions(X_unseen, positives_filter, model):
    unseen_filter = np.array(list({tuple(i) for i in np.vstack((positives_filter, X_unseen))}))

    ranks_unseen = evaluate_performance(
        X_unseen,
        model=model,
        filter_triples=unseen_filter,   # Corruption strategy filter defined above
        corrupt_side = 's+o',
        use_default_protocol=False, # corrupt subj and obj separately while evaluating
        verbose=True)

    scores = model.predict(X_unseen)
    return scores
    #for score in scores:
    #    print(score)


