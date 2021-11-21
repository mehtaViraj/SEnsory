from tensorflow.keras.models import load_model
import preprocessing
import tensorflow
import numpy as np

from tensorflow.keras.models import load_model
from preprocessing import *
import tensorflow
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, LSTM
#from tensorflow.keras.utils import to_categorica
modelllll = load_model('trained_model')

max_len = 11
buckets = 20

# Save data to array file first
save_data_to_array(max_len=max_len, n_mfcc=buckets)

labels=["inner"]

# # Loading train set and test set
X_train, X_test, y_train, y_test = get_train_test()

# # Feature dimension
channels = 1
epochs = 50
batch_size = 100

num_classes = len(labels)

X_train = X_train.reshape(X_train.shape[0], buckets, max_len, channels)
X_test = X_test.reshape(X_test.shape[0], buckets, max_len, channels)

#plt.imshow(X_train[100, :, :, 0])
#print(y_train[100])

y_train_hot = to_categorical(y_train)
y_test_hot = to_categorical(y_test)

X_train = X_train.reshape(X_train.shape[0], buckets, max_len)
X_test = X_test.reshape(X_test.shape[0], buckets, max_len)

predictions = modelllll.predict(X_test)
classes = np.argmax(predictions, axis = 1)
print(classes)
