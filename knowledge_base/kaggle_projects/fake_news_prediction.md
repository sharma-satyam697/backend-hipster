## Text Classification Using LSTM (Kaggle Project)

In this project, I built a deep learning model using an LSTM-based neural network to classify binary text data. The model architecture included an Embedding layer with a vocabulary size of 5000 and 40-dimensional embedded features, followed by a single LSTM layer with 100 units and a final Dense layer with a sigmoid activation function for binary output. The model was compiled using the Adam optimizer and binary cross-entropy loss function.

### Model Architecture
```python
embedded_features = 40
model = Sequential()
model.add(Embedding(5000, embedded_features, input_length=max_length))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
```

### Evaluation Results
- **Confusion Matrix:**
```
[[5045  153]
 [ 230 5797]]
```
- **Classification Report:**
```
              precision    recall  f1-score   support

           0       0.96      0.97      0.96      5198
           1       0.97      0.96      0.97      6027

    accuracy                           0.97     11225
   macro avg       0.97      0.97      0.97     11225
weighted avg       0.97      0.97      0.97     11225
```

These metrics reflect the model's strong and balanced ability to accurately predict both classes, with an overall accuracy of 97%. It demonstrates the model’s robustness and effectiveness in binary classification tasks.

This project highlights my proficiency in deep learning workflows using Keras, my ability to preprocess and vectorize text data effectively, and my focus on evaluating model quality using both confusion matrices and advanced classification metrics.
