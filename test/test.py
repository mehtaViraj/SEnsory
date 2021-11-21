from preprocessing import *
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, LSTM
from tensorflow.keras.utils import to_categorical
import h5py

from tensorflow.keras.models import load_model
import os

modelllll = tensorflow.keras.models.load_model('trained_model.h5')
print("yooooooo")
