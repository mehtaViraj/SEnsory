from preprocessing import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, LSTM
from tensorflow.keras.utils import to_categorical


max_len = 11
buckets = 20

# Save data to array file first
save_data_to_array(max_len=max_len, n_mfcc=buckets)

labels=["audio0","audio1","audio2",]

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

model = Sequential()
model.add(Flatten(input_shape=(buckets, max_len)))
model.add(Dense(num_classes, activation='softmax'))
#model.add(Dropout(0.1))
model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=['accuracy'])

'''model = Sequential()
model.add(Conv2D(32,
    (3,3),
    input_shape=(buckets, max_len),
    activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=['accuracy'])'''


model.fit(X_train, y_train_hot, epochs=50, validation_data=(X_test, y_test_hot))
model.summary()