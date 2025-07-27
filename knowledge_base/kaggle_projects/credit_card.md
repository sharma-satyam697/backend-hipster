## Credit Card Default Prediction Using ML (Kaggle Project)

### 📚 Background
In a world where consumerism is on the rise, the convenience of "Buy now, pay later" can often lead individuals into financial traps. While this model offers immediate gratification, it may also result in burdensome debt and missed payments. This project attempts to counter this issue using machine learning — enabling smarter credit decisions by analyzing historical financial behavior.

### 🎯 Objective
The goal of this project is to predict whether a credit card client will default on their payment in the next billing cycle, using their past financial data and payment patterns. We aim to assist credit institutions in making responsible and sustainable lending decisions.

---

### 🧾 Dataset Description
The dataset includes demographic, financial, and billing data from **Taiwanese credit card clients**, covering the period between April 2005 and September 2005. 
- Contains details like **credit limit**, **bill amounts**, **payment history**, and the **target variable** `will_default`
- All monetary values are in **New Taiwan (NT) Dollars**

---

### 🔁 Data Preprocessing & Balancing
The dataset was significantly imbalanced in terms of the target class `will_default`. To address this:
- **SMOTE (Synthetic Minority Over-sampling Technique)** was applied to balance the classes
- The new dataset shape became: `X.shape → (new rows, features)`

```python
versample = SMOTE()
X_input, y_output = df_smote.iloc[:,:-1], df_smote[['will_default']]
X, y = oversample.fit_resample(X_input, y_output)
df_smote = pd.concat([X, y], axis=1)
```

![Dataset Distribution](./08a7cd43-731c-49e0-a5d0-3cb22f4a3511.png)

---

### ⚙️ Models & Algorithms
A variety of classification algorithms were trained and evaluated:
- Support Vector Machine
- Decision Tree
- Random Forest
- AdaBoost
- K-Nearest Neighbors
- Logistic Regression
- XGBoost

| Algorithm              | Accuracy (Train) | Accuracy (Test) | Test Accuracy (MSE) |
|------------------------|------------------|------------------|----------------------|
| Support Vector Machine | 0.619            | 0.612            | 0.387                |
| Decision Tree          | 0.999            | 0.741            | 0.259                |
| AdaBoost               | 0.755            | 0.753            | 0.247                |
| Random Forest          | 0.999            | 0.812            | 0.187                |
| KNN                    | 0.771            | 0.653            | 0.347                |
| Logistic Regression    | 0.561            | 0.554            | 0.446                |
| XGBoost                | 0.858            | 0.804            | 0.196                |

![Model Performance](./b94ccf4a-b797-491a-af14-7ee307ac47ec.png)

---

### 🛠️ Model Selection & Optimization
Although several models performed well, **AdaBoostClassifier** was selected due to its generalizability and consistent performance.

**Hyperparameter Tuning** was conducted using `GridSearchCV`:
```python
params = {
    'n_estimators': [30, 50, 70, 100],
    'algorithm': ['SAMME', 'SAMME.R'],
    'learning_rate': [0.5, 0.7, 1, 1.4]
}
clf = GridSearchCV(estimator=AdaBoostClassifier(), param_grid=params, cv=5, scoring='accuracy')
clf.fit(X_train, y_train)
best_params = clf.best_params_
```

---

### 📊 Final Model Evaluation
The final AdaBoost model achieved an accuracy of **81.96%** on the test set. Evaluation metrics were as follows:

#### Classification Report
```
              precision    recall  f1-score   support

           0       0.84      0.95      0.89      5873
           1       0.67      0.34      0.45      1627

    accuracy                           0.82      7500
   macro avg       0.75      0.65      0.67      7500
weighted avg       0.80      0.82      0.80      7500
```

#### Confusion Matrix
```
[[5596  277]
 [1076  551]]
```

---

### ✅ Summary
This project showcases a full machine learning pipeline — from data cleaning and balancing to model selection and optimization. It demonstrates practical application of classification algorithms like AdaBoost and XGBoost for real-world financial prediction tasks. The system could potentially assist banks and fintech platforms in minimizing risk by proactively identifying users more likely to default.
