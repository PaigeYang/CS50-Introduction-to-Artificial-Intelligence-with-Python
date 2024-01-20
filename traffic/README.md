I have tried different convolutional layers and pooling layers combined. Two convolutional layers with 60 filters would get the lowest loss rate in testing data. However, I found the loss rate would be much high in testing data than training data. In other words, there may be overfitting in the model. In order to improve it, I add a hidden layer with dropout, and the situation improved. The loss rate decreases and the accuracy increase in my testing data. Therefore, in my final code, I use two convolutional layers, one pooling layer, and one hidden layer to get the best result.

Here are all models I have tried:
con:50 filters -> loss: 0.9513 - accuracy: 0.9166
con:10 filters / polling -> loss: 1.0009 - accuracy: 0.8790
con:50 filters / polling -> loss: 0.6862 - accuracy: 0.9244
con:100 filters / polling -> loss: 0.7044 - accuracy: 0.9276

con: 50 filters x2 / polling -> loss: 0.4862 -> accuracy: 0.9458
con: 30 filters / polling / con: 30 filters -> loss: 0.3894 - accuracy: 0.9425
con: 50 filters / polling / 50 filters -> loss: 0.4608 - accuracy: 0.9483
**con: 60 filters / polling / con: 60 filters -> loss: 0.2117 - accuracy: 0.9583**
con: 70 filters / polling / con: 70 filters -> loss: 0.3388 - accuracy: 0.9410

con: 30 filters / polling / con: 30 filters / polling ->  loss: 0.3077 - accuracy: 0.9371
con: 50 filters / polling / con: 50 filters / polling -> loss: 0.3172 - accuracy: 0.9444
con: 60 filters / polling / con: 60 filters / polling -> loss: 0.4866 - accuracy: 0.9140
con: 70 filters / polling / con: 70 filters / polling -> loss: 0.3863 - accuracy: 0.9250

con: 50 filters / polling / con: 50 filters / polling / 128 dropout 0.2 -> loss: 0.2593 - accuracy: 0.9356
con: 70 filters / polling / con: 70 filters / polling / 256 dropout 0.3 -> loss: 0.2258 - accuracy: 0.9463
con: 70 filters / polling / con: 70 filters / 128 dropout 0.5 - loss: 0.2375 - accuracy: 0.9433
**con: 60 filters / polling / con: 60 filters / 128 dropout 0.5 - loss: 0.1631 - accuracy: 0.9610**

con: 30 filters / polling / con: 30 filters / polling / con: 30 filters / polling ->  loss: 0.3506 - accuracy: 0.9306
con: 30 filters / polling / con: 30 filters / polling / con: 30 filters / polling / 128 dropout 0.2 -> loss: 0.2353 - accuracy: 0.9369