# A neural network that predicts the next spin color
This is my attempt at building a neural network that is able to find weaknesses in a particular Casino algorithm, using the same methodology as time series forecasting in neural networks, usually applied to stock prediction.
The bot.py only works with a particular casino, and it was used to get the training data. It spins the roulette and detects the resulting color. Each sequence of 200 consecutive colors is then stored into a file.
The main.py is the keras implementation of the network.
