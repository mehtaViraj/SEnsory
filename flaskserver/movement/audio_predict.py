from tensorflow.keras.models import load_model
#import preprocessing
import tensorflow
import numpy as np
import movement.duplicate_wav_file as duplicate_wav_file
from tensorflow.keras.models import load_model
from movement.preprocessing import *
import tensorflow
#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, LSTM

print("<-----------------------------------AUDIO IMPORTS COMPLETE------------------------------------>")

class VoiceRecognition:
    def __init__(self):
        self.model = load_model('trained_model_colour')
        print("Model loaded")

    def predict(self):
        duplicate_wav_file.duplicateIt()
        print("Duplicated")
        #from tensorflow.keras.utils import to_categorica

        max_len = 11
        buckets = 20

        # Save data to array file first
        get_test_data_array(max_len=max_len, n_mfcc=buckets)
        print("Data saved to array")

        # # Loading train set and test set
        X_train, X_test, y_train, y_test = get_train_test()
        print("Dataset split")

        # # Feature dimension
        channels = 1

        X_test = X_test.reshape(X_test.shape[0], buckets, max_len, channels)
        X_test = X_test.reshape(X_test.shape[0], buckets, max_len)
        print("All reshaped")

        predictions = self.model.predict(X_test)
        print("Tested")
        classes = np.argmax(predictions, axis = 1)
        l = ['blue','yellow','pink']
        print("Returning")
        return l[classes[0]]

if __name__ == "__main__":
    alexa = VoiceRecognition()
    for i in range(4):
        print(alexa.predict())