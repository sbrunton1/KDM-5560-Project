# KDM-5560-Project
Project for UMKC CS-5560 Knowledge and Discovery Management 
### Team members

- Lyle Vanfossan
- Scott Brunton
- Jack Wojcicki
- Zekai How

## Setup
This application was developed using `Python 3.6+` running in an Anaconda Environment

- [Install Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
- [Install Python](https://www.python.org/downloads/windows/)

## Dependencies
Using the package manager [pip](https://pip.pypa.io/en/stable/), run the following script to install all necessary packages.

```bash
pip install requirements.txt
```

## Initial model training
This application requires running the `chatbot_trainer.py` file prior to running the main demo.

```bash
py chatbot_trainer.py
```
Doing so will create the tensorflow model which will be used throughout the demonstration process.

For this project, a sample text corpus has been provided in `training_data/training.json`. 

This training file can and will be modified throughout the demo.

### The following is an example of what a user should see when running initial training.
```bash
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
embedding (Embedding)        (None, 20, 16)            16000
_________________________________________________________________
global_average_pooling1d (Gl (None, 16)                0
_________________________________________________________________
dense (Dense)                (None, 46)                782
_________________________________________________________________
dense_1 (Dense)              (None, 46)                2162
_________________________________________________________________
dense_2 (Dense)              (None, 9)                 423
=================================================================
Total params: 19,367
Trainable params: 19,367
Non-trainable params: 0
_________________________________________________________________
Epoch 1/500

1/1 [==============================] - ETA: 0s - loss: 2.1994 - accuracy: 0.0000e+00
1/1 [==============================] - 0s 312ms/step - loss: 2.1994 - accuracy: 0.0000e+00
Epoch 2/500

1/1 [==============================] - ETA: 0s - loss: 2.1974 - accuracy: 0.1250
1/1 [==============================] - 0s 0s/step - loss: 2.1974 - accuracy: 0.1250
Epoch 3/500

1/1 [==============================] - ETA: 0s - loss: 2.1956 - accuracy: 0.1250
1/1 [==============================] - 0s 997us/step - loss: 2.1956 - accuracy: 0.1250
Epoch 4/500
...
```

A new folder `./chat_model` will be created, containing all files necessary for utilizing the trained tensorflow model across the project.

## Running main application

Once initial training has completed, the following script can be ran to launch the main demo app.
```bash
py main.py
```

This will lauch an application, which can be accessed via browser at `http://localhost:5000/`