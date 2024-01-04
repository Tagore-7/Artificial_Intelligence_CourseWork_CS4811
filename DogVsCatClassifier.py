#!/usr/bin/env python
# coding: utf-8

################## TODO #####################
    # install tensorflow, pandas, numpy, PIL

# Import libraries
import os
import pandas as pd
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def prepare_val_train_dataset(train_data_dir = 'dogs-vs-cats/train/'):
     
    # Define the input shape and batch size
    input_shape = (128, 128, 3)
    batch_size = 32

    # Create an ImageDataGenerator for data augmentation and preprocessing
    data_generator = ImageDataGenerator(
        rescale=1.0 / 255.0,  # Rescale pixel values to [0, 1]
        validation_split=0.2,  # 20% of the data will be used for validation
    )

    # Load and preprocess the training data
    train_data = data_generator.flow_from_directory(
        train_data_dir,
        target_size=input_shape[:2],
        batch_size=batch_size,
        class_mode='binary',  # Binary classification
        subset='training',  # Training split
    )

    
    # Load and preprocess the validation data
    validation_data = data_generator.flow_from_directory(
        train_data_dir,
        target_size=input_shape[:2],
        batch_size=batch_size,
        class_mode='binary',  # Binary classification
        subset='validation',  # Validation split
    )
    
    ########################### TODO:A ###########################
        
        # Observe shapes of validation and training dataset 
    print("Training Data Shape:", train_data.image_shape, train_data.samples)
    print("Validation Data Shape:", validation_data.image_shape, validation_data.samples)
    
    #################### YOUR CODE ENDS HERE ##################### 
        

    # Create a dictionary to 
    class_to_label = train_data.class_indices


    # print classes to labels mapping (cat: 0, dog: 1)
    print("Class to Label Mapping:", class_to_label)
    
    return train_data, validation_data



class DogVsCatClassifier:
    def __init__(self, input_shape=(128, 128, 3)):
        self.model = self.build_model(input_shape)
        self.compile_model()

    def build_model(self, input_shape):
        model = keras.Sequential()

        # Convolutional layers
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        
        # Flatten the output from convolutional layers
        model.add(layers.Flatten())

        # Fully connected layers
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))  # Binary classification

        return model
    

    def compile_model(self):
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    def train(self, train_data, validation_data, epochs=15, batch_size=32):
        history = self.model.fit(
            train_data,
            epochs=epochs,
            validation_data=validation_data,
            batch_size=batch_size
        )
        return history

    def evaluate(self, test_data):
        #### TASK C: Expand to calculate Sensitivity, Specificity, F1 Score
        true_labels = test_data.labels
        predicted_prbs = self.model.predict(test_data)
        
        # Convert probabilities to binary predictions (0 or 1)
        predicted_labels = (predicted_prbs > 0.5).astype(int)
        
        #calculate confusion matrix
        conf_matrix = confusion_matrix(true_labels, predicted_labels)
        
        # Extract the true positive, true negative ,false positive, false negative
        tn, fp, fn, tp = conf_matrix.ravel()
        
        # Calculate Sensitivity, Specificity, F1 Score
        Sensitivity = tp/(tp+fn)
        Specificity = tn/(tn+fp)
        F1_Score = 2 * (sensitivity * (1 - specificity)) / (sensitivity + (1 - specificity))
        
        print("Confusion Matrix:")
        print(conf_matrix)
        print("\nSensitivity (True Positive Rate):", Sensitivity)
        print("\nSpecificity (True Negative Rate):", Specificity)
        print("F1 Score:", F1_Score)
        
        return Sensitivity, Specificity, F1_Score
        return self.model.evaluate(test_data)[1]

    def predict(self, image):
        # Assuming you have preprocessed the input image
        return self.model.predict(image)

    def save_model(self, model_path):
        self.model.save(model_path)

    def load_model(self, model_path):
        self.model = keras.models.load_model(model_path)


if __name__ == '__main__':
    # Prepare dataset
    train_data, validation_data = prepare_val_train_dataset('dogs-vs-cats/train/')
    
    # create classifier instance
    classifier = DogVsCatClassifier()

    # Train the model using your training data and validation data
    classifier.train(train_data, validation_data)

    # Evaluate the model on validation dataset
    accuracy = classifier.evaluate(validation_data)
    print(accuracy)
    
    ###### TASK D: Expand the below given code to test all the images in test1 folder. ######
    # Create a CSV file with column names: 
    # Image name, probability_score, predicted_class for all 12500 images 

    results_df = pd.DataFrame(columns=['Image name', 'Probability score', 'Predicted class'])

    # Path to the test1 folder
    test_folder_path = 'test1/'

    # Iterate over images in the test1 folder
    for image_name in os.listdir(test_folder_path):
        # Load the test image
        image_path = os.path.join(test_folder_path, image_name)
        image = Image.open(image_path)
        image = image.resize((128, 128))
        image_array = np.array(image) / 255.0

            # Make a prediction
        prediction = classifier.predict(np.expand_dims(image_array, axis=0))

            # Store the results in the DataFrame
        results_df = results_df.append({
                'Image name': image_name,
                'Probability score': prediction[0][0],
                'Predicted class': 'Dog' if prediction[0][0] > 0.5 else 'Cat'
            }, ignore_index=True)

    # The 'prediction' variable contains the model's output, which is a probability
    # You can interpret the result based on your class labels
    if prediction[0][0] > 0.5:
        print("It's a dog!")
    else:
        print("It's a cat!")

