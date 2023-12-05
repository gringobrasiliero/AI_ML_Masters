import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import UpSampling2D, Conv2D
from keras.models import Sequential, Model
from keras.optimizers import Adam,SGD
from numpy import expand_dims
from numpy import ones
from numpy import zeros
from numpy.random import rand
from numpy.random import randint
from keras.datasets.cifar10 import load_data
from keras.optimizers import Adam
from keras.models import Sequential
from tensorflow.keras.utils import plot_model
from numpy.random import randn
from matplotlib import pyplot
from keras.layers import Conv2DTranspose

class CIFAR10_GAN():
    def __init__(self):
        self.x_train = None 
        self.batch_size = 49
        self.half_batch_size = self.batch_size//2
        self.epochs = 200
        self.image_shape = (32, 32, 3)
        self.latent_points = 100
        self.current_model_name = None
        pass

    def load_data(self):
        (x_train, y_train), (_,_) = keras.datasets.cifar10.load_data()
        x_train = x_train[y_train.flatten() == 3] #Filtering for only Cat images
        x_train = (x_train-127.5) / 127.5 #Normalizing Pixel values to be between -1 and 1.
        self.x_train = x_train
        pass

    def get_real_samples(self, batch_size):
        random_int = randint(0, self.x_train.shape[0], batch_size)
        x = self.x_train[random_int]
        y = ones((batch_size,1))
        return x,y
    
    def generate_fake_images(self, gen_model, batch_size):
        x_input = self.generate_latent_points(batch_size)
        x = gen_model.predict(x_input)
        y = zeros((batch_size, 1))
        return x, y

# generate points in latent space as input for the generator
    def generate_latent_points(self, batch_size):
         # generate points in the latent space
        x_input = randn(self.latent_points * batch_size)
        # reshape into a batch of inputs for the network
        x_input = x_input.reshape(batch_size, self.latent_points)
        return x_input

    #Step 4: Define a utility function to build the generator.
    def build_generator(self, latent_dimensions):
         model = Sequential()
         # foundation for 4x4 image
         n_nodes = 256 * 4 * 4
         model.add(Dense(n_nodes, input_dim=latent_dimensions))
         model.add(LeakyReLU(alpha=0.2))
         model.add(Reshape((4, 4, 256)))
         # upsample to 8x8
         model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'))
         model.add(LeakyReLU(alpha=0.2))
         # upsample to 16x16
         model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'))
         model.add(LeakyReLU(alpha=0.2))
         # upsample to 32x32
         model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'))
         model.add(LeakyReLU(alpha=0.2))
         # output layer
         model.add(Conv2D(3, (3,3), activation='tanh', padding='same'))
         return model

#Step 5: Define a utility function to build the discriminator.
    def build_discriminator(self):
         model = Sequential()
         # normal
         model.add(Conv2D(64, (3,3), padding='same', input_shape=self.image_shape))
         model.add(LeakyReLU(alpha=0.2))
         # downsample
         model.add(Conv2D(128, (3,3), strides=(2,2), padding='same'))
         model.add(LeakyReLU(alpha=0.2))
         # downsample
         model.add(Conv2D(128, (3,3), strides=(2,2), padding='same'))
         model.add(LeakyReLU(alpha=0.2))
         # downsample
         model.add(Conv2D(256, (3,3), strides=(2,2), padding='same'))
         model.add(LeakyReLU(alpha=0.2))
         # classifier
         model.add(Flatten())
         model.add(Dropout(0.4))
         model.add(Dense(1, activation='sigmoid'))
         # compile model
         opt = Adam(learning_rate=0.0002, beta_1=0.5)
         model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
         return model

    def define_gan(self, gen_model, discrim_model):
        discrim_model.trainable = False
        model = Sequential()
        model.add(gen_model)
        model.add(discrim_model)
        optimizer = Adam(learning_rate=.0002, beta_1=0.5)
        model.compile(loss='binary_crossentropy', optimizer=optimizer)
        return model

    def train_gan(self, gen_model, discrim_model, gan_model):        
        for i in range(self.epochs):
            for j in range(self.batch_size):
                x_real, y_real = self.get_real_samples(self.half_batch_size)
                d_loss1, _ = discrim_model.train_on_batch(x_real, y_real)
                x_fake, y_fake = self.generate_fake_images(gen_model, self.half_batch_size)
                d_loss2 , _ = discrim_model.train_on_batch(x_fake, y_fake)
                x_gan = self.generate_latent_points(self.half_batch_size)
                y_gan = ones((self.half_batch_size,1))
                g_loss = gan_model.train_on_batch(x_gan, y_gan)
                print('>%d, %d/%d, d_r=%.3f, d_f=%.3f g=%.3f' % (i+1, j+1, self.batch_size, d_loss1, d_loss2, g_loss))
            if (i+1) % 10 == 0 or i == 0:
                self.summarize_performance(i, discrim_model, gen_model)
        pass

    def summarize_performance(self, epoch, discrim_model, gen_model):
        x_real, y_real = self.get_real_samples(self.batch_size)
        _, accuracy_real = discrim_model.evaluate(x_real, y_real, verbose=0)
        x_fake, y_fake = self.generate_fake_images(gen_model, self.batch_size)
        _, accuracy_fake = discrim_model.evaluate(x_fake, y_fake, verbose=0)
        print('>Accuracy real: %.0f%%, fake: %.0f%%' % (accuracy_real*100, accuracy_fake*100))
        filename = 'generator_model_%03d.h5' % (epoch+1)
        self.current_model_name = filename
        gen_model.save(filename)
        self.save_plot(x_fake, epoch)
        self.save_plot(x_real, epoch)

    def save_plot(self, examples, epoch, n=7):
        examples = (examples + 1) / 2.0
        for i in range(n * n):
            pyplot.subplot(n, n, 1 + i)
            pyplot.axis('off')
            pyplot.imshow(examples[i])
     # save plot to file
        filename = 'generated_plot_e%03d.png' % (epoch+1)
        pyplot.savefig(filename)
        pyplot.close()


def main():
    gan = CIFAR10_GAN()
    #Load Data
    gan.load_data()
    #Define the discriminator model
    discriminator_model = gan.build_discriminator()
    discriminator_model.compile(loss='binary_crossentropy',
                          optimizer=Adam(0.0002,0.5),
                        metrics=['accuracy'])

    #Define the size of the latent space
    latent_dim = 100
    #Define the generator model
    gen_model = gan.build_generator(latent_dim)
    gan_model = gan.define_gan(gen_model, discriminator_model)

    gan.train_gan(gen_model, discriminator_model, gan_model)

if __name__ == "__main__":
    main()