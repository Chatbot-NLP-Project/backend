import nltk
from tensorflow.python.ops.gen_array_ops import shape

from nltk.stem.lancaster import LancasterStemmer   # used to stem our words
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

    # tflearn works with numpy arrays
    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# resetting if there are any previous underlying data graphs
tensorflow.compat.v1.reset_default_graph()

# define input shape we are expecting to train the model
net = tflearn.input_data(shape=[None, len(training[0])])
# adding two hidden internal layers with 8 neurons each
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
# softmax gives the probability of the output
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
# regression is the classification algorithm used (probably logistic regression)
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
     model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

# model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
# model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def chat3(inp):

    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]


    if results[results_index] > 0.75:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                print(responses)
                res = random.choice(responses)

        return res
    else:
        return ("I didn't get that, try again.")
