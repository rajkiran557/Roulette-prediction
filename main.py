import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import json
import math

def testModel(predictions, targets):
    accuracy=[]
    i=0
    for predict in predictions: # predict: 50 elements array
        acc=0
        j=0
        for element in predict:
            if targets[i][j]==element:
                acc+=1
            j+=1
        accuracy.append(acc/len(predict))
        i+=1
    return np.mean(accuracy)

def color(data):
    result=[]
    for el in data:
        if el==0:
            result.append('green')
        elif el==1:
            result.append('black')
        elif el==-1:
            result.append('red')
    return result

def plot(data, targets=None):
    plt.figure()
    plt.title("Spin history", fontsize=20)
    n=len(data)
    plt.scatter([i+1 for i in range(0,n)], [1 for i in range(0,n)], c=color(data), marker='$\u25AE$', s=100)
    if not (targets is None):
        plt.scatter([i+1 for i in range(0,n)], [-1 for i in range(0,n)], c=color(targets), marker='$\u25AE$', s=100)
    plt.xlabel('Spin')
    plt.ylim([-20,20])
    plt.yticks([])
    plt.show()

def roundPred(predictions):
    predR=[]
    for prediction in predictions:
        pred50=[]
        for el in prediction:
            if el>0:
                el=1
            elif el<0:
                el=-1
            pred50.append(el)
        predR.append(pred50)
    return predR

"""training_data is a list containing x tuples (x, y)
x is a 100-dimensional numpy.ndarray
containing the input spins.  y is a 50-dimensional
numpy.ndarray representing the next 50 spins to be predicted"""

if __name__ == '__main__':
    data = json.load(open("data.txt", "r"))
    raw_data = data["raw_data"]
    training_data = []
    data = []
    targets = []
    for arr in raw_data: # arr contains 200 spins
        first_x = [np.array(x) for x in arr[:100]]
        first_y = [np.array(y) for y in arr[100:150]]
        training_data.append(tuple([first_x, first_y]))
        data.append(first_x)
        targets.append(first_y)
        second_x = [np.array(x) for x in arr[50:150]]
        second_y = [np.array(y) for y in arr[150:200]]
        training_data.append(tuple([second_x, second_y]))
        data.append(second_x)
        targets.append(second_y)

    data, targets = np.array(data), np.array(targets)
    
    #split data between test and train
    train_data_len = math.ceil(len(data) * .9)
    train_data = data[0:train_data_len]
    test_data = data[train_data_len:len(data)]
    train_target = targets[0:train_data_len]
    test_target = targets[train_data_len:len(data)]

    #reshape the data
    train_data = np.reshape(train_data, (train_data.shape[0], train_data.shape[1], 1))
    test_data = np.reshape(test_data, (test_data.shape[0], test_data.shape[1], 1))

    #build the LSTM model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(train_data.shape[1], 1)))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.LSTM(128, return_sequences=False))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(80, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(50, activation=tf.nn.tanh))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(train_data, train_target, batch_size=10, epochs=500)

    predictions = model.predict(test_data)
    predictionsR = roundPred(predictions)

    # plotting one prediction
    print(predictionsR[1])
    print(test_target[1])
    plot(predictionsR[2], test_target[2])
    
    # test the model
    percentCorrect = testModel(predictionsR, test_target)

    print(f"Average accuracy: {percentCorrect*100:.2f}%")

    model.save("Roulette.model")
