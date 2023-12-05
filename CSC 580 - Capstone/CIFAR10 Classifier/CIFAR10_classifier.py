import os
import numpy as np
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

class CIFAR10_classifier():

    def __init__(self):
        self.model_name = 'CIFAR10_classifier'
        #Data Properties - Defined in load_data()
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.x_val = None
        self.y_val = None

        #Model - Defined in Load_Model()
        self.model = None

        #HYPERPARAMETERS
        self.epochs = 100
        self.batch_size = 64
        self.dropout = 0.2
        self.validation_size = 0.5 # Size of Validation data set - Split from test data set.
        self.data_shape = (32, 32, 3)

        #Callbacks
        self.es_callback = keras.callbacks.EarlyStopping(monitor='val_loss',mode='min', patience=3)

        #Dictionary of CIFAR10 Labels
        self.cfar10_label_dict = {0:'airplane', 1:'automobile', 2:'bird', 3:'cat', 4:'deer', 5:'dog', 6:"frog", 7:'horse', 8:'ship', 9:'truck'  }
        
        #NORMALIZATION PROPERTIES
        self.mean = None
        self.std = None
        pass

    def load_data(self):
        print("Loading Data...")
        (self.x_train, self.y_train), (self.x_test, self.y_test) = tf.keras.datasets.cifar10.load_data()
        #Shuffling Dataset
        self.x_train, self.y_train = shuffle(self.x_train, self.y_train, random_state=42)
        self.x_test, self.y_test = shuffle(self.x_test, self.y_test, random_state=42)
        #Splitting Test Dataset to have a Validation dataset.        
        self.x_test, self.x_val, self.y_test, self.y_val = train_test_split(self.x_test, self.y_test, test_size=self.validation_size, random_state=42)
        print("TRAIN Dataset Length:",len(self.x_train))
        print("TEST Dataset Length:",len(self.x_test))
        print("VAL Dataset Length:",len(self.x_val))

        self.x_train = self.x_train.astype('float32')
        self.mean = tf.math.reduce_mean(self.x_train, axis=0)
        self.std = tf.math.reduce_std(self.x_train,axis=0)
        #Normalizing Pixel values to be between 0 and 1
        self.x_train = (self.x_train-self.mean)/self.std
        self.x_test = (self.x_test-self.mean)/self.std
        self.x_val = (self.x_val-self.mean)/self.std
        pass


    def define_model(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.data_shape))
        self.model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        self.model.add(tf.keras.layers.Dropout(self.dropout))  
        
        self.model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        self.model.add(tf.keras.layers.Dropout(self.dropout))

        self.model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(tf.keras.layers.Flatten())
        self.model.add(tf.keras.layers.Dense(64, activation='relu'))
        self.model.add(tf.keras.layers.Dense(10)) # 10 Classes

        # Output Layer
        self.model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))
        self.model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
        return self.model

    def load_model(self):
        exists = os.path.isdir(self.model_name)
        model = None
        if exists:
            model = tf.keras.models.load_model(self.model_name)
        return model

    def train_model(self):
        history = self.model.fit(self.x_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size, validation_data=(self.x_val, self.y_val), callbacks=[self.es_callback])    
        self.model.save(self.model_name)
        return history

    def evaluate_test_data(self):
        eval_results = self.model.evaluate(self.x_test,self.y_test,batch_size=self.batch_size)
        loss, accuracy = eval_results
        print("Test Loss:",loss)
        print("Test Accuracy:",accuracy)
        pass

    def display_model_history(self, history):
        #Display Accuracy History Plot
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.savefig('training_history.png')
        plt.waitforbuttonpress()
        plt.close()
        #Display Loss History Plot
        plt.plot(history.history['loss'], label='loss')
        plt.plot(history.history['val_loss'], label = 'val_loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.savefig('training_loss.png')
        plt.waitforbuttonpress()
        plt.close()
        pass

    def display_imgs(self):
        predictions = self.model.predict(self.x_test)
        plt.figure(figsize=(10,10))
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        for i in range(25):
            plt.subplot(5,5,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            unnormalized_img = (self.x_test[i]*self.std + self.mean)#.astype('uint8')
            unnormalized_img = tf.cast(unnormalized_img, dtype=tf.uint8)
            plt.imshow(unnormalized_img)
            # The CIFAR labels happen to be arrays, 
            # which is why you need the extra index
            predicted=predictions[i].argmax()
            label_string = "Predicted:" + self.cfar10_label_dict[predicted] + "\nActual:" + self.cfar10_label_dict[self.y_test[i][0]]
            plt.xlabel(label_string)
        plt.show()
        pass

def main():
    c = CIFAR10_classifier()
    
    c.load_data()
    
    c.model = c.load_model()
    #If Model hasn't been trained yet, train the model.
    if c.model == None:
        print("Training Model.")
        c.define_model()
        history = c.train_model()
        c.display_model_history(history)

    c.evaluate_test_data()
    c.display_imgs()
    pass

if __name__ == "__main__":
    main()
    